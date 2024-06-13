from roxbot.gps.mock import MockGPS


def test_set_pose() -> None:
    """Test setting the pose."""

    mock = MockGPS()

    assert mock._pose.x == 0.0
    assert mock._pose.y == 0.0
    assert mock._pose.theta == 0.0

    mock._pose_cmd({"x": 1.0, "y": 2.0, "theta": 3.0})

    assert mock._pose.x == 1.0
    assert mock._pose.y == 2.0
    assert mock._pose.theta == 3.0
