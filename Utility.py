import time
import pygame


def take_screen_shot(screen):
    """
    Takes a screenshot and saves it to the screenshot directory
    :param screen:  Screen to take screenshot of
    """
    time_taken = time.asctime(time.localtime(time.time()))
    time_taken = time_taken.replace(" ", "_")
    time_taken = time_taken.replace(":", ".")
    save_file = "screenshots/" + time_taken + ".png"
    pygame.image.save(screen, save_file)
    print("A screen shot has been taken and saved as: " + save_file)




