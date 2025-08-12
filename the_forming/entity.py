"""Entity base class."""
import pygame


class Entity(pygame.sprite.Sprite):
    """Base sprite entity."""

    def __init__(self) -> None:
        super().__init__()
