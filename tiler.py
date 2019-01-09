import math
import random
import pygame
import pygame.gfxdraw

import colors

MAP_SIZE_CELLS = (16, 16)  # 8, 8
TILE_SIZE = 30  # 60
SEA_HEIGHT_CELLS = 4
MIN_HEIGHT_CELLS = 0
BASE_THICKNESS_CELLS = 1

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 480

PERTURBS_PER_UPDATE = 1
MAX_PERTURBS = 100

TERRAIN_HEIGHT_SCALE = 1 / math.sqrt(2)

world_sea_height = - SEA_HEIGHT_CELLS * TILE_SIZE / 2

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
            map_height = terrain.map_grid[self.index_x + offset_x][self.index_y + offset_y]
            self.absolute_heights.append(map_height)

        self.relative_heights = []
        self.relative_heights = self.get_relative_heights()

        # print(self.get_tile_geometry_type())
        self.geometry_type = self.get_tile_geometry_type()

    def draw(self):
        """

        """
        terrain_pointlist_screen = []
        sea_pointlist_screen = []

        # todo reuse the absolute heights already calculated
        for offset_x, offset_y in self.corner_offsets:
            world_x, world_y = self.index_x * TILE_SIZE, self.index_y * TILE_SIZE
            map_height = terrain.map_grid[self.index_x + offset_x][self.index_y + offset_y]
            world_terrain_height = - map_height * TILE_SIZE / 2

            terrain_pointlist_screen.append(
                camera(offset_x * TILE_SIZE + world_x, offset_y * TILE_SIZE + world_y,
                       world_terrain_height))

            sea_pointlist_screen.append(
                camera(offset_x * TILE_SIZE + world_x, offset_y * TILE_SIZE + world_y, world_sea_height))

        is_sea = False
        if max(self.absolute_heights) <= SEA_HEIGHT_CELLS:  # TODO needs improvement
            is_sea = True
            terrain_fill_color = colors.SEABED
            terrain_grid_color = colors.SEABED_GRID
        else:
            terrain_fill_color = colors.GRASS
            terrain_grid_color = colors.GRASS_GRID

        if self.geometry_type == 'simple':

            pygame.draw.polygon(tiler.screen, depth_shade(terrain_fill_color, self.depth_factor),
                                terrain_pointlist_screen)  # fill
            pygame.draw.polygon(tiler.screen, depth_shade(terrain_grid_color, self.depth_factor),
                                terrain_pointlist_screen, 1)  # grid/border

            if is_sea:
                pass
                # draw sea surface quad
                # pygame.draw.polygon(self.screen, depth_shade(colors.SEA, current_map_depth / self.terrain.map_depth),
                #                    sea_pointlist_screen)  # fill
                # pygame.draw.polygon(self.screen, colors.SEA_GRID, sea_pointlist_screen, 1)  # border

        elif self.geometry_type == 'flat-low':
            flat_tri_points = []
            slope_tri_points = []

            # print('relative_heights_at_offsets: {}'.format(relative_heights_at_offsets))
            for i in range(len(self.relative_heights)):
                if self.relative_heights[i] == 1:
                    flat_tri_points.append(terrain_pointlist_screen[i])

            # print('tri points: {}'.format(flat_tri_points))
            # print('quad points: {}'.format(terrain_pointlist_screen))
            # temp background quad
            pygame.draw.polygon(tiler.screen, depth_shade(colors.MAGENTA, self.depth_factor),
                                terrain_pointlist_screen)  # fill
            pygame.draw.polygon(tiler.screen, depth_shade(colors.BLACK, self.depth_factor), terrain_pointlist_screen,
                                1)  # border
            # draw flat tri
            pygame.draw.polygon(tiler.screen, depth_shade(terrain_fill_color, self.depth_factor),
                                flat_tri_points)  # fill
            pygame.draw.polygon(tiler.screen, depth_shade(terrain_grid_color, self.depth_factor), flat_tri_points,
                                1)  # border
            # draw slope tri

        elif self.geometry_type == 'flat-high':
            # draw flat tri
            flat_tri_points = []
            slope_tri_points = []

            # print('relative_heights_at_offsets: {}'.format(relative_heights_at_offsets))

            for i in range(len(self.relative_heights)):
                if self.relative_heights[i] == 0:
                    flat_tri_points.append(terrain_pointlist_screen[i])

            # print('tri points: {}'.format(flat_tri_points))
            # print('quad points: {}'.format(terrain_pointlist_screen))
            # temp background quad
            pygame.draw.polygon(tiler.screen, depth_shade(colors.CYAN, self.depth_factor),
                                terrain_pointlist_screen)  # fill
            pygame.draw.polygon(tiler.screen, depth_shade(colors.BLACK, self.depth_factor), terrain_pointlist_screen,
                                1)  # border
            # draw flat tri
            pygame.draw.polygon(tiler.screen, depth_shade(terrain_fill_color, self.depth_factor),
                                flat_tri_points)  # fill
            pygame.draw.polygon(tiler.screen, depth_shade(terrain_grid_color, self.depth_factor), flat_tri_points,
                                1)  # border

        else:
            # draw highlighted quad

            pygame.draw.polygon(tiler.screen, depth_shade(colors.RED, self.depth_factor),
                                terrain_pointlist_screen)  # fill
            pygame.draw.polygon(tiler.screen, depth_shade(colors.RED_DARK, self.depth_factor), terrain_pointlist_screen,
                                1)  # border

            # pygame.draw.polygon(self.screen, depth_shade(colors.RED, depth_factor), terrain_pointlist_screen[0:3])  # right tri
            # pygame.draw.polygon(self.screen, depth_shade(colors.YELLOW, depth_factor), terrain_pointlist_screen[1:4])  # front tri
            # pygame.draw.polygon(self.screen, depth_shade(colors.YELLOW, depth_factor), terrain_pointlist_screen[1:4])  # front tri

        # pygame.draw.circle(self.screen, colors.DEBUG, terrain_pointlist_screen[3], 5)

    def get_tile_geometry_type(self):
        """

        Returns
        -------

        """
        if self.relative_heights in [
            [0, 0, 0, 0],
            [0, 0, 1, 1],
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [1, 1, 0, 0]
        ]:
            return 'simple'
        elif sorted(self.relative_heights) == [0, 0, 0, 1]:
            return 'flat-high'
        elif sorted(self.relative_heights) == [0, 1, 1, 1]:
            return 'flat-low'
        elif sorted(self.relative_heights) == [0, 0, 1, 1]:
            return 'saddle'
        else:
            return 'unhandled geometry'  # todo raise error

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
    """

    """

    def __init__(self, map_size_x, map_size_y):
        """

        Parameters
        ----------
        map_size_x
        map_size_y
        """
        self.map_size_x = map_size_x
        self.map_size_y = map_size_y
        self.map_depth = map_size_x + map_size_y + 2
        self.map_grid = [[MIN_HEIGHT_CELLS for _x in range(self.map_size_x + 1)] for _y in range(self.map_size_y + 1)]

    def perturb(self):
        """Drop a quantity of particles at a single point on the Terrain object, then move the particles to neighbour cells
        until the terrain is 'stable'.
        """
        particles_per_drop = 128
        drop_index_x, drop_index_y = self.get_random_pos()
        self.map_grid[drop_index_x][drop_index_y] += particles_per_drop
        neighbour_offsets = ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))
        neighbour_weightings = (math.sqrt(0.5), 1, math.sqrt(0.5), 1, math.sqrt(0.5), 1, math.sqrt(0.5), 1)

        cycle = True
        while cycle is True:
            particle_moved = False
            for index_x in range(self.map_size_x):
                for index_y in range(self.map_size_y):
                    [neighbour_choice] = random.choices(neighbour_offsets, neighbour_weightings)
                    current_cell_height = self.map_grid[index_x][index_y]
                    try:
                        neighbour_cell_height = self.map_grid[index_x + neighbour_choice[0]][
                            index_y + neighbour_choice[1]]
                        if current_cell_height > neighbour_cell_height + 1:
                            self.map_grid[index_x + neighbour_choice[0]][index_y + neighbour_choice[1]] += 1
                            self.map_grid[index_x][index_y] -= 1
                            particle_moved = True
                    except IndexError:
                        particle_moved = True  # particle falls off edge of world
                        break
            if particle_moved is False:
                break

    def get_random_pos(self):
        """Get a random point on the heightmap.

        """
        # never returns an edge cell
        return random.randint(1, self.map_size_x - 2), random.randint(1, self.map_size_y - 2)

    def normalise(self, min_height):
        """
        Lowers the whole terrain so that its lowest point is at height 'min_height'
        """
        lowest_height_value = min([min(row) for row in self.map_grid])
        if lowest_height_value != min_height:
            increment = -1
            if lowest_height_value < min_height:
                increment = 1
            for index_x in range(self.map_size_x):
                for index_y in range(self.map_size_y):
                    self.map_grid[index_x][index_y] += increment


def depth_shade(base_color, depth, depth_color=colors.DEPTH_COLOR):
    """

    :param depth_color: 
    :param base_color:
    :param depth:
    :return:
    """

    r1, g1, b1 = base_color
    r2, g2, b2 = depth_color

    if DEPTH_SHADER:

        r = int((r1 * (1 - depth)) + r2 * depth)
        g = int((g1 * (1 - depth)) + g2 * depth)
        b = int((b1 * (1 - depth)) + b2 * depth)

        return r, g, b

    else:

        return r1, g1, b1


class Tiler:
    """

    """

    def __init__(self):

        self.world_size = ((terrain.map_size_x - 1) * TILE_SIZE, (terrain.map_size_y - 1) * TILE_SIZE)  #
        self.perturbs_counter = 0

        # initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tiler')

        self.fps_clock = pygame.time.Clock()
        self.running = True

    def run(self):
        """

        """
        while self.running:
            self.main_loop()

    def main_loop(self):
        """

        """
        self.handle_input()
        if self.perturbs_counter < MAX_PERTURBS:
            for _ in range(PERTURBS_PER_UPDATE):
                if self.perturbs_counter < MAX_PERTURBS:
                    terrain.perturb()
                    self.perturbs_counter += 1
        terrain.normalise(MIN_HEIGHT_CELLS)
        self.render_frame()

    def update(self):
        """

        """
        pass

    def render_frame(self):
        """

        """
        self.screen.fill(colors.BACKGROUND)
        self.draw_floor()
        for index_x in range(terrain.map_size_x - 1):
            for index_y in range(terrain.map_size_y - 1):
                tile = Tile(index_x, index_y)
                tile.draw()

        # limit fps
        self.fps_clock.tick(10)

        # update screen
        pygame.display.update()

    def handle_input(self):
        """

        """
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

    def draw_floor(self):
        """

        """

        world_pointlist = [(0, 0),
                           (self.world_size[0], 0),
                           (self.world_size[0], self.world_size[1]),
                           (0, self.world_size[1]),
                           (0, 0)]
        screen_pointlist = []

        for world_x, world_y in world_pointlist:
            screen_pointlist.append(camera(world_x, world_y, BASE_THICKNESS_CELLS * TILE_SIZE))
        pygame.draw.polygon(self.screen, colors.WORLD_EDGES, screen_pointlist)


if __name__ == "__main__":
    terrain = Terrain(MAP_SIZE_CELLS[0] + 1, MAP_SIZE_CELLS[1] + 1)
    tiler = Tiler()
    tiler.run()
