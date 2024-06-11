#!/usr/bin/env python3
# type: ignore
"""
Created on Wed May 08 2024

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

from unittest.mock import AsyncMock, Mock

import pytest
import orjson
from roxbot.adapters.mqtt_adapter import MqttAdapter, MqttConfig, MqttMessage


async def dummy_coro(*args, **kwargs) -> None:  # type: ignore
    pass


@pytest.fixture
def mqtt_bridge() -> MqttAdapter:
    """Fixture to provide an MQTT bridge with a mocked client and ready state."""
    bridge = MqttAdapter(MqttConfig(host="localhost", port=1883))
    bridge._client = Mock()
    bridge._client.subscribe = AsyncMock()
    bridge._client.unsubscribe = AsyncMock()
    bridge._client_ready.set()  # Simulate that the client is ready for use.
    return bridge


@pytest.mark.asyncio
async def test_subscribe(mqtt_bridge: MqttAdapter) -> None:
    """Test that the bridge subscribes to a topic."""
    await mqtt_bridge.register_callback("/test", Mock())
    mqtt_bridge._client.subscribe.assert_called_once_with("/test")

    # try to subscribe again
    with pytest.raises(ValueError):
        await mqtt_bridge.register_callback("/test", Mock())


@pytest.mark.asyncio
async def test_remove_callback(mqtt_bridge: MqttAdapter) -> None:
    """Test removing a callback from a topic."""
    callback = Mock()
    topic = "/remove"

    # Register and then remove the callback
    await mqtt_bridge.register_callback(topic, callback)
    await mqtt_bridge.remove_callback(topic)
    mqtt_bridge._client.unsubscribe.assert_called_once_with(topic)

    # Ensure callback is actually removed
    assert topic not in mqtt_bridge._topic_callbacks


@pytest.mark.asyncio
async def test_remove_callback_not_exist(mqtt_bridge: MqttAdapter) -> None:
    """Test removing a callback that does not exist."""
    with pytest.raises(KeyError):
        await mqtt_bridge.remove_callback("/nonexistent")


@pytest.mark.asyncio
async def test_send(mqtt_bridge: MqttAdapter) -> None:
    """Test sending data to a topic."""
    topic = "/send"
    data = {"key": "value"}

    # Set up the mock for the asyncio.Queue put method
    mqtt_bridge._mqtt_queue.put = AsyncMock()

    # Send the data
    await mqtt_bridge.send(topic, data)

    # Check if the put method was called correctly
    mqtt_bridge._mqtt_queue.put.assert_awaited_once_with(
        MqttMessage(topic, orjson.dumps(data))
    )


@pytest.mark.asyncio
async def test_unsubscribe(mqtt_bridge: MqttAdapter) -> None:
    """Test unsubscribing from a topic."""
    topic = "/unsubscribe"

    # Ensure the bridge attempts to unsubscribe
    await mqtt_bridge.register_callback(topic, Mock())
    await mqtt_bridge.remove_callback(topic)
    mqtt_bridge._client.unsubscribe.assert_called_once_with(topic)
