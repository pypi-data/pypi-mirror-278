#!/usr/bin/env python3
"""
GPS node listens to mqtt gps topics and aggregates dat

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

import logging
import time
from enum import Enum, auto

import aiomqtt
import orjson

from roxbot.config import MqttConfig
from roxbot.interfaces import Pose


# enum for gps warnings
class FixProblem(Enum):
    """enum for gps warnings"""

    NONE = auto()
    INCOMPLETE_DATA = auto()
    NO_RTK_FIX = auto()
    OLD_FIX = auto()


class FixException(Exception):
    """exception for gps fix errors"""

    def __init__(self, reason: FixProblem) -> None:
        self.reason = reason

    def __str__(self) -> str:
        return f"GPS fix problem: {self.reason.name}"


class GpsNode:
    """interface to gps mqtt data, works in meters and radians.
    latlon conversion is done by the gps sender node"""

    def __init__(self) -> None:
        self._log = logging.getLogger("gps_node")
        self.last_update = 0.0  # last update time
        self.x = 0.0  # x position in meters
        self.y = 0.0  # y position in meters
        self.theta = 0.0  # heading in radians (data from gps, not adjusted)
        self.gps_qual = 0  # gps quality

    async def _mqtt_loop(self) -> None:
        """receive mqtt messages"""
        cfg = MqttConfig()

        self._log.info(f"Connecting to {cfg.host}:{cfg.port}")
        pos_topic = cfg.gps_position_topic
        dir_topic = cfg.gps_direction_topic

        async with aiomqtt.Client(cfg.host, port=cfg.port) as client:
            await client.subscribe(pos_topic)
            await client.subscribe(dir_topic)
            async for message in client.messages:
                try:
                    data = orjson.loads(message.payload)  # type: ignore
                    self._log.debug(f"received {data=}")
                    if message.topic.matches(pos_topic):
                        self.x = data["x"]
                        self.y = data["y"]
                        self.gps_qual = data["gps_qual"]
                        self.last_update = data["ts"]

                    if message.topic.matches(dir_topic):
                        self.theta = data["theta"]
                        self.last_update = data["ts"]

                except Exception as e:
                    self._log.error(e)

    def get_pose(self, max_age: float = 1.0) -> Pose:
        """returns pose or raises FixException if data is too old"""
        if time.time() - self.last_update > max_age:
            raise FixException(FixProblem.OLD_FIX)

        if self.gps_qual != 4:
            raise FixException(FixProblem.NO_RTK_FIX)

        return Pose(self.x, self.y, self.theta)

    async def main(self) -> None:
        """main coroutine"""
        await self._mqtt_loop()


if __name__ == "__main__":
    # simple standalone demo code
    from roxbot.utils import run_main_async

    gps = GpsNode()
    run_main_async(gps.main())
