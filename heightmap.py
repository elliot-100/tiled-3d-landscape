"""Heightmap class."""

import random
from dataclasses import dataclass

NEIGHBOUR_OFFSETS = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
]


@dataclass
class Location:
    """Represents a location on the Heightmap."""

    x: int
    y: int


class Heightmap:
    """Represents a heightmap.

    Attributes
    ----------
    size_x: int
    size_y: int
    map_depth: int
    heightmap: list[list[float]]
        Access values via `self.height[x][y]`
    """

    def __init__(self, size_x: int, size_y: int) -> None:
        """Initialise heightmap to zero."""
        self.size_x = size_x
        self.size_y = size_y
        self.map_depth = self.size_x + self.size_y
        self.heightmap = [[0 for _x in range(self.size_x)] for _y in range(self.size_y)]

    def perturb(self, particles: int, max_slope: int) -> None:
        """
        Perturb the heightmap.

        Drop particles at a random point, then move each particle to a
        random downhill neighbour location until the heightmap is 'stable'.

        Parameters
        ----------
        particles: int
            Number of particles
        max_slope: int
            Maximum stable height difference between adjacent locations.
            Particle will be moved downhill if this is exceeded.
        """
        drop_location = self._get_random_location()
        self.heightmap[drop_location.x][drop_location.y] += particles

        cycle = True
        while cycle is True:
            particle_moved_this_land_cycle = False

            for x in range(self.size_x):
                for y in range(self.size_y):
                    height = self.heightmap[x][y]
                    random.shuffle(NEIGHBOUR_OFFSETS)

                    for offset in NEIGHBOUR_OFFSETS:
                        neighbour = Location(x + offset[0], y + offset[1])

                        if self._in_bounds(neighbour):
                            neighbour_height = self.heightmap[neighbour.x][neighbour.y]
                            if height > neighbour_height + max_slope:
                                self.heightmap[x][y] -= 1
                                self.heightmap[neighbour.x][neighbour.y] += 1
                                particle_moved_this_land_cycle = True

            if not particle_moved_this_land_cycle:
                break

    def _in_bounds(self, location: Location) -> bool:
        """Determine whether `location` is within the heightmap."""
        return 0 <= location.x < self.size_x and 0 <= location.y < self.size_y

    def _get_random_location(self) -> Location:
        """Get a random location on the heightmap."""
        # never returns an edge node
        return Location(
            random.randint(1, self.size_x - 1),
            random.randint(1, self.size_y - 1),
        )

    def normalise(self) -> None:
        """Lowers the whole heightmap so that its lowest point is at zero height."""
        lowest_height = min([min(row) for row in self.heightmap])
        if lowest_height > 0:
            for index_x in range(self.size_x):
                for index_y in range(self.size_y):
                    self.heightmap[index_x][index_y] -= lowest_height
