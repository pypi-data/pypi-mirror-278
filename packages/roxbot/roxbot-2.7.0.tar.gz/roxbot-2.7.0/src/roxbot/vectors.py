#!/usr/bin/env python3
"""
Vectors moved to rox-vectors. This file is to keep backwards compatibility.

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

from __future__ import annotations
import rox_vectors
from rox_vectors import Line, distance_to_b, distance_to_line, point_on_line  # noqa

import numpy as np
from numpy.typing import NDArray  # pylint: disable=import-error, no-name-in-module

from roxbot.gps.converters import enu_to_latlon, latlon_to_enu


class Vector(rox_vectors.Vector):
    """vector class extended  with numpy array conversion"""

    def __array__(self) -> NDArray[np.float32]:
        """numpy array compatibility"""
        return np.array([self.x, self.y])

    @property
    def latlon(self) -> tuple[float, float]:
        """convert from xy to latlon"""
        return enu_to_latlon(self.xy)

    @classmethod
    def from_latlon(cls, latlon: tuple[float, float]) -> Vector:
        """convert from latlon to xy"""

        x, y = latlon_to_enu(latlon)
        return cls(x, y)
