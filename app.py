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


class App:
    """Application class.

    Attributes
    ----------
    window_size: Tuple[int, int]
    landscape_size_tiles: Tuple[int, int]
    tile_size_px: int
    height_scale: float
    heightmap: Heightmap

    """

    def __init__(
        self,
        window_size: Tuple[int, int],
        landscape_size_tiles: Tuple[int, int],
    ) -> None:
        self.window_size = window_size
        self.landscape_size_tiles = landscape_size_tiles
        self.tile_size_px = TILE_SIZE_PX
        self.height_scale = HEIGHT_SCALE

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
        self._render_frame()

    def _render_frame(self) -> None:
        self.window.fill(colors.BACKGROUND)
        self._draw_floor()
        for index_x in range(self.landscape_size_tiles[0]):
            for index_y in range(self.landscape_size_tiles[1]):
                tile = Tile(
                    surface=self.window,
                    size_px=self.tile_size_px,
                    heightmap=self.heightmap,
                    height_scale=self.height_scale,
                    sea_height=SEA_HEIGHT,
                )
                tile.render(index_x, index_y)

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

    def _camera(
        self,
        world_x: float,
        world_y: float,
        world_height: float = 0,
    ) -> Tuple[float, float]:
        screen_x = (world_x - world_y) / math.sqrt(2) + self.window_size[0] / 2
        screen_y = (world_x + world_y) / math.sqrt(2) / 2 + 100
        screen_y += world_height * self.height_scale
        # screen_x = int(screen_x)
        # screen_y = int(screen_y)
        return screen_x, screen_y

    def _draw_floor(self) -> None:
        world_max_x = self.landscape_size_tiles[0] * self.tile_size_px
        world_max_y = self.landscape_size_tiles[1] * self.tile_size_px
        world_pointlist = [
            (0, 0),
            (world_max_x, 0),
            (world_max_x, world_max_y),
            (0, world_max_y),
            (0, 0),
        ]
        screen_pointlist = []

        for world_x, world_y in world_pointlist:
            screen_pointlist.append(self._camera(world_x, world_y))
        pygame.draw.polygon(self.window, colors.WORLD_EDGES, screen_pointlist)
