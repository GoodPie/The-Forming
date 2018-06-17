from Entity import Entity, Rect


class Cursor(Entity):

    def __init__(self, pos):
        Entity.__init__(self)
        self.rect = Rect(pos[0], pos[1], 32, 32)

    def update(self, pos):
        self.rect.top = pos[1]
        self.rect.left = pos[0]
