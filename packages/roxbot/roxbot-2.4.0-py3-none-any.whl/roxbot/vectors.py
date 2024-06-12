#!/usr/bin/env python3
"""
Vectors moved to rox-vectors. This file is to keep backwards compatibility.

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

import rox_vectors
from rox_vectors import Line, distance_to_b, distance_to_line, point_on_line  # noqa

import numpy as np
from numpy.typing import NDArray  # pylint: disable=import-error, no-name-in-module


class Vector(rox_vectors.Vector):
    """vector class extended  with numpy array conversion"""

    def __array__(self) -> NDArray[np.float32]:
        """numpy array compatibility"""
        return np.array([self.x, self.y])
