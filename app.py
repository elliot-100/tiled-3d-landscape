"""App class."""

import math
from typing import Tuple

import pygame

import colors
from heightmap import Heightmap

PARTICLES_PER_DROP = 128
MAX_SLOPE = 1


class App:
    """Application class."""

    def __init__(self) -> None:
        map_size_cells = (16, 16)  # 8, 8
        self.map_size_cells = map_size_cells
        self.terrain = Heightmap(map_size_cells[0] + 1, map_size_cells[1] + 1)
        self.tile_size = 30  # 60
        self.terrain_height_scale = 1 / math.sqrt(2)
        self.perturbs_per_update = 1
        self.max_perturbs = 10
        self.sea_height = 3

        self.perturbs_counter = 0

        # initialize pygame
        pygame.init()
        self.screen_width = 700
        self.screen_height = 480
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Demo")

        self.fps_clock = pygame.time.Clock()
        self.running = True

    def run(self) -> None:
        """Run the App."""
        while self.running:
            self._main_loop()

    def _main_loop(self) -> None:
        self._handle_input()
        if self.perturbs_counter < self.max_perturbs:
            for _ in range(self.perturbs_per_update):
                if self.perturbs_counter < self.max_perturbs:
                    self.terrain.perturb(
                        particles=PARTICLES_PER_DROP,
                        max_slope=MAX_SLOPE,
                    )
                    self.perturbs_counter += 1
        self.terrain.normalise()
        self._render_frame()

    def _render_frame(self) -> None:
        self.screen.fill(colors.BACKGROUND)
        self._draw_floor()
        for index_x in range(self.map_size_cells[0]):
            for index_y in range(self.map_size_cells[1]):
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
        screen_x = (world_x - world_y) / math.sqrt(2) + self.screen_width / 2
        screen_y = (world_x + world_y) / math.sqrt(2) / 2 + 100
        screen_y += world_height * self.terrain_height_scale
        # screen_x = int(screen_x)
        # screen_y = int(screen_y)
        return screen_x, screen_y

    def _draw_floor(self) -> None:
        world_max_x = self.map_size_cells[0] * self.tile_size
        world_max_y = self.map_size_cells[1] * self.tile_size
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
            world_x, world_y = index_x * self.tile_size, index_y * self.tile_size
            map_height = self.terrain.heightmap[index_x + offset_x][index_y + offset_y]
            heights_at_offsets.append(map_height)
            world_terrain_height = -map_height * self.tile_size / 2
            world_sea_height = -self.sea_height * self.tile_size / 2
            terrain_pointlist_screen.append(
                self._camera(
                    offset_x * self.tile_size + world_x,
                    offset_y * self.tile_size + world_y,
                    world_terrain_height,
                )
            )
            sea_pointlist_screen.append(
                self._camera(
                    offset_x * self.tile_size + world_x,
                    offset_y * self.tile_size + world_y,
                    world_sea_height,
                )
            )

        current_map_depth = self.terrain.map_depth - (index_y + index_x)

        if max(heights_at_offsets) <= self.sea_height:
            # draw seabed quad
            pygame.draw.polygon(
                self.screen,
                self._depth_shade(
                    colors.SEABED, current_map_depth / self.terrain.map_depth
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
                    colors.SEA, current_map_depth / self.terrain.map_depth
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
                    colors.GRASS, current_map_depth / self.terrain.map_depth
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
