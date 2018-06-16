from Tiles.Tile import Tile


class Path(Tile):

    def __init__(self, x, y, img):
        Tile.__init__(self, x, y, "Path", img)
