import math
import random
import pygame
import pygame.gfxdraw

import colors


class Terrain:
    def __init__(self, map_size_x, map_size_y):
        self.map_size_x = map_size_x
        self.map_size_y = map_size_y
        self.map_depth = map_size_x + map_size_y + 2
        self.map_grid = [[0 for _x in range(self.map_size_x+1)] for _y in range(self.map_size_y+1)]

    def perturb(self):
        particles_per_drop = 32
        drop_index_x, drop_index_y = self.get_random_pos()
        self.map_grid[drop_index_x][drop_index_y] += particles_per_drop
        neighbour_offsets = ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))
        neigbour_weightings = (1/math.sqrt(2), 1, 1/math.sqrt(2), 1, 1/math.sqrt(2), 1, 1/math.sqrt(2), 1)

        cycle = True
        while cycle is True:
            particle_moved = False
            for index_x in range(self.map_size_x):
                for index_y in range(self.map_size_y):
                    [neigbour_choice] = random.choices(neighbour_offsets, neigbour_weightings)
                    current_cell_height = self.map_grid[index_x][index_y]
                    print(neigbour_choice)
                    try:
                        neighbour_cell_height = self.map_grid[index_x + neigbour_choice[0]][index_y + neigbour_choice[1]]
                        if current_cell_height > neighbour_cell_height + 1:
                            self.map_grid[index_x + neigbour_choice[0]][index_y + neigbour_choice[1]] += 1
                            self.map_grid[index_x][index_y] -= 1
                            particle_moved = True
                    except IndexError:
                        break
            if particle_moved is False:
                break

    def get_random_pos(self):
        # never returns an edge cell
        return random.randint(1, self.map_size_x - 2), random.randint(1, self.map_size_y - 2)

    def normalise(self):
        lowest_height_value = min([min(row) for row in self.map_grid])
        print("lowest: " + str(lowest_height_value))
        if lowest_height_value > 0:
            for index_x in range(self.map_size_x):
                for index_y in range(self.map_size_y):
                   self.map_grid[index_x][index_y] -= 1


def depth_shade(base_color, depth):
    r, g, b = base_color
    r = int(r + (255 - r) * depth * 0.5)
    g = int(g + (255 - g) * depth * 0.5)
    b = int(b + (255 - b) * depth * 0.65)
    return r, g, b


class Tiler:
    def __init__(self):
        map_size_cells = (16, 16)  # 8, 8
        self.terrain = Terrain(map_size_cells[0]+1, map_size_cells[1]+1)
        self.tile_size = 32  # 60
        self.terrain_height_scale = 0.71
        self.world_size = (self.terrain.map_size_x-1, self.terrain.map_size_y-1) * self.tile_size
        self.perturbs_per_update = 1
        self.max_perturbs = 40
        self.sea_height = 3

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
        self.terrain.normalise()
        self.render_frame()

    def update(self):
        pass

    def render_frame(self):
        self.screen.fill(colors.BACKGROUND)
        self.draw_floor()
        for index_x in range(self.terrain.map_size_x-1):
            for index_y in range(self.terrain.map_size_y-1):
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

    def draw_floor(self):
        world_max_x = self.world_size[0] * self.tile_size
        world_max_y = self.world_size[1] * self.tile_size
        world_pointlist = [(0, 0),
                         (world_max_x, 0),
                         (world_max_x, world_max_y),
                         (0, world_max_y),
                         (0, 0)]
        screen_pointlist = []

        for world_x, world_y in world_pointlist:
            screen_pointlist.append(self.camera(world_x, world_y, -1))
        pygame.draw.polygon(self.screen, colors.WORLD_EDGES, screen_pointlist)


    def draw_tile(self, index_x, index_y):
        local_offsets = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
        heights_at_offsets = []
        terrain_pointlist_screen = []
        sea_pointlist_screen = []

        for offset_x, offset_y in local_offsets:
            world_x, world_y = index_x * self.tile_size, index_y * self.tile_size
            map_height = self.terrain.map_grid[index_x+offset_x][index_y+offset_y]
            heights_at_offsets.append(map_height)
            world_terrain_height = - map_height * self.tile_size / 2
            world_sea_height = - self.sea_height * self.tile_size / 2
            terrain_pointlist_screen.append(self.camera(offset_x * self.tile_size + world_x, offset_y * self.tile_size + world_y, world_terrain_height))
            sea_pointlist_screen.append(self.camera(offset_x * self.tile_size + world_x, offset_y * self.tile_size + world_y, world_sea_height))

        current_map_depth = self.terrain.map_depth - (index_y + index_x)

        if max(heights_at_offsets) <= self.sea_height:
            # seabed
            pygame.draw.polygon(self.screen, depth_shade(colors.SEABED, current_map_depth / self.terrain.map_depth),
                                terrain_pointlist_screen)  # fill
            pygame.draw.polygon(self.screen, colors.SEABED_GRID, terrain_pointlist_screen, 1)  # border
            # sea surface
            pygame.draw.polygon(self.screen, depth_shade(colors.SEA, current_map_depth / self.terrain.map_depth),
                                 sea_pointlist_screen)  # fill
            pygame.draw.polygon(self.screen, colors.SEA_GRID, sea_pointlist_screen, 1)  # border

        else:
            pygame.draw.polygon(self.screen, depth_shade(colors.GRASS, current_map_depth / self.terrain.map_depth),
                                terrain_pointlist_screen)  # fill
            pygame.draw.polygon(self.screen, colors.GRASS_GRID, terrain_pointlist_screen, 1)  # border



if __name__ == "__main__":
    demo = Tiler()
    demo.run()
