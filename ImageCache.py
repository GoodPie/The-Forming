import glob

import pygame


class ImageCache:

    def __init__(self):

        self.cache = {}

    def add_dir(self, directory, img_type):
        """
        Adds an entire directory of images to the image cache
        :param directory:   Directory to look for images
        :param img_type:    The type of image to add (ie: png)
        """
        images = glob.glob(directory + "*." + img_type)
        for image in images:
            self.add_image(image)

    def add_image(self, key):
        """
        Adds an individual image to the image cache
        :param key:     Image to add, using the image name as a key
        """
        if not key in self.cache:
            self.cache[key] = pygame.image.load(key).convert_alpha()

    def get_image(self, key):
        """
        Returns an image from the image cache. Will add if not already a part of the cache
        :param key:     Image to add, using the image name as a key
        :return:        Image
        """
        self.add_image(key)
        return self.cache[key]
