"""Menu screen implementation separated from main game loop."""
import pygame

from the_forming import config
from the_forming.screens import menu_config
from the_forming.ui.button import Button


class MenuScreen:
    def __init__(self, screen, clock, fps, ui_cache, window_width, window_height, quit_callback):
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.ui_cache = ui_cache
        self.window_width = window_width
        self.window_height = window_height
        self.quit_callback = quit_callback

        # Preload images
        self.new_game_img = self.ui_cache.get_image("new_game_but")
        self.new_game_img_hov = self.ui_cache.get_image("new_game_but_hover")
        self.quit_img = self.ui_cache.get_image("quit_but")
        self.quit_img_hover = self.ui_cache.get_image("quit_but_hover")
        self.bg_img = self.ui_cache.get_image("menu_bg")
        self.credits_img = self.ui_cache.get_image("credits")

        # Create buttons
        self.new_game_button = Button(
            self.get_half_width(),
            self.get_half_height() + menu_config.MENU_NEW_GAME_Y_OFFSET,
            self.new_game_img,
            self.new_game_img_hov,
            menu_config.MENU_BUTTON_WIDTH,
            menu_config.MENU_BUTTON_HEIGHT,
            lambda: True,
        )

        self.quit_button = Button(
            self.get_half_width(),
            self.get_half_height() + menu_config.MENU_QUIT_Y_OFFSET,
            self.quit_img,
            self.quit_img_hover,
            menu_config.MENU_BUTTON_WIDTH,
            menu_config.MENU_BUTTON_HEIGHT,
            self.quit_callback,
        )

        self.button_entities = pygame.sprite.Group()
        self.button_entities.add((self.new_game_button, self.quit_button))

    def get_half_width(self):
        return self.window_width / 2

    def get_half_height(self):
        return self.window_height / 2

    def run(self) -> bool:
        """
        Run the menu loop. Returns True if a new game was requested.
        """
        start_game = False

        # Draw static background and credits once
        self.screen.blit(self.bg_img, (0, 0))
        self.screen.blit(
            self.credits_img,
            (menu_config.CREDITS_MARGIN_LEFT, self.window_height - menu_config.CREDITS_MARGIN_BOTTOM),
        )

        pygame.display.set_caption(config.WINDOW_TITLE)

        while not start_game:
            self.clock.tick(self.fps)
            mouse_clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Delegate quitting logic
                    self.quit_callback()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True

            # Update buttons
            if self.new_game_button.update(pygame.mouse.get_pos(), mouse_clicked):
                start_game = True
            self.quit_button.update(pygame.mouse.get_pos(), mouse_clicked)

            self.button_entities.draw(self.screen)
            pygame.display.flip()

        return True
