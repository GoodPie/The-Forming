from the_forming.tiles.tile import Tile


class Water(Tile):
    def __init__(self, x, y, img):
        super().__init__(x, y, "Water", img)
