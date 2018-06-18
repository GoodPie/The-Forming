from Tiles.Tile import Tile


class Tree(Tile):

    def __init__(self, x, y, img):
        Tile.__init__(self, x, y, "Tree", img)
