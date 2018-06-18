from Tiles.Tile import Tile


class Sand(Tile):

    def __init__(self, x, y, img):
        Tile.__init__(self, x, y, "Sand", img)
