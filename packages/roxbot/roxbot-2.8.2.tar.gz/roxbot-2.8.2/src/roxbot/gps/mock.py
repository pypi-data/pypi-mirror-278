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
        self.fix_quality = 4  # 4 is RTK fix, change this if needed

        self._pose = Pose(0.0, 0.0, 0.0)
        self._log = logging.getLogger("mock_gps")

        self._mqtt_adapter = MqttAdapter()

    def set_pose(self, x: float, y: float, theta: float) -> None:
        """set pose"""
        self._pose = Pose(x, y, theta)

    def _pose_cmd(self, args: dict) -> None:
        """set pose from mqtt command"""
        self._log.info(f"Setting pose to {args=}")

        if not isinstance(args, dict):
            self._log.error("Invalid argument type, must be dict")
            return

        try:
            self.set_pose(args["x"], args["y"], args["theta"])
        except KeyError as e:
            self._log.error(f"Missing key {e}")

    async def publish_data(self) -> None:
        """publish gps position and orientation"""
        delay = 1 / PUBLISH_FREQ
        gps_converter = converters.GpsConverter()

        while True:
            # position
            lat, lon = gps_converter.enu_to_latlon((self._pose.x, self._pose.y))

            ts = timestamp()

            position = PositionData(
                lat,
                lon,
                self._pose.x,
                self._pose.y,
                self.fix_quality,
                datetime.now().strftime("%H:%M:%S"),
                ts,
            )
            await self._mqtt_adapter.publish(
                MQTT_CFG.gps_position_topic, position.to_dict()
            )

            # heading
            heading = converters.theta_to_heading(self._pose.theta)
            heading_data = HeadingData(heading, 0.1, self._pose.theta, ts)

            await self._mqtt_adapter.publish(
                MQTT_CFG.gps_direction_topic, heading_data.to_dict()
            )

            await asyncio.sleep(delay)

    async def main(self) -> None:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self._mqtt_adapter.main())
            await self._mqtt_adapter.register_callback(SET_POSE_TOPIC, self._pose_cmd)
            tg.create_task(self.publish_data())


if __name__ == "__main__":
    gps = MockGPS()
    run_main_async(gps.main())
