"""tests for diff_drive model"""

import pytest
from roxbot.models import DiffDriveModel
from roxbot.interfaces import Pose, MachineProtocol


@pytest.fixture
def robot() -> DiffDriveModel:
    # Setup with default or custom parameters
    return DiffDriveModel(wheel_base=0.16, wheel_diameter=0.066, wheel_accel=1e6)


def test_protocol() -> None:
    """check protocol compliance, not tested during run, this is for the typechecker"""

    robot: MachineProtocol = DiffDriveModel()

    assert isinstance(robot, DiffDriveModel)


def test_curvature(robot: DiffDriveModel) -> None:
    # Test with non-zero velocities
    robot.cmd_lr(1.0, 2.0)
    robot.step(1.0)
    expected_curvature = 1 / (
        0.5 * robot.DEFAULT_WHEEL_BASE * (1.0 + 2.0) / (2.0 - 1.0)
    )
    assert robot.curvature == pytest.approx(expected_curvature)

    # Test with zero velocity difference
    robot.cmd_lr(1.0, 1.0)
    robot.step(1.0)
    assert robot.curvature == 0.0


def test_set_pose(robot: DiffDriveModel) -> None:
    x, y, theta = 1.0, 2.0, 3.1415

    robot.pose = Pose(x, y, theta)

    pose = robot.get_pose()
    assert pose.x == x
    assert pose.y == y
    assert pose.theta == theta


def test_vc_to_vels(robot: DiffDriveModel) -> None:
    v, c = 1.0, 0.5  # Example values for linear velocity and curvature

    robot.cmd_curvature(v, c)
    vl, vr = robot.setpoints

    # Calculate expected values
    R = 1 / c
    expected_vr = (v * robot.DEFAULT_WHEEL_BASE + 2 * R * v) / 2 / R
    expected_vl = 2 * v - expected_vr

    assert vl == pytest.approx(expected_vl)
    assert vr == pytest.approx(expected_vr)

    # Test with zero curvature
    robot.cmd_curvature(v, 0.0)
    vl, vr = robot.setpoints

    assert vl == vr == v


def test_cmd_vel_straight_line(robot: DiffDriveModel) -> None:
    # Test moving in a straight line (angular velocity = 0)
    robot.cmd_vel(1.0, 0.0)  # 1 m/s linear velocity, 0 rad/s angular velocity
    assert robot.left_wheel.setpoint == 1.0
    assert robot.right_wheel.setpoint == 1.0


def test_cmd_vel_turn_in_place(robot: DiffDriveModel) -> None:
    # Test turning in place (linear velocity = 0)
    robot.cmd_vel(0.0, 1.0)  # 0 m/s linear velocity, 1 rad/s angular velocity
    vl, vr = robot.setpoints
    assert vl == -0.08  # -W/2 * angular_velocity
    assert vr == 0.08  # W/2 * angular_velocity


def test_repr(robot: DiffDriveModel) -> None:
    robot.cmd_lr(1.0, 2.0)

    repr_string = repr(robot)
    expected_string = (
        f"diffdrive vels: ({robot.vl:.2f},{robot.vr:.2f}) C={robot.curvature}"
    )

    assert repr_string == expected_string
