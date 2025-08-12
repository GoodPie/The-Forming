import random

import pygame

from the_forming.tiles.grass import Grass
from the_forming.tiles.sand import Sand
from the_forming.tiles.water import Water


def clamp(value, a, b):
    if value < a:
        value = a
    elif value > b:
        value = b

    return value


class Level:

    def __init__(self, width=200, height=200, roughness=0.2):
        self.width = width
        self.height = height
        self.map = DiamondSquare(8, roughness)
        self.terrain = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.level = []

    def generate(self, tile_cache):
        grid = self.map.get_grid_2D()

        # TODO: Add more tiles and depth to the level
        for y in range(len(grid)):
            for x in range(len(grid)):
                val = grid[x][y]
                if val <= 0.1:
                    # Water
                    self.level.append('W')
                    water_img = tile_cache.get_image("water")
                    self.obstacles.add(Water(x * 32, y * 32, water_img))
                elif 0.1 < val < 0.2:
                    # Sand
                    sand_img = tile_cache.get_image("sand_01")
                    self.terrain.add(Sand(x * 32, y * 32, sand_img))
                    self.level.append('S')
                else:
                    # Grass
                    grass_img = tile_cache.get_image("grass_01")
                    self.terrain.add(Grass(x * 32, y * 32, grass_img))
                    self.level.append('G')


class DiamondSquare:
    """
    Based heavily off of https://github.com/hunterloftis/playfuljs-demos/blob/gh-pages/terrain/index.html#L65 and
    http://www.bluh.org/code-the-diamond-square-algorithm/ with majority of theory from http://www.gameprogrammer.com/fractal.html
    """

    def __init__(self, size, roughness):

        self.grid = []
        self.size = (2 ** size) + 1
        self.max = self.size - 1
        self.roughness = roughness
        self.make_grid(self.size)
        self.divide(self.max)  # Start

    # Sets x,y position in self.grid
    def set(self, x, y, val):
        self.grid[x + self.size * y] = val;

    # Get's value of x, y in self.grid
    def get(self, x, y):
        if x < 0 or x > self.max or y < 0 or y > self.max:
            return -1
        return self.grid[x + self.size * y]

    # Clamps x between min and max

    # Main iteration
    def divide(self, size):

        x = int(size / 2)
        y = int(size / 2)
        half = int(size / 2)
        scale = int(self.roughness * size)

        if half < 1:
            return

        # Square
        for y in range(half, self.max, int(size)):
            for x in range(half, self.max, int(size)):
                s_scale = random.uniform(0, 1) * scale * 2 - scale
                self.square(x, y, half, s_scale)

        # Diamond
        for y in range(0, self.max + 1, int(half)):
            for x in range((y + half) % int(size), self.max + 1, int(size)):
                d_scale = random.uniform(0, 1) * scale * 2 - scale
                self.diamond(x, y, half, d_scale)

        self.divide(size / 2)

    def square(self, x, y, size, scale):

        top_left = self.get(x - size, y - size)
        top_right = self.get(x + size, y - size)
        bottom_left = self.get(x + size, y + size)
        bottom_right = self.get(x - size, y + size)

        average = ((top_left + top_right + bottom_left + bottom_right) / 4)
        self.set(x, y, clamp(average + scale, 0, 1))

    def diamond(self, x, y, size, scale):

        top = self.get(x, y - size)
        right = self.get(x + size, y)
        bottom = self.get(x, y + size)
        left = self.get(x - size, y)

        average = ((top + right + bottom + left) / 4)
        self.set(x, y, clamp(average + scale, 0, 1))

    def make_grid(self, size):

        # Make the grid
        for x in range(size * size):
            self.grid.append(-1)

        # Base value
        self.set(0, 0, 1)
        self.set(self.max, 0, 0.5)
        self.set(self.max, self.max, 0)
        self.set(0, self.max, 0.5)

    # Returns a 2D array of the grid
    # Used for easier readability and manipulation
    def get_grid_2D(self):
        grid_2d = [self.grid[x:x + self.size] for x in range(0, len(self.grid), self.size)]
        return grid_2d
