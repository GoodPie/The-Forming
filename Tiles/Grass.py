from Tiles.Tile import Tile


class Grass(Tile):

    def __init__(self, x, y, img):
        Tile.__init__(self, x, y, "Grass", img)
