import glob

import pygame


class ImageCache:

    def __init__(self, directory, img_type='png'):

        self.cache = {}
        self.directory = directory
        self.img_type = img_type
        self.add_dir(directory)

    def add_dir(self, directory):
        """
        Adds an entire directory of images to the image cache
        :param directory:   Directory to look for images
        :param img_type:    The type of image to add (ie: png)
        """
        images = glob.glob(directory + "*." + self.img_type)
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
        actual_key = self.directory + key + "." + self.img_type
        self.add_image(actual_key)
        return self.cache[actual_key]
