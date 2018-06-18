import pygame

from Entity import Entity, Rect


class Cursor(Entity):

    def __init__(self):
        Entity.__init__(self)
        mouse_pos = pygame.mouse.get_pos()
        self.rect = Rect(mouse_pos[0], mouse_pos[1], 32, 32)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.top = mouse_pos[1]
        self.rect.left = mouse_pos[0]
