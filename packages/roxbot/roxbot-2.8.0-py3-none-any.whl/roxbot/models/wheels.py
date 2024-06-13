#!/usr/bin/env python3
"""
Driving and steering wheels

Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""

import math
from typing import Optional
from .linear_model import LinearModel


class Wheel:
    """simple wheel model with a linear speed profile"""

    __slots__ = (
        "_diameter",
        "_circumference",
        "_model",
        "distance",
        "_distance",
        "time",
    )

    def __init__(
        self, diameter: float, accel: float, max_velocity: Optional[float] = None
    ):
        """create a wheel wit LinearModel driver and a diameter
        Parameters
        ----------
        diameter : float [m] wheel diameter
        accel : float [m/s^2] acceleration
        max_velocity : float [m/s] maximum velocity"""

        self._diameter = diameter
        self._circumference = math.pi * self._diameter
        self.distance = 0.0
        self.time = 0.0

        # linear velocity model in m/s
        if max_velocity is not None:
            self._model = LinearModel(
                roc=accel, max_val=max_velocity, min_val=-max_velocity
            )
        else:
            self._model = LinearModel(roc=accel)

        # keep last distance reading
        self._distance = 0.0

    @property
    def rps(self) -> float:
        """revolutions per second"""
        return self._model.val / self._circumference

    @property
    def velocity_ms(self) -> float:
        """axle velocity in m/s"""
        return self._model.val

    @property
    def revolutions(self) -> float:
        """number of revolutions"""
        return self.distance / self._circumference

    @property
    def ds(self) -> float:
        """distance travelled since last step"""

        ds = self.distance - self._distance
        self._distance = self.distance
        return ds

    @property
    def setpoint(self) -> float:
        """get velocity setpoint in m/s"""
        return self._model.setpoint

    def set_velocity_ms(self, v: float) -> None:
        """set velocity in m/s"""
        self._model.setpoint = v

    def step(self, delta_t: float) -> None:
        """perform timestep to update"""
        self._model.step(delta_t)
        self.distance += self._model.val * delta_t
        self.time += delta_t

    def __repr__(self) -> str:
        return f"Wheel(rps={self.rps:.2f}, velocity={self.velocity_ms:.2f} m/s)"
