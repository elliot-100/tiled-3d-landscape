"""Tests for App class."""

from app import App


def test_create_app_happy_path() -> None:
    """Test."""
    app0 = App(
        window_size=(800, 600),
        landscape_size_tiles=(3, 3),
    )
    assert app0.heightmap.size_x, app0.heightmap.size_x == (4, 4)
