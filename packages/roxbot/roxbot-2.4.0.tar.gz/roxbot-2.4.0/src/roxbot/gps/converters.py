#!/usr/bin/env python3
"""
gps conversions

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

import warnings
import os
import cmath
from math import degrees, radians
from typing import Tuple
from pymap3d import enu2geodetic, geodetic2enu  # type: ignore


def heading_to_theta(angle_deg: float) -> float:
    """convert gps heading to theta in radians"""
    h = -1j * cmath.rect(1, radians(angle_deg))
    return -cmath.phase(h)


def theta_to_heading(angle_rad: float) -> float:
    """convert theta in radians to gps heading"""
    h = -1j * cmath.rect(1, angle_rad)
    return degrees(-cmath.phase(h))  # type: ignore


class GpsConverter:
    """coordinate converter (lat,lon) to (xEast,yNorth). wrapper around pymap3d"""

    def __init__(self, gps_ref: tuple[float, float] | None = None) -> None:
        """create converter, try to get reference from GPS_REF env variable"""
        if gps_ref is not None:
            self.gps_ref = gps_ref
        else:
            # get gps reference from environment variable
            var = os.environ.get("GPS_REF")
            if var is None:  # not set, use default fallback.
                new_gps_ref = (51.0, 6.0)
                warnings.warn(
                    f"GPS_REF environment variable not set, using default {new_gps_ref}"
                )
            else:
                new_gps_ref = tuple(float(x) for x in var.split(","))  # type: ignore
                if len(new_gps_ref) != 2:
                    raise ValueError(f"invalid GPS_REF: {var}")

            self.gps_ref = new_gps_ref

    def latlon_to_enu(self, latlon: Tuple[float, float]) -> Tuple[float, float]:
        x, y, _ = geodetic2enu(
            latlon[0], latlon[1], 0, self.gps_ref[0], self.gps_ref[1], 0
        )
        return float(x), float(y)

    def enu_to_latlon(self, xy: Tuple[float, float]) -> Tuple[float, float]:
        lat, lon, _ = enu2geodetic(xy[0], xy[1], 0, self.gps_ref[0], self.gps_ref[1], 0)
        return float(lat), float(lon)
