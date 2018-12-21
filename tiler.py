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
        self.world_size = self.map_size * self.tile_size

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

        for index_x in range(self.map_size[0]):
            for index_y in range(self.map_size[1]):
                self.draw_tile(index_x, index_y)

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
        screen_x = (world_x - world_y) / math.sqrt(2) + self.screen_width / 2
        screen_y = (world_x + world_y) / math.sqrt(2) / 2 + 100
        return screen_x, screen_y

    def draw_tile(self, index_x, index_y):
        local_offsets = [(0, 0),
                     (self.tile_size, 0),
                     (self.tile_size, self.tile_size),
                     (0, self.tile_size),
                     (0, 0)]
        iso_pointlist =[]

        for local_x, local_y in local_offsets:
            world_x, world_y = index_x * self.tile_size, index_y * self.tile_size
            iso_pointlist.append(self.camera(local_x + world_x, local_y + world_y))

        r, g, b = colors.GREEN
        total_grid_depth = self.map_size[0] + self.map_size[1] -2

        current_grid_depth = total_grid_depth - (index_y + index_x)
        # r = int(r + (255-r) * current_grid_depth/total_grid_depth)
        # g = int(g + (255-g) * current_grid_depth/total_grid_depth)
        # b = int(b + (255-b) * current_grid_depth/total_grid_depth)
        color_shade = (r, g, b)
        print(color_shade)

        pygame.draw.polygon(self.screen, color_shade, iso_pointlist, 0) # fill
        pygame.draw.polygon(self.screen, colors.BLACK, iso_pointlist, 1)  # border
        # pygame.draw.rect(self.screen, colors.BLUE, (self.camera(world_x, world_y), (4,4)))  # origin marker
        label_font = pygame.font.SysFont("monospace", 12)
        # label_text = str(index_x) + ', ' + str(index_y)
        label_text = str(current_grid_depth)
        tile_label = label_font.render(label_text, 1, colors.YELLOW, colors.BACKGROUND)
        # TO DO: is it right to blit this here?
        self.screen.blit(tile_label, self.camera(world_x, world_y))



if __name__ == "__main__":
    demo = Tiler()
    demo.run()
