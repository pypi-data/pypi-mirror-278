#!/usr/bin/env python3
"""
MQTT bridge for communication between subsystems

This class class abstracts away specific mqtt implementation

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

import asyncio
import logging
from typing import Dict, Callable
import orjson
import aiomqtt as mqtt

from roxbot.config import MqttConfig
from roxbot.interfaces import MqttMessage, JsonSerializableType


class MqttAdapter:
    """MQTT bridge for communication between subsystems"""

    def __init__(self, config: MqttConfig | None = None) -> None:
        self._log = logging.getLogger(self.__class__.__name__)
        self._topic_callbacks: Dict[str, Callable] = {}  # topic callbacks

        self.config = config or MqttConfig()

        self._client: mqtt.Client | None = None
        self._client_ready = asyncio.Event()

        self._mqtt_queue: asyncio.Queue[MqttMessage] = asyncio.Queue(10)

    async def _publish_mqtt(self, client: mqtt.Client) -> None:
        """publish items from mqtt queue.
        an item must have .mqtt_message() and .mqtt_topic() methods"""

        while True:
            item = await self._mqtt_queue.get()
            msg = item.message
            topic = item.topic

            # publish message
            self._log.debug(f"{topic=}, {msg=}")
            await client.publish(topic, msg.encode() if isinstance(msg, str) else msg)
            self._mqtt_queue.task_done()

    async def _receive_mqtt(self, client: mqtt.Client) -> None:
        """receive velocity setpoint from mqtt"""

        self._log.debug("Starting mqtt receive loop")
        async for message in client.messages:
            try:
                self._log.debug(f"{message.topic=}, {message.payload=}")
                if not isinstance(message.payload, (str, bytes, bytearray)):
                    raise TypeError(f"Unexpected payload type {type(message.payload)}")

                topic = message.topic.value

                data = orjson.loads(message.payload)
                if topic in self._topic_callbacks:
                    self._topic_callbacks[topic](data)

            except (TypeError, orjson.JSONDecodeError) as e:
                self._log.error(f"Error decoding message {message.payload!r}: {e}")

            except Exception as e:
                self._log.exception(e, exc_info=True)

    async def register_callback(self, topic: str, fcn: Callable) -> None:
        """add callback to topic."""
        if topic in self._topic_callbacks:
            raise ValueError(f"Topic {topic} already has a callback registered")

        await self.subscribe(topic)

        self._topic_callbacks[topic] = fcn

    async def remove_callback(self, topic: str) -> None:
        """remove topic callback"""
        del self._topic_callbacks[topic]
        await self.unsubscribe(topic)

    async def send(self, topic: str, data: JsonSerializableType) -> None:
        """send data to topic"""

        await self._mqtt_queue.put(MqttMessage(topic, orjson.dumps(data)))

    async def subscribe(self, topic: str) -> None:
        """subscribe to topic"""

        await asyncio.wait_for(self._client_ready.wait(), timeout=1)

        if self._client is None:
            raise RuntimeError("MQTT client not initialized")

        self._log.info(f"Subscribing to {topic}")
        await self._client.subscribe(topic)

    async def unsubscribe(self, topic: str) -> None:
        """unsubscribe from topic"""
        if self._client is None:
            raise RuntimeError("MQTT client not initialized")

        self._log.info(f"Unsubscribing from {topic}")
        await self._client.unsubscribe(topic)

    async def main(self) -> None:
        """starting point to handle mqtt communication, starts send and recieve coroutines"""

        self._log.info(f"Connecting to {self.config.host}:{self.config.port}")

        async with mqtt.Client(self.config.host, port=self.config.port) as client:
            self._client = client
            self._client_ready.set()
            async with asyncio.TaskGroup() as tg:
                tg.create_task(self._receive_mqtt(client))
                tg.create_task(self._publish_mqtt(client))

        self._client = None
