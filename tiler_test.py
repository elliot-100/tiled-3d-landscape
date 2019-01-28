import unittest
import tiler


class TestCase(unittest.TestCase):
    def test_create_tiler_object(self):
        test_tiler = tiler.Tiler()
        self.assertEqual(test_tiler.map_size_cells, (16, 16))
        self.assertEqual(test_tiler.terrain.heightmap_size_x, 17)
        self.assertEqual(test_tiler.terrain.heightmap_size_y, 17)


if __name__ == '__main__':
    unittest.main()