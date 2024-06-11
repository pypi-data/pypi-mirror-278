# type: ignore

from roxbot import interfaces
from roxbot.vectors import Vector


def test_machine():
    class TestMachine(interfaces.MachineProtocol):
        def get_pose(self) -> interfaces.Pose:
            return interfaces.Pose(1, 2, 3)

        def cmd_vel(self, linear_velocity: float, angular_velocity: float) -> None:
            pass

        def cmd_curvature(self, v_linear: float, curvature: float) -> None:
            pass

        async def main(self) -> None:
            pass

    m = TestMachine()
    assert m.get_pose() == interfaces.Pose(1, 2, 3)
    m.cmd_vel(1, 1)
    m.cmd_curvature(1, 1)

    xy = m.get_pose().xy
    assert xy == Vector(1, 2)
