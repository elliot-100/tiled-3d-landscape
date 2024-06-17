"""Tests for App class."""

from pytest import approx

from app import App
from camera import isometric_projection


def test_create_app_happy_path() -> None:
    """Test."""
    # arrange
    # act
    app0 = App(
        window_size=(800, 600),
        landscape_size_tiles=(3, 3),
    )
    # assert
    assert (app0.heightmap.size_x, app0.heightmap.size_x) == (4, 4)


def test_camera() -> None:
    """Test."""
    # arrange
    # act
    nw = isometric_projection(0, 0, 0)
    ne = isometric_projection(1, 0, 0)
    se = isometric_projection(1, 1, 0)
    sw = isometric_projection(0, 1, 0)

    # assert
    relative_tolerance = 1e-3
    assert nw == (0, 0)
    assert ne == approx((0.7071, 0.3535), relative_tolerance)
    assert se == approx((0, 0.7071), relative_tolerance)
    assert sw == approx((-0.7071, 0.3535), relative_tolerance)
