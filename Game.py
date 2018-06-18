import pygame

from ImageCache import ImageCache
from UI.Button import Button


def start_game_cb():
    return True


def quit_game():
    print("User quit game")
    pygame.quit()
    exit()


class Game:
    tile_dir = "data/images/tiles/"
    ui_dir = "data/images/ui/"

    def __init__(self):

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

        # Create different sprite groups and default to None until we start the main game loop
        self.collidable_entities = None
        self.built_entities = None
        self.character_entities = None

        # Define the key entities and default to None until we start the main game loop
        self.player = None
        self.level = None

    def main_menu_loop(self):
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
            start_game = new_game_button.update(pygame.mouse.get_pos(), mouse_clicked)
            quit_button.update(pygame.mouse.get_pos(), mouse_clicked)

            button_entities.draw(self.screen)

            pygame.display.flip()

    def get_half_width(self):
        return self.window_width / 2

    def get_half_height(self):
        return self.window_height / 2


if __name__ == "__main__":
    game = Game()
    game.main_menu_loop()
