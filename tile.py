"""Tile class."""

from typing import Tuple

import pygame

import colors
from camera import camera
from heightmap import Heightmap

CORNER_OFFSETS = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]


class Tile:
    """Represents a single Landscape tile.

    Attributes
    ----------
    surface: pygame.Surface
    size_px: int
    heightmap: Heightmap
    index_x: int
    index_y: int
    height_scale: float
    sea_height: int
    """

    def __init__(
        self,
        surface: pygame.Surface,
        size_px: int,
        heightmap: Heightmap,
        index_x: int,
        index_y: int,
        height_scale: float,
        sea_height: int,
    ) -> None:
        self.surface = surface
        self.size_px = size_px
        self.heightmap = heightmap
        self.index_x = index_x
        self.index_y = index_y
        self.height_scale = height_scale
        self.sea_height = sea_height

        self.heights_at_corners = []
        self.terrain_pointlist_screen = []
        self.sea_pointlist_screen = []

        for offset_x, offset_y in CORNER_OFFSETS:
            world_x, world_y = self.index_x * self.size_px, self.index_y * self.size_px
            map_height = self.heightmap.heightmap[self.index_x + offset_x][
                self.index_y + offset_y
            ]
            self.heights_at_corners.append(map_height)

            world_terrain_height = -map_height * self.size_px / 2
            world_sea_height = -self.sea_height * self.size_px / 2
            self.terrain_pointlist_screen.append(
                camera(
                    world_x=offset_x * self.size_px + world_x,
                    world_y=offset_y * self.size_px + world_y,
                    world_height=world_terrain_height,
                    window_width=self.surface.get_width(),
                    height_scale=self.height_scale,
                ),
            )
            self.sea_pointlist_screen.append(
                camera(
                    world_x=offset_x * self.size_px + world_x,
                    world_y=offset_y * self.size_px + world_y,
                    world_height=world_sea_height,
                    window_width=self.surface.get_width(),
                    height_scale=self.height_scale,
                ),
            )

        self.current_map_depth = self.heightmap.map_depth - (
            self.index_y + self.index_x
        )

    @property
    def is_underwater(self) -> bool:
        """Determine if the tile is underwater.
        True if no corners are above sea level.
        """
        return max(self.heights_at_corners) <= self.sea_height

    def render(self) -> None:
        """Render the Tile to the Pygame surface."""
        if self.is_underwater:
            self._render_seabed_quad()
            self._render_sea_surface_quad()
        else:
            self._render_land_quad()

    def _render_seabed_quad(self) -> None:
        pygame.draw.polygon(
            self.surface,
            self._depth_shade(
                colors.SEABED,
                self.current_map_depth / self.heightmap.map_depth,
            ),
            self.terrain_pointlist_screen,
        )  # fill
        pygame.draw.polygon(
            self.surface,
            colors.SEABED_GRID,
            self.terrain_pointlist_screen,
            1,
        )  # border

    def _render_sea_surface_quad(self) -> None:
        pygame.draw.polygon(
            self.surface,
            self._depth_shade(
                colors.SEA_SURFACE,
                self.current_map_depth / self.heightmap.map_depth,
            ),
            self.sea_pointlist_screen,
        )  # fill
        pygame.draw.polygon(
            self.surface,
            colors.SEA_SURFACE_GRID,
            self.sea_pointlist_screen,
            1,
        )  # border

    def _render_land_quad(self) -> None:
        pygame.draw.polygon(
            self.surface,
            self._depth_shade(
                colors.GRASS,
                self.current_map_depth / self.heightmap.map_depth,
            ),
            self.terrain_pointlist_screen,
        )  # fill
        pygame.draw.polygon(
            self.surface,
            colors.GRASS_GRID,
            self.terrain_pointlist_screen,
            1,
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
