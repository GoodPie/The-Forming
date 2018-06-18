"""This is where all primary, "non-game" related functions are helf"""
import time

from Entity import *


# Screen shot functionality
def take_screen_shot(screen):
    time_taken = time.asctime(time.localtime(time.time()))
    time_taken = time_taken.replace(" ", "_")
    time_taken = time_taken.replace(":", ".")
    save_file = "screenshots/" + time_taken + ".png"
    pygame.image.save(screen, save_file)
    print("A screen shot has been taken and saved as: " + save_file)


def currentLevelChecker(area="generation"):
    return area



