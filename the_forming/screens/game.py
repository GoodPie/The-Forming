"""Game screen implementation separated from main module."""
import pygame

from the_forming import config
from the_forming.camera import Camera, main_camera
from the_forming.characters.player import Player
from the_forming.cursor import Cursor
from the_forming.level_generation.level_generation import Level
from the_forming.screens import game_config


class GameScreen:
    def __init__(self, screen, clock, fps, tile_cache, window_width, window_height, tile_size, quit_callback):
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.tile_cache = tile_cache
        self.window_width = window_width
        self.window_height = window_height
        self.tile_size = tile_size
        self.quit_callback = quit_callback

        # Initialized later
        self.player = None

    def run(self):
        """Run the main gameplay loop until termination."""
        # Define the entity groups
        character_entities = pygame.sprite.Group()

        # Build the level
        level = Level()
        level.generate(self.tile_cache)

        # Create the player
        player_sprites = config.PLAYER_SPRITES_DIR
        camera = Camera(
            main_camera,
            level.width * self.tile_size,
            level.height * self.tile_size,
            self.window_width,
            self.window_height,
        )
        self.player = Player(
            config.TILE_SIZE,
            config.TILE_SIZE,
            player_sprites,
            self.tile_size,
            self.tile_size,
            game_config.PLAYER_ANIM_FRAMES,
            camera,
        )
        character_entities.add(self.player)

        # Create cursor entity for better collisions
        cursor = Cursor()

        up, down, left, right = 0, 0, 0, 0

        running = True
        while running:
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_callback()

                # Key down events
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        up = 1
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        down = 1
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        left = 1
                    if event.key in (pygame.K_RIGHT, pygame.K_d):
                        right = 1

                # Key up events
                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        up = 0
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        down = 0
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        left = 0
                    if event.key in (pygame.K_RIGHT, pygame.K_d):
                        right = 0

            cursor.update()

            for tile in level.terrain:
                self.screen.blit(tile.image, self.player.camera.apply(tile))

            for tile in level.obstacles:
                self.screen.blit(tile.image, self.player.camera.apply(tile))

            for character in character_entities:
                self.screen.blit(character.image, self.player.camera.apply(character))

            self.player.update(up, down, left, right, level.obstacles)

            pygame.display.flip()

        # Currently, this loop only ends on quit.
        return None
