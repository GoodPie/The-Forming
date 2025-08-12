from pygame.rect import Rect

from the_forming.entity import Entity
from the_forming.image_cache import ImageCache


class Character(Entity):
    def __init__(self, start_x, start_y, sprite_dir, width, height, frames, cache=None):
        super().__init__()

        # Directory where all the sprites will be held
        self.sprite_dir = sprite_dir

        # We can preload the cache in for duplicated characters or just create a new one
        if cache is None:
            self.cache = ImageCache(sprite_dir)
        else:
            self.cache = cache

        # Default the sprite to face down
        self.image = self.cache.get_image("down_1")

        # Where to spawn the character
        self.x_speed = 0
        self.y_speed = 0
        self.width = width
        self.height = height

        # Define movement properties
        self.speed = 8
        self.sneak_mult = 0.4
        self.sprint_mult = 1.5

        # Animation properties
        self.anim_frames = frames  # How many animation frames
        self.current_anim_frame = 0
        self.frame_wait = 4  # How long to wait between frames
        self.current_frame_wait = 0

        self.rect = Rect(start_x, start_y, self.width, self.height)

    def update(self, up, down, left, right, obstacles):
        x_dir = -left + right
        y_dir = -up + down

        self.x_speed = x_dir * self.speed
        self.y_speed = y_dir * self.speed

        # Update the characters rect to apply movement
        self.rect.left += self.x_speed
        self.rect.top += self.y_speed

        self.animate()

    def animate(self):
        # Just determine which frame of which direction to use as current image
        if self.x_speed < 0:
            self.image = self.cache.get_image("left_" + str(self.current_anim_frame))
        elif self.x_speed > 0:
            self.image = self.cache.get_image("right_" + str(self.current_anim_frame))
        elif self.y_speed < 0:
            self.image = self.cache.get_image("up_" + str(self.current_anim_frame))
        elif self.y_speed > 0:
            self.image = self.cache.get_image("down_" + str(self.current_anim_frame))

        # Create a pause between frames
        self.current_frame_wait += 1
        if self.current_frame_wait >= self.frame_wait:
            # Frame switch
            self.current_anim_frame += 1
            if self.current_anim_frame >= self.anim_frames:
                self.current_anim_frame = 0
            self.current_frame_wait = 0

    def get_pos(self):
        return self.rect.left, self.rect.top
