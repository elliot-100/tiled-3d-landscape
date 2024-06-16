"""Tests for Heightmap class."""

from heightmap import Heightmap, Location


def test_create_heightmap_happy_path() -> None:
    """Test."""
    # arrange
    # act
    hm = Heightmap(32, 16)
    # assert
    assert hm.size_x == 32
    assert hm.size_y == 16


def test_in_bounds() -> None:
    """Test."""
    # arrange
    hm = Heightmap(5, 5)
    # act
    loc0 = Location(0, 0)
    loc1 = Location(4, 4)
    loc2 = Location(4, 5)
    # assert
    assert hm._in_bounds(loc0) is True
    assert hm._in_bounds(loc1) is True
    assert hm._in_bounds(loc2) is False
