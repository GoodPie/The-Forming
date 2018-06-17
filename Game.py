import pygame

import tilemap
from Character import Character
from ImageCache import ImageCache
from UI.Button import Button


class Game:
    tile_dir = "data/images/tiles/"
    ui_dir = "data/images/ui/"

    def __init__(self):
        self.window_size = self.window_width, self.window_height = 640, 640
        self.tile_size = 32
        self.depth = 0
        self.flags = 32
        self.fps = 60

        # Initialize pygame
        pygame.init()

        self.screen = pygame.display.set_mode(self.window_size, self.flags, self.depth)
        self.clock = pygame.time.Clock()

        self.tile_cache = ImageCache(Game.tile_dir)
        self.ui_cache = ImageCache(Game.ui_dir)

        # Create different sprite groups
        self.collidable_entities = pygame.sprite.Group()
        self.built_entities = pygame.sprite.Group()
        self.character_entities = pygame.sprite.Group()

        # Create the main player
        # TODO: Use own player class when finished
        player_sprites = "data/images/player/"
        self.player = Character(32, 32, player_sprites, self.tile_size, self.tile_size)
        self.character_entities.add(self.player)

        # Create the game level
        self.level = tilemap.get_level()

    def main_menu_loop(self):
        start_game = False

        # Create buttons
        new_game_img = self.ui_cache.get_image("new_game_but")
        new_game_img_hov = self.ui_cache.get_image("new_game_but_hover")
        new_game_button = Button(self.get_half_width(), self.get_half_height() - 50,
                                 new_game_img, new_game_img_hov, 200, 50)

        quit_img = self.ui_cache.get_image("quit_but")
        quit_img_hover = self.ui_cache.get_image("quit_but_hover")
        quit_button = Button(self.get_half_width(), self.get_half_height() + 10,
                             quit_img, quit_img_hover, 200, 50)

        # Create entity groups for the buttons for collisions
        button_entities = pygame.sprite.Group()
        button_entities.add((new_game_button, quit_button))

        bg_img = self.ui_cache.get_image("menu_bg")
        credits_img = self.ui_cache.get_image("credits")

        # Add UI to screen
        self.screen.blit(bg_img, (0, 0))
        self.screen.blit(credits_img, (20, self.get_half_height() - 50))

        while not start_game:
            break

    def get_half_width(self):
        return self.window_width / 2

    def get_half_height(self):
        return self.window_height / 2
