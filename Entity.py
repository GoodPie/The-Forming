import sys

import pygame
from pygame.locals import *


# Main Entity Class
class Entity(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
