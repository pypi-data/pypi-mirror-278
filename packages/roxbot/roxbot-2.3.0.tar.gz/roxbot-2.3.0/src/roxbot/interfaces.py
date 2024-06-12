"""Common interface definitions"""

from typing import Any, Callable, Dict, List, NamedTuple, Protocol, TypeAlias

from .vectors import Vector

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


class BridgeProtocol(Protocol):
    """interface for communication bridge"""

    async def send(self, topic: str, msg: JsonSerializableType) -> None:
        """send a message to a topic"""

    async def register_callback(self, topic: str, callback: Callable) -> None:
        """register a callback for a topic, subscribe to topic if required"""

    async def remove_callback(self, topic: str) -> None:
        """remove callback for a topic and unsubscribe if required"""

    async def main(self) -> None:
        """main loop for the bridge"""
