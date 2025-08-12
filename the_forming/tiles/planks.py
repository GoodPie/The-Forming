from the_forming.tiles.tile import Tile


class Planks(Tile):
    def __init__(self, x, y, img):
        super().__init__(x, y, "Planks", img)
