"""Main game loop and menu for The Forming."""
import sys

import pygame

from the_forming import config
from the_forming.image_cache import ImageCache
from the_forming.screens.game import GameScreen
from the_forming.screens.menu import MenuScreen


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
    tile_dir = config.TILE_DIR
    ui_dir = config.UI_DIR

    def __init__(self):
        """Initialize pygame, window, caches, and default state."""

        # Define window properties
        self.window_width = config.WINDOW_WIDTH
        self.window_height = config.WINDOW_HEIGHT
        self.window_size = config.WINDOW_SIZE
        self.tile_size = config.TILE_SIZE
        self.depth = config.DEPTH
        self.flags = config.FLAGS
        self.fps = config.FPS

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
        menu = MenuScreen(
            self.screen,
            self.clock,
            self.fps,
            self.ui_cache,
            self.window_width,
            self.window_height,
            quit_game,
        )
        start_game = menu.run()
        if start_game:
            self.main_game_loop()

    def main_game_loop(self):
        """Run the main gameplay loop until termination."""
        game = GameScreen(
            self.screen,
            self.clock,
            self.fps,
            self.tile_cache,
            self.window_width,
            self.window_height,
            self.tile_size,
            quit_game,
        )
        game.run()

    def get_half_width(self):
        """Return half of the window width."""
        return self.window_width / 2

    def get_half_height(self):
        """Return half of the window height."""
        return self.window_height / 2


if __name__ == "__main__":
    game = Game()
    game.main_menu_loop()
