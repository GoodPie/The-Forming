from Tiles.Tile import Tile


class Planks(Tile):

    def __init__(self, x, y, img):
        Tile.__init__(self, x, y, "Planks", img)
