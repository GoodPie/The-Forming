import sys

import pygame
from pygame.locals import *


# Main Entity Class
class Entity(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

# Start Menu New Game
class NewGame(Entity):

    def __init__(self, x, y, image_cache):
        Entity.__init__(self)
        self.image_cache = image_cache
        self.image = self.image_cache.get_image("new_game_but")
        self.image.convert()
        self.rect = Rect(x, y, 200, 50)

    def update(self, mousepos):
        if self.rect.collidepoint(mousepos):
            self.image = self.image_cache.get_image("new_game_but_hover")
        else:
            self.image = self.image_cache.get_image("new_game_but")

    def check_click(self, clicked, mousepos):
        if self.rect.collidepoint(mousepos):
            if clicked:
                self.image = self.image_cache.get_image("new_game_but_hover")
                start = True
            else:
                start = False
        else:
            start = False
        return start


# Start Menu Quit Button
class QuitGame(Entity):

    def __init__(self, x, y, image_cache):
        Entity.__init__(self)
        self.image_cache = image_cache
        self.image = self.image_cache.get_image("quit_but")
        self.image.convert()
        self.rect = Rect(x, y, 200, 50)

    def update(self, mousepos, clicked):
        if self.rect.collidepoint(mousepos):
            self.image = self.image_cache.get_image("quit_but_hover")
            if clicked:
                pygame.quit()
                sys.exit()
        else:
            self.image = self.image_cache.get_image("quit_but")
