from Tiles.Tile import Tile


class Water(Tile):

    def __init__(self, x, y, img):
        Tile.__init__(self, x, y, "Water", img)
