import math
import random
import pygame
import pygame.gfxdraw

import colors


class Terrain:
    def __init__(self, map_size_x, map_size_y):
        self.map_size_x = map_size_x
        self.map_size_y = map_size_y
        self.map_grid = [[0 for _x in range(self.map_size_x)] for _y in range(self.map_size_y)]

    def perturb(self):
        particles_per_drop = 80
        drop_index_x, drop_index_y = self.get_random_pos()
        self.map_grid[drop_index_x][drop_index_y] += particles_per_drop
        neighbour_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        cycle = True
        while cycle is True:
            particle_moved = False
            for index_x in range(self.map_size_x):
                for index_y in range(self.map_size_y):
                    random.shuffle(neighbour_offsets)
                    for offset in neighbour_offsets:
                        current_cell_height = self.map_grid[index_x][index_y]
                        try:
                            neighbour_cell_height = self.map_grid[index_x + offset[0]][index_y + offset[1]]
                            if current_cell_height > neighbour_cell_height + 1:
                                self.map_grid[index_x + offset[0]][index_y + offset[1]] += 1
                                self.map_grid[index_x][index_y] -= 1
                                particle_moved = True
                        except IndexError:
                            break
            if particle_moved is False:
                break

    def get_random_pos(self):
        # never returns an edge cell
        return random.randint(1, self.map_size_x - 2), random.randint(1, self.map_size_y - 2)


class Tiler:
    def __init__(self):
        self.terrain = Terrain(16, 16)
        self.tile_size = 32 # 60
        self.terrain_height_scale = 0.5
        self.world_size = (self.terrain.map_size_x, self.terrain.map_size_y) * self.tile_size
        self.perturbs_per_update = 1
        self.max_perturbs = 12

        self.perturbs_counter = 0

        # initialize pygame
        pygame.init()
        self.screen_width = 700
        self.screen_height = 480
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Tiler')

        self.fps_clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.main_loop()

    def main_loop(self):
        self.handle_input()
        if self.perturbs_counter < self.max_perturbs:
            for _ in range(self.perturbs_per_update):
                if self.perturbs_counter < self.max_perturbs:
                    self.terrain.perturb()
                    self.perturbs_counter += 1
        self.render_frame()

    def update(self):
        pass

    def render_frame(self):
        self.screen.fill(colors.BACKGROUND)

        for index_x in range(self.terrain.map_size_x):
            for index_y in range(self.terrain.map_size_y):
                self.draw_tile(index_x, index_y)

        # limit fps
        self.fps_clock.tick(10)

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

    def camera(self, world_x, world_y, world_height=0):
        screen_x = (world_x - world_y) / math.sqrt(2) + self.screen_width / 2
        screen_y = (world_x + world_y) / math.sqrt(2) / 2 + 100
        screen_y += world_height * self.terrain_height_scale
        # screen_x = int(screen_x)
        # screen_y = int(screen_y)
        return screen_x, screen_y

    def draw_tile(self, index_x, index_y):
        local_offsets = [(0, 0),
                         (self.tile_size, 0),
                         (self.tile_size, self.tile_size),
                         (0, self.tile_size),
                         (0, 0)]
        iso_pointlist = []

        for local_x, local_y in local_offsets:
            world_x, world_y = index_x * self.tile_size, index_y * self.tile_size
            world_height = -self.terrain.map_grid[index_x][index_y] * self.tile_size / 2
            iso_pointlist.append(self.camera(local_x + world_x, local_y + world_y, world_height))

        r, g, b = colors.GREEN
        total_grid_depth = self.terrain.map_size_x + self.terrain.map_size_y - 2

        current_grid_depth = total_grid_depth - (index_y + index_x)
        r = int(r + (255 - r) * current_grid_depth / total_grid_depth * 0.7)
        g = int(g + (255 - g) * current_grid_depth / total_grid_depth * 0.7)
        b = int(b + (255 - b) * current_grid_depth / total_grid_depth * 0.7)
        color_shade = (r, g, b)
        # print(color_shade)

        pygame.draw.polygon(self.screen, color_shade, iso_pointlist, 0)  # fill
        pygame.draw.polygon(self.screen, colors.BACKGROUND, iso_pointlist, 1)  # border
        # pygame.draw.line(self.screen, colors.BLACK, iso_pointlist[1], iso_pointlist[2], 1)  # border
        # pygame.draw.line(self.screen, colors.BLACK, iso_pointlist[2], iso_pointlist[3], 1)  # border
        # pygame.draw.rect(self.screen, colors.BLUE, (self.camera(world_x, world_y), (4,4)))  # origin marker
        # label_font = pygame.font.SysFont("monospace", 12)
        # label_text = str(index_x) + ', ' + str(index_y)
        # label_text = str(current_grid_depth)
        # label_text = str(self.terrain.map_grid[index_x][index_y])
        # tile_label = label_font.render(label_text, 1, colors.YELLOW, colors.BACKGROUND)
        # TO DO: is it right to blit this here?
        # text_pos = self.camera(world_x, world_y, world_height)
        # offset text labels
        # tp_list = list(text_pos)
        # tp_list[1] += self.tile_size/4
        # self.screen.blit(tile_label, tp_list)


if __name__ == "__main__":
    demo = Tiler()
    demo.run()
