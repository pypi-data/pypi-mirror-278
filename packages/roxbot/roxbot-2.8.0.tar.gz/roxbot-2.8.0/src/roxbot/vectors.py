#!/usr/bin/env python3
"""
Vectors moved to rox-vectors. This file is to keep backwards compatibility.

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

import warnings

from rox_vectors import *  # noqa: F401, F403

warnings.warn(
    "roxbot.vectors is deprecated, use rox_vectors instead", DeprecationWarning
)
