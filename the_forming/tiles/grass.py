"""Tile implementation for grass terrain."""

from typing import TYPE_CHECKING

from pygame import Surface

from the_forming.tiles.tile import Tile

__all__ = ["Grass"]

if TYPE_CHECKING:
    pass


class Grass(Tile):
    """A simple grass tile."""

    def __init__(self, x: int, y: int, img: Surface) -> None:
        """Initialize a grass tile at the given coordinates with an image.

        Args:
            x: X-coordinate in pixels.
            y: Y-coordinate in pixels.
            img: Pygame surface representing the tile image.
        """
        super().__init__(x, y, "Grass", img)
