from Tiles.Tile import Tile


class Foundation(Tile):

    def __init__(self, x, y, img):
        Tile.__init__(self, x, y, "Foundation", img)
