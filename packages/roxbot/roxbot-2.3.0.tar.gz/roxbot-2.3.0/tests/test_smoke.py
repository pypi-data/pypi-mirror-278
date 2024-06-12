#!/usr/bin/env python3
"""
Smoke tests - check basics such as imports etc.

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""


async def dummy_coro() -> None:
    pass


def test_interfaces() -> None:
    from roxbot import interfaces

    interfaces.Pose()
    interfaces.MqttMessage("topic", "message")


def test_runners() -> None:
    from roxbot.utils import run_main_async

    run_main_async(dummy_coro())


def test_mocks() -> None:
    from roxbot.utils import mock_robot

    mock_robot.MockRobot()


def test_bridges() -> None:
    from roxbot.adapters.mqtt_adapter import MqttAdapter

    MqttAdapter()


def test_nodes() -> None:
    from roxbot.nodes import gps_node

    gps_node.GpsNode()
