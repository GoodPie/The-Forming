from pygame.rect import Rect


# Camera function
def main_camera(camera, target_rect, window_width, window_height):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l + (window_width / 2), -t + (window_height / 2), w, h

    l = min(0, l)
    l = max(-(camera.width - window_width), l)
    t = max(-(camera.height - window_height), t)
    t = min(0, t)
    return Rect(l, t, w, h)


class Camera(object):

    def __init__(self, camera_func, width, height, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect, self.window_width, self.window_height)

    def reverse(self, pos):
        return pos[0] - self.state.left, pos[1] - self.state.top
