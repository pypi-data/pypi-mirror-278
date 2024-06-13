from roxbot.gps.mock import MockGPS


def test_set_pose() -> None:
    """Test setting the pose."""

    mock = MockGPS()

    assert mock.pose.x == 0.0
    assert mock.pose.y == 0.0
    assert mock.pose.theta == 0.0

    mock.set_pose({"x": 1.0, "y": 2.0, "theta": 3.0})

    assert mock.pose.x == 1.0
    assert mock.pose.y == 2.0
    assert mock.pose.theta == 3.0
