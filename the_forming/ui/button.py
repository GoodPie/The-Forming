from pygame.rect import Rect

from the_forming.entity import Entity


class Button(Entity):
    def __init__(self, x, y, img, img_hover, width, height, callback):
        super().__init__()
        self.image_norm = img
        self.image_hover = img_hover
        self.image = self.image_norm
        self.rect = Rect(x, y, width, height)

        self.callback = callback

    def update(self, cursor_pos, clicked=False):
        """
        Updates the current state of the button and calls the on clicked if needed.
        :param cursor_pos:  The current position of the cursor
        :param clicked:     Mouse has been clicked
        :return: Optional boolean return in case we need an action defined by the on click
        """
        if self.rect.collidepoint(cursor_pos[0], cursor_pos[1]):
            self.image = self.image_hover
            if clicked:
                return self.on_clicked()
        else:
            self.image = self.image_norm

        return False

    def on_clicked(self):
        """
        Calls the callback function
        :return: The return value of the callback
        """
        return self.callback()
