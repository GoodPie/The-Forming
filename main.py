"""Main game loop and menu for The Forming."""
import sys

import pygame

from the_forming.camera import Camera, main_camera
from the_forming.characters.player import Player
from the_forming.cursor import Cursor
from the_forming.image_cache import ImageCache
from the_forming.level_generation.level_generation import Level
from the_forming.ui.button import Button


def start_game_cb():
    """Callback indicating a new game should start."""
    return True

def quit_game():
    """Quit pygame and terminate the program."""
    print("User quit game")
    pygame.quit()
    sys.exit()


class Game:
    """Entry point for running the menu and main game loop."""
    tile_dir = "data/images/tiles/"
    ui_dir = "data/images/ui/"

    def __init__(self):
        """Initialize pygame, window, caches, and default state."""

        # Define window properties
        self.window_size = self.window_width, self.window_height = 640, 640
        self.tile_size = 32
        self.depth = 0
        self.flags = 0
        self.fps = 60

        # Initialize pygame
        pygame.init()

        # Define basic pygame properties
        self.screen = pygame.display.set_mode(self.window_size, self.flags, self.depth)
        self.clock = pygame.time.Clock()

        # Load the image cache
        self.tile_cache = ImageCache(Game.tile_dir)
        self.ui_cache = ImageCache(Game.ui_dir)

        # Define the key entities and default to None until we start the main game loop
        self.player = None

    def main_menu_loop(self):
        """Display and run the main menu until the user clicks New Game or Quit."""
        start_game = False

        # Create buttons with the static callback functions
        new_game_img = self.ui_cache.get_image("new_game_but")
        new_game_img_hov = self.ui_cache.get_image("new_game_but_hover")
        new_game_button = Button(self.get_half_width(), self.get_half_height() - 50,
                                 new_game_img, new_game_img_hov, 200, 50, start_game_cb)

        quit_img = self.ui_cache.get_image("quit_but")
        quit_img_hover = self.ui_cache.get_image("quit_but_hover")
        quit_button = Button(self.get_half_width(), self.get_half_height() + 10,
                             quit_img, quit_img_hover, 200, 50, quit_game)

        # Define sprite group for buttons to easily draw
        button_entities = pygame.sprite.Group()
        button_entities.add((new_game_button, quit_button))

        # Retrieve other UI images from cache
        bg_img = self.ui_cache.get_image("menu_bg")
        credits_img = self.ui_cache.get_image("credits")

        # Only draw background and other static images once to screen
        self.screen.blit(bg_img, (0, 0))
        self.screen.blit(credits_img, (20, self.window_height - 50))

        # Set the screen title
        pygame.display.set_caption("The Forming")

        while not start_game:
            self.clock.tick(self.fps)
            mouse_clicked = False

            # Loop through all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True
                if event.type == pygame.KEYDOWN:
                    pass

            # Update the buttons. Start game will return True if clicked, exiting the menu loop
            new_game_button.update(pygame.mouse.get_pos(), mouse_clicked)
            quit_button.update(pygame.mouse.get_pos(), mouse_clicked)

            button_entities.draw(self.screen)

            pygame.display.flip()

        self.main_game_loop()

    def main_game_loop(self):
        """Run the main gameplay loop until termination."""

        # Define the entity groups
        character_entities = pygame.sprite.Group()  # All character entities (including Player.py)

        # Build the level
        level = Level()
        level.generate(self.tile_cache)

        # Create the player
        player_sprites = "data/images/player/"
        camera = Camera(main_camera, level.width * self.tile_size, level.height * self.tile_size,
                        self.window_width, self.window_height)
        self.player = Player(32, 32, player_sprites, self.tile_size, self.tile_size, 2, camera)
        character_entities.add(self.player)

        # Create cursor entity for better collisions
        cursor = Cursor()

        game_running = True

        up, down, left, right = 0, 0, 0, 0

        while game_running:

            # Reset game variables

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

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

        self.main_menu_loop()

    def get_half_width(self):
        """Return half of the window width."""
        return self.window_width / 2

    def get_half_height(self):
        """Return half of the window height."""
        return self.window_height / 2


if __name__ == "__main__":
    game = Game()
    game.main_menu_loop()
