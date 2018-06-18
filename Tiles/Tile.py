from Entity import Entity, Rect


class Tile(Entity):

    def __init__(self, x, y, name, img, width=32, height=32):
        Entity.__init__(self)
        self.x = x
        self.y = y
        self.name = name
        self.image = img
        self.rect = Rect(x, y, width, height)

    def hit_test(self, x, y):
        """
        Determines if the current x and y coordinates are within the tiles rect
        :param x:
        :param y:
        :return:    x and y inside the current tile?
        """
        return (self.rect.x <= x < self.rect.x + self.rect.width and
                self.rect.y <= y < self.rect.y + self.rect.height)
