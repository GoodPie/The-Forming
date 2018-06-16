from Entity import Entity


class Player(Entity):

    def __init__(self, start_x, start_y):
        Entity.__init__(self)

        self.x = start_x
        self.y = start_y
