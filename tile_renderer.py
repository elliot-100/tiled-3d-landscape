"""Tile class."""

import pygame

import colors
from camera import isometric_projection


class TileRenderer:
    """Renders a single Tile to a pygame Surface.

    Attributes
    ----------
    surface: pygame.Surface
    size_px: int
    index_x: int
    index_y: int
    height_scale: float
    sea_height: int
    """

    def __init__(
        self,
        surface: pygame.Surface,
        size_px: int,
        depth: float,
        heights_at_corners: dict[tuple[int, int], int],
        index_x: int,
        index_y: int,
        height_scale: float,
        sea_height: int,
    ) -> None:
        self.surface = surface
        self.size_px = size_px
        self.depth = depth
        self.heights_at_corners = heights_at_corners
        self.index_x = index_x
        self.index_y = index_y
        self.height_scale = height_scale
        self.sea_height = sea_height

        self.terrain_pointlist_screen = []
        self.sea_pointlist_screen = []

        for offset, height in heights_at_corners.items():
            world_x, world_y = self.index_x * self.size_px, self.index_y * self.size_px

            world_terrain_height = -height * self.size_px / 2
            world_sea_height = -self.sea_height * self.size_px / 2
            self.terrain_pointlist_screen.append(
                isometric_projection(
                    world_x=offset[0] * self.size_px + world_x,
                    world_y=offset[1] * self.size_px + world_y,
                    world_z=world_terrain_height,
                    display_x_offset=self.surface.get_width() / 2,
                    display_y_offset=100,
                    scale_z=self.height_scale,
                ),
            )
            self.sea_pointlist_screen.append(
                isometric_projection(
                    world_x=offset[0] * self.size_px + world_x,
                    world_y=offset[1] * self.size_px + world_y,
                    world_z=world_sea_height,
                    display_x_offset=self.surface.get_width() / 2,
                    display_y_offset=100,
                    scale_z=self.height_scale,
                ),
            )

    @property
    def is_underwater(self) -> bool:
        """Determine if the tile is underwater.
        True if no corners are above sea level.
        """
        return max(self.heights_at_corners.values()) <= self.sea_height

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
                self.depth,
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
                self.depth,
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
                self.depth,
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
        base_color: tuple[int, int, int],
        depth: float,
    ) -> tuple[int, int, int]:
        r, g, b = base_color
        r = int(r + (255 - r) * depth * 0.5)
        g = int(g + (255 - g) * depth * 0.5)
        b = int(b + (255 - b) * depth * 0.65)
        return r, g, b
