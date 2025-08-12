from the_forming.tiles.tile import Tile


class Tree(Tile):
    def __init__(self, x, y, img):
        super().__init__(x, y, "Tree", img)
