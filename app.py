"""App class."""

import math
from typing import Tuple

import pygame

import colors
from heightmap import Heightmap
from tile import Tile

# Heightmap
PERTURBS = 10
PARTICLES_PER_PERTURB = 128
MAX_SLOPE = 1

# Rendering
TILE_SIZE_PX = 30
HEIGHT_SCALE = 1 / math.sqrt(2)
PERTURBS_PER_DISPLAY_UPDATE = 1
SEA_HEIGHT = 3

# Window
WINDOW_BOTTOM_MARGIN = 100


class App:
    """Application class.

    Attributes
    ----------
    window_size: Tuple[int, int]
    landscape_size_tiles: Tuple[int, int]
    heightmap: Heightmap

    """

    def __init__(
        self,
        window_size: Tuple[int, int],
        landscape_size_tiles: Tuple[int, int],
    ) -> None:
        self.window_size = window_size
        self.landscape_size_tiles = landscape_size_tiles

        self.heightmap = Heightmap(
            self.landscape_size_tiles[0] + 1,
            self.landscape_size_tiles[1] + 1,
            # heightmap applies to vertices
        )
        self._perturbs_counter = 0

        # initialize pygame
        pygame.init()
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Demo")

        self.fps_clock = pygame.time.Clock()
        self.running = True

    def run(self) -> None:
        """Run the App."""
        while self.running:
            self._main_loop()

    def _main_loop(self) -> None:
        """Continues to run after landscape is complete, so window does not close."""
        self._handle_input()
        if self._perturbs_counter < PERTURBS:
            for _ in range(PERTURBS_PER_DISPLAY_UPDATE):
                if self._perturbs_counter < PERTURBS:
                    self.heightmap.perturb(
                        particles=PARTICLES_PER_PERTURB,
                        max_slope=MAX_SLOPE,
                    )
                    self._perturbs_counter += 1
        self.heightmap.normalise()
        self._render()

    def _render(self) -> None:
        self.window.fill(colors.BACKGROUND)
        self._render_floor()
        for index_x in range(self.landscape_size_tiles[0]):
            for index_y in range(self.landscape_size_tiles[1]):
                tile = Tile(
                    surface=self.window,
                    size_px=TILE_SIZE_PX,
                    heightmap=self.heightmap,
                    index_x=index_x,
                    index_y=index_y,
                    height_scale=HEIGHT_SCALE,
                    sea_height=SEA_HEIGHT,
                )
                tile.render()

        # limit fps
        self.fps_clock.tick(10)

        # update window
        pygame.display.update()

    def _handle_input(self) -> None:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                print("Quit event")
                break

            # KEYBOARD
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.running = False
                    print("Quit via keypress")

    def _render_floor(self) -> None:
        """Draw a single landscape-sized quad at height zero."""
        grid_points = [
            (0, 0),
            (self.landscape_size_tiles[0], 0),
            (self.landscape_size_tiles[0], self.landscape_size_tiles[1]),
            (0, self.landscape_size_tiles[1]),
            (0, 0),
        ]
        screen_points = [
            self._grid_xyz_to_window_xy(x, y)
            for x, y in grid_points
        ]
        pygame.draw.polygon(self.window, colors.WORLD_EDGES, screen_points)

    def _grid_xyz_to_window_xy(
        self,
        grid_x: int,
        grid_y: int,
        grid_z: int = 0,
    ) -> Tuple[float, float]:
        """Convert grid (x, y, z) index coordinate to window (x, y) pixel coordinate."""
        return self._world_xyz_to_window_xy(
            world_x=grid_x * TILE_SIZE_PX,
            world_y=grid_y * TILE_SIZE_PX,
            world_z=grid_z,
        )

    def _world_xyz_to_window_xy(
        self,
        world_x: float,
        world_y: float,
        world_z: float = 0,
    ) -> Tuple[float, float]:
        """Convert world (x, y, z) pixel coordinate to window (x, y) pixel coordinate.

        Uses 'video game isometric' projection, i.e. dimetric projection with a 2:1
        pixel ratio.
        """
        display_x = (world_x - world_y) / math.sqrt(2)
        display_y = (world_x + world_y) / math.sqrt(2) / 2

        display_x += +self.window_size[0] / 2  # centre horizontally in window

        display_y += WINDOW_BOTTOM_MARGIN
        display_y += world_z * HEIGHT_SCALE

        return display_x, display_y
