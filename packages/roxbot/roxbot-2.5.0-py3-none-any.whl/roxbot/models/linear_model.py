#!/usr/bin/env python3
"""
Simple linear model for generating setpoints.

Copyright (c) 2023-2024 ROX Automation - Jev Kuznetsov
"""

from typing import Optional
import math


class LinearModel:
    """Simple linear model for generating setpoints."""

    __slots__ = ("val", "roc", "setpoint", "min_val", "max_val")

    def __init__(
        self,
        roc: float,
        val: float = 0.0,
        setpoint: Optional[float] = None,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None,
    ):
        """
        Args:
            roc (float): rate of change / sec
            val (float): current value
            setpoint (float, optional): target value.
            max_val (float, optional): maximum value
            min_val (float, optional): minimum value
        """

        self.val = val
        self.roc = roc
        if setpoint is None:
            self.setpoint = val
        else:
            self.setpoint = setpoint

        self.min_val = min_val
        self.max_val = max_val

    def step(self, delta_t: float) -> None:
        """perform timestep"""

        if delta_t < 0:
            raise ValueError(f"dt may not be negative, got {delta_t=} ")

        error = self.setpoint - self.val
        step = math.copysign(1, error) * self.roc * delta_t

        if abs(step) > abs(error):
            self.val += error
        else:
            self.val += step

        if self.max_val is not None:
            self.val = min(self.val, self.max_val)

        if self.min_val is not None:
            self.val = max(self.val, self.min_val)

    def __repr__(self) -> str:
        return f"LinearModel(val={self.val}, setpoint={self.setpoint}, roc={self.roc})"
