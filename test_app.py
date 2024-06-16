"""Tests for App class."""

import unittest

import app


class TestCase(unittest.TestCase):
    """Test case."""

    def test_create_tiler_object(self) -> None:
        """Test."""
        test_tiler = app.App()
        self.assertEqual(test_tiler.map_size_cells, (16, 16))


if __name__ == "__main__":
    unittest.main()
