"""Tests for App class."""

from pytest import approx

from app import App


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


def test_world_xyz_to_window_xy() -> None:
    """Test."""
    # arrange
    app0 = App(
        window_size=(800, 600),
        landscape_size_tiles=(1, 1),
    )
    # act
    nw = app0._world_xyz_to_window_xy(0, 0)
    ne = app0._world_xyz_to_window_xy(100, 0)
    se = app0._world_xyz_to_window_xy(100, 100)
    sw = app0._world_xyz_to_window_xy(0, 100)

    # assert
    tolerance = 1e3
    assert nw == approx((400, 100), tolerance)
    assert ne == approx((470.710, 135.355), tolerance)
    assert se == approx((400, 170.710), tolerance)
    assert sw == approx((329.289, 135.355), tolerance)
