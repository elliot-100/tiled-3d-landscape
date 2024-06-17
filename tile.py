"""Tile class."""

import math
from typing import Tuple

import pygame

import colors
from camera import camera
from heightmap import Heightmap


class Tile:
    """Represents a single Landscape tile.

    Attributes
    ----------
    surface: pygame.Surface
    size_px: int
    heightmap: Heightmap
    height_scale: float
    sea_height: int
    """

    def __init__(
        self,
        surface: pygame.Surface,
        size_px: int,
        heightmap: Heightmap,
        height_scale: float,
        sea_height: int,
    ) -> None:
        self.surface = surface
        self.size_px = size_px
        self.heightmap = heightmap
        self.height_scale = height_scale
        self.sea_height = sea_height

    def render(self, index_x: int, index_y: int) -> None:
        """Render the Tile."""
        local_offsets = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]

        heights_at_offsets = []
        terrain_pointlist_screen = []
        sea_pointlist_screen = []

        for offset_x, offset_y in local_offsets:
            world_x, world_y = index_x * self.size_px, index_y * self.size_px
            map_height = self.heightmap.heightmap[index_x + offset_x][
                index_y + offset_y
            ]
            heights_at_offsets.append(map_height)
            world_terrain_height = -map_height * self.size_px / 2
            world_sea_height = -self.sea_height * self.size_px / 2
            terrain_pointlist_screen.append(
                camera(
                    world_x=offset_x * self.size_px + world_x,
                    world_y=offset_y * self.size_px + world_y,
                    world_height=world_terrain_height,
                    window_width=self.surface.get_width(),
                    height_scale=self.height_scale,
                )
            )
            sea_pointlist_screen.append(
                camera(
                    world_x=offset_x * self.size_px + world_x,
                    world_y=offset_y * self.size_px + world_y,
                    world_height=world_sea_height,
                    window_width=self.surface.get_width(),
                    height_scale=self.height_scale,
                )
            )

        current_map_depth = self.heightmap.map_depth - (index_y + index_x)

        if max(heights_at_offsets) <= self.sea_height:
            # draw seabed quad
            pygame.draw.polygon(
                self.surface,
                self._depth_shade(
                    colors.SEABED, current_map_depth / self.heightmap.map_depth
                ),
                terrain_pointlist_screen,
            )  # fill
            pygame.draw.polygon(
                self.surface, colors.SEABED_GRID, terrain_pointlist_screen, 1
            )  # border
            # draw sea surface quad
            pygame.draw.polygon(
                self.surface,
                self._depth_shade(
                    colors.SEA, current_map_depth / self.heightmap.map_depth
                ),
                sea_pointlist_screen,
            )  # fill
            pygame.draw.polygon(
                self.surface, colors.SEA_GRID, sea_pointlist_screen, 1
            )  # border

        else:
            # draw land quad
            pygame.draw.polygon(
                self.surface,
                self._depth_shade(
                    colors.GRASS, current_map_depth / self.heightmap.map_depth
                ),
                terrain_pointlist_screen,
            )  # fill
            pygame.draw.polygon(
                self.surface, colors.GRASS_GRID, terrain_pointlist_screen, 1
            )  # border

    @staticmethod
    def _depth_shade(
        base_color: Tuple[int, int, int],
        depth: float,
    ) -> Tuple[int, int, int]:
        r, g, b = base_color
        r = int(r + (255 - r) * depth * 0.5)
        g = int(g + (255 - g) * depth * 0.5)
        b = int(b + (255 - b) * depth * 0.65)
        return r, g, b
