"""Renderer class."""

import math

import pygame

import colors
from camera import isometric_projection
from heightmap import Heightmap
from tile_renderer import TileRenderer

# Rendering
TILE_SIZE_PX = 30
HEIGHT_SCALE = 1 / math.sqrt(2)
SEA_HEIGHT = 3

# Window
WINDOW_TOP_MARGIN = 100

CORNER_OFFSETS = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]


class Renderer:
    """Renders the landscape to a pygame Surface.

    Attributes
    ----------
    surface: pygame.Surface
    heightmap: Heightmap
    """

    def __init__(
        self,
        surface: pygame.Surface,
        heightmap: Heightmap,
    ) -> None:
        self.surface = surface
        self.heightmap = heightmap

    def render(self) -> None:
        """Render the landscape."""
        self._render_floor()
        for index_x in range(self.heightmap.size_x - 1):
            for index_y in range(self.heightmap.size_y - 1):
                tile = TileRenderer(
                    surface=self.surface,
                    size_px=TILE_SIZE_PX,
                    heightmap=self.heightmap,
                    index_x=index_x,
                    index_y=index_y,
                    height_scale=HEIGHT_SCALE,
                    sea_height=SEA_HEIGHT,
                )
                tile.render()

    def _render_floor(self) -> None:
        grid_points = [
            (
                x * (self.heightmap.size_x - 1),
                y * (self.heightmap.size_y - 1),
            )
            for x, y in CORNER_OFFSETS
        ]
        screen_points = [
            isometric_projection(
                world_x=x * TILE_SIZE_PX,
                world_y=y * TILE_SIZE_PX,
                world_z=0,
                display_x_offset=self.surface.get_width() / 2,
                display_y_offset=WINDOW_TOP_MARGIN,
                scale_z=HEIGHT_SCALE,
            )
            for x, y in grid_points
        ]
        pygame.draw.polygon(self.surface, colors.WORLD_EDGES, screen_points)
