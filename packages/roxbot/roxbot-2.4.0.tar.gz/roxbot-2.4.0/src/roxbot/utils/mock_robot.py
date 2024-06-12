#!/usr/bin/env python3
"""
mock robot data generator

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

import math
import asyncio
import json
import logging
from roxbot.utils import run_main_async

log = logging.getLogger("mock")

UPDATE_RATE = 1.0  # Hz
RADIUS = 10.0  # meters
SPEED = 1.0  # meters per second


# TODO: add middleware to send messages.


class MockRobot:
    """simulate a robot that drives around in cirles around origin"""

    def __init__(self) -> None:
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

    async def sim_loop(self, dt: float = 0.1) -> None:
        """simulate robot movement"""

        while True:
            self.theta += SPEED * dt / RADIUS
            self.x = RADIUS * (1 - math.cos(self.theta))
            self.y = RADIUS * math.sin(self.theta)

            # clip theta to 2pi
            self.theta %= 2 * math.pi

            await asyncio.sleep(dt)

    async def send_data(self) -> None:
        """send robot data to the UI"""

        while True:
            data = {
                "x": round(self.x, 3),
                "y": round(self.y, 3),
                "theta": round(self.theta, 3),
            }
            msg = json.dumps(data)
            log.info(f"Sending data: {msg}")
            await asyncio.sleep(1.0 / UPDATE_RATE)

    async def main(self) -> None:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.sim_loop())
            tg.create_task(self.send_data())


if __name__ == "__main__":
    run_main_async(MockRobot().main())
