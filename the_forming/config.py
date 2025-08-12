"""Project-wide configuration and constants.

Centralizes common values to avoid magic numbers across the codebase.
"""

# Display
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
DEPTH = 0
FLAGS = 0
FPS = 60
WINDOW_TITLE = "The Forming"  # Window caption / app title

# Tiles
TILE_SIZE = 32

# Asset directories
TILE_DIR = "data/images/tiles/"
UI_DIR = "data/images/ui/"
PLAYER_SPRITES_DIR = "data/images/player/"

# App files
SAVE_FILE_NAME = "the_forming_save.json"  # Default save file name

# Screen-specific settings have been moved to per-screen configs:
# - Menu: the_forming.screens.menu_config
# - Game: the_forming.screens.game_config
