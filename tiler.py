import math
import random
import pygame

import colors
import tile_shapes

MAP_SIZE_CELLS = (16, 16)  # 8, 8
TILE_SIZE = 30  # 60
SEA_HEIGHT_CELLS = 4  # 4
MIN_HEIGHT_CELLS = 0
BASE_THICKNESS_CELLS = 1

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 480

PERTURBS_PER_UPDATE = 1  # 1
MAX_PERTURBS = 10  # 10

TERRAIN_HEIGHT_SCALE = 1 / math.sqrt(2)

DEPTH_SHADER = True


def camera(world_x, world_y, world_height=0):
    """

    Parameters
    ----------
    world_x
    world_y
    world_height

    Returns
    -------

    """
    screen_x = (world_x - world_y) / math.sqrt(2) + SCREEN_WIDTH / 2
    screen_y = (world_x + world_y) / math.sqrt(2) / 2 + 100
    screen_y += world_height * TERRAIN_HEIGHT_SCALE
    # screen_x = int(screen_x)
    # screen_y = int(screen_y)
    return int(screen_x), int(screen_y)


class Tile:
    """

    """

    def __init__(self, index_x, index_y):
        self.index_x = index_x
        self.index_y = index_y
        self.corner_offsets = [(0, 0), (1, 0), (1, 1), (0, 1)]

        map_depth = terrain.map_depth - (index_y + index_x)
        self.depth_factor = map_depth / terrain.map_depth

        self.absolute_heights = []
        for offset_x, offset_y in self.corner_offsets:
            map_height = terrain.heightmap[self.index_x + offset_x][self.index_y + offset_y]
            self.absolute_heights.append(map_height)

        self.relative_heights = []
        self.relative_heights = self.get_relative_heights()


        self.geometry_type = tile_shapes.geometries[tuple(self.relative_heights)]['type']
        if self.geometry_type in ('flat-low', 'flat-high', 'saddle'):
            self.geometry_tri1 = tile_shapes.geometries[tuple(self.relative_heights)]['tri1']
            self.geometry_tri2 = tile_shapes.geometries[tuple(self.relative_heights)]['tri2']

    def draw(self):
        """

        """
        terrain_pointlist_screen = []
        sea_pointlist_screen = []

        # todo reuse the absolute heights already calculated
        for offset_x, offset_y in self.corner_offsets:
            world_x, world_y = self.index_x * TILE_SIZE, self.index_y * TILE_SIZE
            map_height = terrain.heightmap[self.index_x + offset_x][self.index_y + offset_y]
            world_terrain_height = - map_height * TILE_SIZE / 2
            world_sea_height = - SEA_HEIGHT_CELLS * TILE_SIZE / 2

            terrain_pointlist_screen.append(
                camera(offset_x * TILE_SIZE + world_x, offset_y * TILE_SIZE + world_y,
                       world_terrain_height))

            sea_pointlist_screen.append(
                camera(offset_x * TILE_SIZE + world_x, offset_y * TILE_SIZE + world_y, world_sea_height))

        if self.geometry_type in ('slope', 'flat'):

            is_sea = False
            if max(self.absolute_heights) <= SEA_HEIGHT_CELLS:
                is_sea = True

            if is_sea:
                terrain_fill_color = colors.SEABED
                terrain_grid_color = colors.SEABED_GRID
            else:
                terrain_fill_color = colors.GRASS
                terrain_grid_color = colors.GRASS_GRID

            pygame.draw.polygon(tiler.screen, depth_shade(terrain_fill_color, self.depth_factor),
                                terrain_pointlist_screen)  # fill
            pygame.draw.polygon(tiler.screen, depth_shade(terrain_grid_color, self.depth_factor),
                                terrain_pointlist_screen, 1)  # grid/border

            if is_sea:

                # draw sea surface quad
                pygame.draw.polygon(tiler.screen, depth_shade(colors.SEA, self.depth_factor),
                                   sea_pointlist_screen)  # fill
                pygame.draw.polygon(tiler.screen, colors.SEA_GRID, sea_pointlist_screen, 1)  # border

        elif self.geometry_type == 'flat-low':
            tri1_points = []
            tri2_points = []

            is_sea = False
            if max(self.absolute_heights) <= SEA_HEIGHT_CELLS:
                is_sea = True

            for i in self.geometry_tri1:
                tri1_points.append(terrain_pointlist_screen[i])
            for i in self.geometry_tri2:
                tri2_points.append(terrain_pointlist_screen[i])

            tri1_fill_color = colors.GRASS
            tri2_fill_color = colors.GRASS
            tri1_grid_color = colors.GRASS_GRID
            tri2_grid_color = colors.GRASS_GRID

            if is_sea:
                # flat tri
                tri1_fill_color = colors.SEABED
                tri1_grid_color = colors.SEABED_GRID
                # slope tri
                tri2_fill_color = colors.SEABED
                tri2_grid_color = colors.SEABED_GRID




            # draw flat tri
            pygame.draw.polygon(tiler.screen, depth_shade(tri1_fill_color, self.depth_factor),
                                tri1_points)  # fill
            pygame.draw.polygon(tiler.screen, depth_shade(tri1_grid_color, self.depth_factor), tri1_points,
                                1)  # border




            # draw slope tri
            pygame.draw.polygon(tiler.screen, depth_shade(tri2_fill_color, self.depth_factor),
                                tri2_points)  # fill
            pygame.draw.polygon(tiler.screen, depth_shade(tri2_grid_color, self.depth_factor), tri2_points,
                                1)  # border
            if is_sea:

                # draw sea surface quad

                pygame.draw.polygon(tiler.screen, depth_shade(colors.SEA, self.depth_factor),
                                  sea_pointlist_screen)  # fill
                pygame.draw.polygon(tiler.screen, colors.SEA_GRID, sea_pointlist_screen, 1)  # border

        elif self.geometry_type == 'flat-high':
            tri1_points = []
            tri2_points = []

            # print('relative_heights_at_offsets: {}'.format(relative_heights_at_offsets))

            for i in self.geometry_tri1:
                tri1_points.append(terrain_pointlist_screen[i])
            for i in self.geometry_tri2:
                tri2_points.append(terrain_pointlist_screen[i])



            tri1_fill_color = colors.GRASS
            tri2_fill_color = colors.GRASS
            tri1_grid_color = colors.GRASS_GRID
            tri2_grid_color = colors.GRASS_GRID

            tri1_is_sea = False
            tri2_is_sea = False
            if min(self.absolute_heights) <= SEA_HEIGHT_CELLS:  # TODO needs improvement
                tri1_is_sea = True
                tri1_fill_color = colors.SEABED
                tri1_grid_color = colors.SEABED_GRID
            if max(self.absolute_heights) <= SEA_HEIGHT_CELLS:  # TODO needs improvement
                tri2_is_sea = True
                tri2_fill_color = colors.SEABED
                tri2_grid_color = colors.SEABED_GRID



            # draw flat tri
            pygame.draw.polygon(tiler.screen, depth_shade(tri1_fill_color, self.depth_factor),
                                tri1_points)  # fill
            pygame.draw.polygon(tiler.screen, depth_shade(tri1_grid_color, self.depth_factor), tri1_points,
                                1)  # border

            if tri1_is_sea and tri2_is_sea is not True:
                print(max(self.absolute_heights), min(self.absolute_heights))
                # draw sea surface quad
                pygame.draw.polygon(tiler.screen, depth_shade(colors.SEA, self.depth_factor),
                                   sea_pointlist_screen)  # fill
                pygame.draw.polygon(tiler.screen, colors.SEA_GRID, sea_pointlist_screen, 1)  # border


            # draw slope tri
            pygame.draw.polygon(tiler.screen, depth_shade(tri2_fill_color, self.depth_factor),
                                tri2_points)  # fill
            pygame.draw.polygon(tiler.screen, depth_shade(tri2_grid_color, self.depth_factor), tri2_points,
                                1)  # border

            if tri1_is_sea and tri2_is_sea:

                # draw sea surface quad
                pygame.draw.polygon(tiler.screen, depth_shade(colors.SEA, self.depth_factor),
                                   sea_pointlist_screen)  # fill
                pygame.draw.polygon(tiler.screen, colors.SEA_GRID, sea_pointlist_screen, 1)  # border


        elif self.geometry_type == 'saddle':
            tri1_points = []
            tri2_points = []

            for i in self.geometry_tri1:
                tri1_points.append(terrain_pointlist_screen[i])

            for i in self.geometry_tri2:
                tri2_points.append(terrain_pointlist_screen[i])

            is_sea = False
            if max(self.absolute_heights) <= SEA_HEIGHT_CELLS:
                is_sea = True
                
            terrain_fill_color = colors.GRASS
            terrain_grid_color = colors.GRASS_GRID

            if max(self.absolute_heights) <= SEA_HEIGHT_CELLS:  # TODO needs improvement

                terrain_fill_color = colors.SEABED
                terrain_grid_color = colors.SEABED_GRID

            # draw tri1

            pygame.draw.polygon(tiler.screen, depth_shade(terrain_fill_color, self.depth_factor),
                                tri1_points)  # fill

            pygame.draw.polygon(tiler.screen, depth_shade(terrain_grid_color, self.depth_factor), tri1_points,
                                1)  # border

            # draw tri2

            pygame.draw.polygon(tiler.screen, depth_shade(terrain_fill_color, self.depth_factor),
                                tri2_points)  # fill

            pygame.draw.polygon(tiler.screen, depth_shade(terrain_grid_color, self.depth_factor), tri2_points,
                                1)  # border
        else:
            # draw highlighted quad

            pygame.draw.polygon(tiler.screen, depth_shade(colors.RED, self.depth_factor),
                                terrain_pointlist_screen)  # fill
            pygame.draw.polygon(tiler.screen, depth_shade(colors.RED_DARK, self.depth_factor), terrain_pointlist_screen,
                                1)  # border

        # pygame.draw.circle(self.screen, colors.DEBUG, terrain_pointlist_screen[3], 5)


    def get_relative_heights(self):
        """

        Returns
        -------

        """
        lowest = min(self.absolute_heights)
        for h in self.absolute_heights:
            if h > lowest:
                self.relative_heights.append(1)
            else:
                self.relative_heights.append(0)
        return self.relative_heights


class Terrain:
    def __init__(self, heightmap_size_x, heightmap_size_y):
        self.heightmap_size_x = heightmap_size_x
        self.heightmap_size_y = heightmap_size_y
        self.map_depth = self.heightmap_size_x + self.heightmap_size_y
        self.heightmap = [[0 for _x in range(self.heightmap_size_x)] for _y in range(self.heightmap_size_y)]
        print("created terrain data")

    def perturb(self):
        """
        Drop a quantity of particles at a single point on the Terrain object, then move the particles to neighbour cells
        until the terrain is 'stable'.
        """
        particles_per_drop = 128
        drop_index_x, drop_index_y = self.get_random_pos()
        # print('drop at', drop_index_x, drop_index_y)
        self.heightmap[drop_index_x][drop_index_y] += particles_per_drop
        neighbour_offsets = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
        cycle = True
        while cycle is True:
            particle_moved_this_land_cycle = False
            for index_x in range(self.heightmap_size_x):
                for index_y in range(self.heightmap_size_y):
                    random.shuffle(neighbour_offsets)
                    for neighbour in neighbour_offsets:
                        current_cell_height = self.heightmap[index_x][index_y]
                        try:  # to address neighbour
                            neighbour_cell_height = self.heightmap[index_x + neighbour[0]][index_y + neighbour[1]]
                            if current_cell_height - neighbour_cell_height > 1:
                                self.heightmap[index_x + neighbour[0]][index_y + neighbour[1]] += 1
                                self.heightmap[index_x][index_y] -= 1
                                # current_cell_height = self.heightmap[index_x][index_y]
                                particle_moved_this_land_cycle = True
                        except IndexError:  # can't address neighbour, it's out of bounds
                            pass

            if particle_moved_this_land_cycle is False:
                break

    def get_random_pos(self):
        """
        Get a random point on the heightmap.

        :return: Tuple representing an x, y position on the heightmap grid
        """
        # never returns an edge node
        return random.randint(1, self.heightmap_size_x - 1), random.randint(1, self.heightmap_size_y - 1)

    def normalise(self):
        """
        Lowers the whole terrain so that its lowest point is at zero height.
        """
        lowest_height_value = min([min(row) for row in self.heightmap])
        if lowest_height_value > 0:
            for index_x in range(self.heightmap_size_x):
                for index_y in range(self.heightmap_size_y):
                    self.heightmap[index_x][index_y] -= 1


def depth_shade(base_color, depth):
    """

    :param base_color:
    :param depth:
    :return:
    """
    r, g, b = base_color
    r = int(r + (255 - r) * depth * 0.5)
    g = int(g + (255 - g) * depth * 0.5)
    b = int(b + (255 - b) * depth * 0.65)
    return r, g, b


class Tiler:
    """

    """

    def __init__(self):
        map_size_cells = (16, 16)  # 8, 8
        self.map_size_cells = map_size_cells
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
                    terrain.perturb()
                    self.perturbs_counter += 1
        terrain.normalise()
        self.render_frame()

    def update(self):
        pass

    def render_frame(self):
        self.screen.fill(colors.BACKGROUND)
        self.draw_floor()
        for index_x in range(terrain.heightmap_size_x - 1):
            for index_y in range(terrain.heightmap_size_y - 1):
                tile = Tile(index_x, index_y)
                tile.draw()

        # limit fps
        self.fps_clock.tick(10)

        # update screen
        pygame.display.update()

    def handle_input(self):
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

    def camera(self, world_x, world_y, world_height=0):
        """

        :param world_x:
        :param world_y:
        :param world_height:
        :return:
        """
        screen_x = (world_x - world_y) / math.sqrt(2) + self.screen_width / 2
        screen_y = (world_x + world_y) / math.sqrt(2) / 2 + 100
        screen_y += world_height * self.terrain_height_scale
        # screen_x = int(screen_x)
        # screen_y = int(screen_y)
        return screen_x, screen_y

    def draw_floor(self):
        """

        """
        world_max_x = self.map_size_cells[0] * self.tile_size
        world_max_y = self.map_size_cells[1] * self.tile_size
        world_pointlist = [(0, 0),
                           (world_max_x, 0),
                           (world_max_x, world_max_y),
                           (0, world_max_y),
                           (0, 0)]
        screen_pointlist = []

        for world_x, world_y in world_pointlist:
            screen_pointlist.append(self.camera(world_x, world_y))
        pygame.draw.polygon(self.screen, colors.WORLD_EDGES, screen_pointlist)



if __name__ == "__main__":
    terrain = Terrain(MAP_SIZE_CELLS[0] + 1, MAP_SIZE_CELLS[1] + 1)
    tiler = Tiler()
    tiler.run()

