"""This is where all primary, "non-game" related functions are helf"""
import time
from EntityClasses import *

#Screen shot functionality
def take_screen_shot(screen):
    time_taken = time.asctime(time.localtime(time.time()))
    time_taken = time_taken.replace(" ", "_")
    time_taken = time_taken.replace(":", ".")
    save_file = "screenshots/" + time_taken + ".png"
    pygame.image.save(screen, save_file)
    print "A screen shot has been taken and saved as: " + save_file
    
    

#This is a test to load images into a dictionary for faster loading
def get_image(key, cache):
    if not key in cache:
        cache[key] = pygame.image.load(key).convert_alpha()
    return cache[key]

def currentLevelChecker(area="generation"):
    return area

class Camera(object):

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
            self.state = self.camera_func(self.state, target.rect)

    def reverse(self, pos):
        return (pos[0] - self.state.left, pos[1] - self.state.top)

