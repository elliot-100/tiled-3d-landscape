import pygame
import pygame.gfxdraw

import colors


class Tiler():
    def __init__(self):
        # initialize pygame
        pygame.init()
        self.screen_width = 640
        self.screen_height = 480
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Tiler')
        self.map_size = (4, 4)
        self.tile_size = 20

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
        for x in range(self.map_size[0]):
            for y in range(self.map_size[1]):
                self.draw_tile(*self.camera(x * self.tile_size, y * self.tile_size))

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



    def camera(self, cart_x, cart_y):
        iso_x = cart_x - cart_y + self.screen_width//2
        iso_y= (cart_x + cart_y) / 2 + self.screen_height//2
        return iso_x, iso_y

    def draw_tile(self, pos_x, pos_y):
        pointlist = [(pos_x - self.tile_size//2, pos_y - self.tile_size//2),
                     (pos_x + self.tile_size//2, pos_y - self.tile_size//2),
                     (pos_x + self.tile_size//2, pos_y + self.tile_size//2),
                     (pos_x - self.tile_size//2, pos_y + self.tile_size//2),
                     (pos_x - self.tile_size // 2, pos_y - self.tile_size//2)]
        pygame.draw.polygon(self.screen, colors.FOREGROUND, pointlist, 1)


if __name__ == "__main__":
    demo = Tiler()
    demo.run()