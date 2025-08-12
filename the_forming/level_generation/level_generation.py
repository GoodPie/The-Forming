"""Terrain generation and level composition."""

import pygame

from the_forming.level_generation.diamond_square import DiamondSquare
from the_forming.tiles.grass import Grass
from the_forming.tiles.sand import Sand
from the_forming.tiles.water import Water


class Level:
    """World level containing terrain and obstacles; generates map via Diamond-Square."""

    def __init__(self, width=200, height=200, roughness=0.2):
        self.width = width
        self.height = height
        self.map = DiamondSquare(8, roughness)
        self.terrain = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.level = []

    def generate(self, tile_cache):
        """Generate the level terrain and obstacles using cached tile images."""
        grid = self.map.get_grid_2D()

        for y, col in enumerate(grid):
            for x, val in enumerate(col):
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


