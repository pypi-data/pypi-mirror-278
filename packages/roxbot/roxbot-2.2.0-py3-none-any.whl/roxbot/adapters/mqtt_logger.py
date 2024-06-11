#!/usr/bin/env python3
"""
simple MQTT logger, forwards log messages to an MQTT topic


Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

import asyncio
import aiomqtt as mqtt

from logging import LogRecord, Formatter, Logger
from logging.handlers import QueueHandler

from roxbot.config import MqttConfig


class MqttLogger:
    """MQTT bridge for communication between subsystems"""

    def __init__(
        self, logger: Logger | None = None, config: MqttConfig | None = None
    ) -> None:
        """create mqtt logger

        Args:
            config (MqttConfig | None, optional): mqtt configuration. Defaults to None.
            logger (Logger | None, optional): logging.logger instance to attach handler. Defaults to None.
        """
        self.config = config or MqttConfig()
        self._mqtt_queue: asyncio.Queue[LogRecord] = asyncio.Queue(10)

        if logger is not None:
            self.add_handler(logger)

    def get_log_handler(self) -> QueueHandler:
        """return a logging handler that logs to mqtt"""
        handler = QueueHandler(self._mqtt_queue)
        return handler

    def add_handler(self, logger: Logger) -> None:
        """add mqtt handler to logger"""
        logger.addHandler(self.get_log_handler())

    async def _publish_mqtt(self) -> None:
        """publish items from mqtt queue."""

        formatter = Formatter(
            fmt="%(asctime)s.%(msecs)03d [%(name)s] %(levelname)s %(message)s",
            datefmt="%H:%M:%S",
        )

        async with mqtt.Client(self.config.host, port=self.config.port) as client:
            while True:
                log_record = await self._mqtt_queue.get()
                log_msg = formatter.format(log_record)

                # publish message
                await client.publish(self.config.log_topic, log_msg.encode())
                self._mqtt_queue.task_done()

    async def main(self) -> None:
        """starting point to handle mqtt communication, starts send and recieve coroutines"""

        await self._publish_mqtt()
