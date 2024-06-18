"""App class."""

import logging

import pygame

import colors
from heightmap import Heightmap
from renderer import Renderer

# Heightmap generation parameters
PERTURBS = 10
PARTICLES_PER_PERTURB = 128
MAX_SLOPE = 1

# Rendering
PERTURBS_PER_DISPLAY_UPDATE = 1

CORNER_OFFSETS = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]


class App:
    """Application class.

    Attributes
    ----------
    window_size: Tuple[int, int]
    landscape_size_tiles: Tuple[int, int]
    """

    def __init__(
        self,
        window_size: tuple[int, int],
        landscape_size_tiles: tuple[int, int],
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

        renderer = Renderer(
            surface=self.window,
            heightmap=self.heightmap,
        )
        self.window.fill(colors.BACKGROUND)
        renderer.render()
        # limit fps
        self.fps_clock.tick(10)

        # update window
        pygame.display.update()

    def _handle_input(self) -> None:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                logging.info("Quit event.")
                break

            # KEYBOARD
            if event.type == pygame.KEYDOWN and event.key in {
                pygame.K_ESCAPE,
                pygame.K_q,
            }:
                self.running = False
                logging.info("Quit via keypress.")
