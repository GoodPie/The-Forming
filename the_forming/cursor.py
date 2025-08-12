"""Cursor entity for mouse tracking."""
import pygame
from pygame.rect import Rect

from the_forming.entity import Entity


class Cursor(Entity):
    def __init__(self) -> None:
        super().__init__()
        mouse_pos = pygame.mouse.get_pos()
        self.rect = Rect(mouse_pos[0], mouse_pos[1], 32, 32)

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.rect.top = mouse_pos[1]
        self.rect.left = mouse_pos[0]
