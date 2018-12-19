import math
import pygame
import pygame.gfxdraw

import colors


class Tiler:
    def __init__(self):
        # initialize pygame
        pygame.init()
        self.screen_width = 700
        self.screen_height = 480
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Tiler')
        self.map_size = (8, 8)
        self.tile_size = 60

        self.fps_clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.main_loop()

    def main_loop(self):
        self.handle_input()
        self.render_frame()

    def update(self):
        pass

    def render_frame(self):
        self.screen.fill(colors.BACKGROUND)
        pygame.draw.rect(self.screen, colors.RED, ((0, 0), (self.tile_size, self.tile_size)))
        # pygame.draw.rect(self.screen, colors.RED, ((100, 100), (self.tile_size, self.tile_size)))

        for x in range(self.map_size[0]):
            for y in range(self.map_size[1]):
                world_x, world_y = x * self.tile_size, y * self.tile_size
                self.draw_tile(world_x, world_y)

        # limit fps
        self.fps_clock.tick(60)

        # update screen
        pygame.display.update()

    def handle_input(self):
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                print("quit")
                break

            # KEYBOARD
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.running = False
                    print("quit")

    def camera(self, world_x, world_y):
        screen_x = (world_x + world_y) / math.sqrt(2)
        screen_y = (world_y - world_x) / math.sqrt(2) / 2 + self.screen_height / 2
        return screen_x, screen_y

    def draw_tile(self, world_x, world_y):
        local_offsets = [(0, 0),
                     (self.tile_size, 0),
                     (self.tile_size, self.tile_size),
                     (0, self.tile_size),
                     (0, 0)]
        iso_pointlist =[]

        for local_x, local_y in local_offsets:
            iso_pointlist.append(self.camera(local_x + world_x, local_y + world_y))
        pygame.draw.polygon(self.screen, colors.FOREGROUND, iso_pointlist, 0) # fill
        pygame.draw.polygon(self.screen, colors.BLACK, iso_pointlist, 1) #border
        # pygame.draw.rect(self.screen, colors.BLUE, (self.camera(pos_x, pos_y), (4,4))) #origin


if __name__ == "__main__":
    demo = Tiler()
    demo.run()
