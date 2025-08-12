from the_forming.characters.character import Character


class Player(Character):
    def __init__(self, start_x, start_y, sprite_dir, width, height, frames, camera, cache=None):
        super().__init__(start_x, start_y, sprite_dir, width, height, frames, cache)
        self.camera = camera

    def update(self, up, down, left, right, obstacles):
        super().update(up, down, left, right, obstacles)
        self.camera.update(self)
