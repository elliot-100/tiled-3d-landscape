"""App class."""

import math
from typing import Tuple

import pygame

import colors
from heightmap import Heightmap

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
        self.screen = pygame.display.set_mode(self.window_size)
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
        self.screen.fill(colors.BACKGROUND)
        self._draw_floor()
        for index_x in range(self.landscape_size_tiles[0]):
            for index_y in range(self.landscape_size_tiles[1]):
                self._draw_tile(index_x, index_y)

        # limit fps
        self.fps_clock.tick(10)

        # update screen
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
        pygame.draw.polygon(self.screen, colors.WORLD_EDGES, screen_pointlist)

    def _draw_tile(self, index_x: int, index_y: int) -> None:
        """Draws a single tile."""
        local_offsets = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]

        heights_at_offsets = []
        terrain_pointlist_screen = []
        sea_pointlist_screen = []

        for offset_x, offset_y in local_offsets:
            world_x, world_y = index_x * self.tile_size_px, index_y * self.tile_size_px
            map_height = self.heightmap.heightmap[index_x + offset_x][
                index_y + offset_y
            ]
            heights_at_offsets.append(map_height)
            world_terrain_height = -map_height * self.tile_size_px / 2
            world_sea_height = -SEA_HEIGHT * self.tile_size_px / 2
            terrain_pointlist_screen.append(
                self._camera(
                    offset_x * self.tile_size_px + world_x,
                    offset_y * self.tile_size_px + world_y,
                    world_terrain_height,
                )
            )
            sea_pointlist_screen.append(
                self._camera(
                    offset_x * self.tile_size_px + world_x,
                    offset_y * self.tile_size_px + world_y,
                    world_sea_height,
                )
            )

        current_map_depth = self.heightmap.map_depth - (index_y + index_x)

        if max(heights_at_offsets) <= SEA_HEIGHT:
            # draw seabed quad
            pygame.draw.polygon(
                self.screen,
                self._depth_shade(
                    colors.SEABED, current_map_depth / self.heightmap.map_depth
                ),
                terrain_pointlist_screen,
            )  # fill
            pygame.draw.polygon(
                self.screen, colors.SEABED_GRID, terrain_pointlist_screen, 1
            )  # border
            # draw sea surface quad
            pygame.draw.polygon(
                self.screen,
                self._depth_shade(
                    colors.SEA, current_map_depth / self.heightmap.map_depth
                ),
                sea_pointlist_screen,
            )  # fill
            pygame.draw.polygon(
                self.screen, colors.SEA_GRID, sea_pointlist_screen, 1
            )  # border

        else:
            # draw land quad
            pygame.draw.polygon(
                self.screen,
                self._depth_shade(
                    colors.GRASS, current_map_depth / self.heightmap.map_depth
                ),
                terrain_pointlist_screen,
            )  # fill
            pygame.draw.polygon(
                self.screen, colors.GRASS_GRID, terrain_pointlist_screen, 1
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
