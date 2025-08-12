"""Tile base class."""
from pygame.rect import Rect

from the_forming.entity import Entity


class Tile(Entity):
    def __init__(self, x: int, y: int, name: str, img, width: int = 32, height: int = 32) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.name = name
        self.image = img
        self.rect = Rect(x, y, width, height)

    def hit_test(self, x: int, y: int) -> bool:
        """Return True if the given x,y is within this tile's rect."""
        return (self.rect.x <= x < self.rect.x + self.rect.width and
                self.rect.y <= y < self.rect.y + self.rect.height)
