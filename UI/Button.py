from Entity import Entity, Rect


class Button(Entity):

    def __init__(self, x, y, img, img_hover, width, height):
        Entity.__init__(self)
        self.image_norm = img
        self.image_hover = img_hover
        self.image = self.image_norm
        self.rect = Rect(x, y, width, height)

    def update(self, cursor_pos, clicked=False):
        if self.rect.collidepoint(cursor_pos):
            self.image = self.image_hover
        else:
            self.image = self.image_norm
        if clicked:
            self.on_clicked()

    def on_clicked(self):
        pass
