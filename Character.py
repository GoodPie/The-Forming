from pygame.rect import Rect

from Entity import Entity
from ImageCache import ImageCache


class Character(Entity):

    def __init__(self, start_x, start_y, sprite_dir, width, height, cache=None):
        Entity.__init__(self)

        # Directory where all the sprites will be held
        # This must include up, down, left, right in both idle and walking positions
        # TODO: Implement other movement types
        self.sprite_dir = sprite_dir

        # We can preload the cache in for duplicated characters or just create a new one
        if cache is None:
            self.cache = ImageCache(sprite_dir)
        else:
            self.cache = cache

        # Default the sprite to face down
        self.image = self.cache.get_image("down_idle")

        # Where to spawn the character
        self.x_speed = 0
        self.y_speed = 0
        self.width = width
        self.height = height

        # Define movement properties
        self.speed = 8
        self.sneak_mult = 0.4
        self.sprint_mult = 1.5

        self.rect = Rect(start_x, start_y, self.width, self.height)

    def update(self, up, down, left, right, obstacles):
        x_dir = -left + right
        y_dir = -up + down

        self.x_speed = x_dir * self.speed
        self.y_speed = y_dir * self.speed

        # Update the characters rect to apply movement
        self.rect.left += self.x_speed
        self.rect.top += self.y_speed

        # This is my dodgy answer for now. Still better than original... maybe
        # TODO: Look more into sprite collisions in PyGame
        # for obstacle in obstacles:
        #    hit = pygame.sprite.spritecollide(self, obstacle, False)
        #    if hit:
        #        self.rect.left -= self.x_speed
        #        self.rect.right -= self.y_speed

        self.animate()

    def animate(self):

        if self.y_speed != 0 and self.x_speed != 0:
            if self.x_speed < 0:
                self.image = self.cache.get_image("left")
            elif self.x_speed > 0:
                self.image = self.cache.get_image("right")
            elif self.x_speed < 0:
                self.image = self.cache.get_image("up")
            elif self.y_speed > 0:
                self.image = self.cache.get_image("down")

    def get_pos(self):
        return self.rect.left, self.rect.top
