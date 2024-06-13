"""Common interface definitions"""

from typing import Any, Callable, Dict, List, NamedTuple, Protocol, TypeAlias, Tuple

from .vectors import Vector
from .gps.converters import (
    latlon_to_enu,
    theta_to_heading,
    heading_to_theta,
    enu_to_latlon,
)


JsonSerializableType: TypeAlias = Dict[str, Any] | List[Any] | str | int | float | bool

# -----------------data types-----------------


class Pose(NamedTuple):
    """Represents a pose in 2D space"""

    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0

    @property
    def xy(self) -> Vector:
        return Vector(self.x, self.y)

    @classmethod
    def from_gps(cls, lat: float, lon: float, heading: float) -> "Pose":
        """create pose from gps coordinates"""
        x, y = latlon_to_enu((lat, lon))
        theta = heading_to_theta(heading)

        return cls(x, y, theta)

    def to_gps(self) -> Tuple[float, float, float]:
        """convert pose to gps coordinates"""
        lat, lon = enu_to_latlon((self.x, self.y))
        heading = theta_to_heading(self.theta)

        return lat, lon, heading

    def __str__(self) -> str:
        return f"x={self.x:.3f}, y={self.y:.3f}, theta={self.theta:.3f}"


class MqttMessage(NamedTuple):
    topic: str
    message: str | bytes


class PositionData(NamedTuple):
    """latitude and longitude data"""

    lat: float
    lon: float
    x: float
    y: float
    gps_qual: int
    time: str
    ts: float  # system time (epoch)

    def to_dict(self) -> dict:
        return self._asdict()  # type: ignore # pylint: disable=no-member


class HeadingData(NamedTuple):
    """heading data"""

    heading: float
    heading_stdev: float
    theta: float
    ts: float

    def to_dict(self) -> dict:
        return self._asdict()  # type: ignore # pylint: disable=no-member


# ----------------porotols-----------------


class MachineProtocol(Protocol):
    """generic machine interface, provides a uniform interface for
    different machine types such as trikes, differential drives, etc."""

    def get_pose(self) -> Pose:
        """return current pose (x, y, theta), in meters.
        Pose class provides a method for converting to GPS coordinates."""

    def cmd_vel(self, linear_velocity: float, angular_velocity: float) -> None:
        """send velocity commands to the machine"""

    def cmd_curvature(self, v_linear: float, curvature: float) -> None:
        """motion command by curvature

        Args:
            v_linear (float): driving velocity
            curvature (float): driving curvature (1/radius)
        """


class AdapterProtocol(Protocol):
    """interface for communication bridge"""

    async def publish(self, topic: str, msg: JsonSerializableType) -> None:
        """send a message to a topic"""

    async def register_callback(self, topic: str, callback: Callable) -> None:
        """register a callback for a topic, subscribe to topic if required"""

    async def remove_callback(self, topic: str) -> None:
        """remove callback for a topic and unsubscribe if required"""

    async def main(self) -> None:
        """main loop for the bridge"""
