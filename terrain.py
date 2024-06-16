"""Terrain class."""

import random


class Terrain:
    def __init__(self, heightmap_size_x, heightmap_size_y):
        self.heightmap_size_x = heightmap_size_x
        self.heightmap_size_y = heightmap_size_y
        self.map_depth = self.heightmap_size_x + self.heightmap_size_y
        self.heightmap = [
            [0 for _x in range(self.heightmap_size_x)]
            for _y in range(self.heightmap_size_y)
        ]
        print("created terrain data")

    def perturb(self):
        """
        Drop a quantity of particles at a single point on the Terrain object, then move the particles to neighbour cells
        until the terrain is 'stable'.
        """
        particles_per_drop = 128
        drop_index_x, drop_index_y = self.get_random_pos()
        # print('drop at', drop_index_x, drop_index_y)
        self.heightmap[drop_index_x][drop_index_y] += particles_per_drop
        neighbour_offsets = [
            (-1, -1),
            (0, -1),
            (1, -1),
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
        ]
        cycle = True
        while cycle is True:
            particle_moved_this_land_cycle = False
            for index_x in range(self.heightmap_size_x):
                for index_y in range(self.heightmap_size_y):
                    random.shuffle(neighbour_offsets)
                    for neighbour in neighbour_offsets:
                        current_cell_height = self.heightmap[index_x][index_y]
                        try:  # to address neighbour
                            neighbour_cell_height = self.heightmap[
                                index_x + neighbour[0]
                            ][index_y + neighbour[1]]
                            if current_cell_height - neighbour_cell_height > 1:
                                self.heightmap[index_x + neighbour[0]][
                                    index_y + neighbour[1]
                                ] += 1
                                self.heightmap[index_x][index_y] -= 1
                                # current_cell_height = self.heightmap[index_x][index_y]
                                particle_moved_this_land_cycle = True
                        except (
                            IndexError
                        ):  # can't address neighbour, it's out of bounds
                            pass

            if particle_moved_this_land_cycle is False:
                break

    def get_random_pos(self):
        """
        Get a random point on the heightmap.

        :return: Tuple representing an x, y position on the heightmap grid
        """
        # never returns an edge node
        return random.randint(1, self.heightmap_size_x - 1), random.randint(
            1, self.heightmap_size_y - 1
        )

    def normalise(self):
        """
        Lowers the whole terrain so that its lowest point is at zero height.
        """
        lowest_height_value = min([min(row) for row in self.heightmap])
        if lowest_height_value > 0:
            for index_x in range(self.heightmap_size_x):
                for index_y in range(self.heightmap_size_y):
                    self.heightmap[index_x][index_y] -= 1
