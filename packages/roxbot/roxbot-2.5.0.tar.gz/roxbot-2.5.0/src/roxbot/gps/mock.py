#!/usr/bin/env python3
"""
Gps mock for testing

Functionality:
---------------

* publish gps position and orientation

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

import asyncio
import logging
import time
from datetime import datetime
from dataclasses import dataclass

from roxbot.adapters import MqttAdapter
from roxbot.config import MqttConfig
from roxbot.gps import converters
from roxbot.interfaces import HeadingData, PositionData
from roxbot.utils import run_main_async

SET_POSE_TOPIC = "/mock_gps/set_pose"
PUBLISH_FREQ = 5  # Hz
MQTT_CFG = MqttConfig()


@dataclass
class Pose:
    x: float
    y: float
    theta: float


def timestamp() -> float:
    return round(time.time(), 3)


class MockGPS:
    def __init__(self) -> None:
        self.pose = Pose(0.0, 0.0, 0.0)
        self.fix_quality = 4

        self._log = logging.getLogger("mock_gps")

        self._mqtt_adapter = MqttAdapter()

    def set_pose(self, args: dict) -> None:
        """example callback function"""
        self._log.info(f"Setting pose to {args=}")

        if not isinstance(args, dict):
            self._log.error("Invalid argument type, must be dict")
            return

        try:
            self.pose.x = args["x"]
            self.pose.y = args["y"]
            self.pose.theta = args["theta"]
        except KeyError as e:
            self._log.error(f"Missing key {e}")

    async def publish_data(self) -> None:
        """publish gps position and orientation"""
        delay = 1 / PUBLISH_FREQ
        gps_converter = converters.GpsConverter()

        while True:
            # position
            lat, lon = gps_converter.enu_to_latlon((self.pose.x, self.pose.y))

            ts = timestamp()

            position = PositionData(
                lat,
                lon,
                self.pose.x,
                self.pose.y,
                self.fix_quality,
                datetime.now().strftime("%H:%M:%S"),
                ts,
            )
            await self._mqtt_adapter.publish(
                MQTT_CFG.gps_position_topic, position.to_dict()
            )

            # heading
            heading = converters.theta_to_heading(self.pose.theta)
            heading_data = HeadingData(heading, 0.1, self.pose.theta, ts)

            await self._mqtt_adapter.publish(
                MQTT_CFG.gps_direction_topic, heading_data.to_dict()
            )

            await asyncio.sleep(delay)

    async def main(self) -> None:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self._mqtt_adapter.main())
            await self._mqtt_adapter.register_callback(SET_POSE_TOPIC, self.set_pose)
            tg.create_task(self.publish_data())


if __name__ == "__main__":
    gps = MockGPS()
    run_main_async(gps.main())
