"""Test suite."""

import unittest

import app


class TestCase(unittest.TestCase):
    """Test case."""

    def test_create_tiler_object(self) -> None:
        """Test."""
        test_tiler = app.App()
        self.assertEqual(test_tiler.map_size_cells, (16, 16))
        self.assertEqual(test_tiler.terrain.heightmap_size_x, 17)
        self.assertEqual(test_tiler.terrain.heightmap_size_y, 17)


if __name__ == "__main__":
    unittest.main()
