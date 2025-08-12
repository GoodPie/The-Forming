"""Image cache for loading and reusing pygame textures."""
import glob

import pygame


class ImageCache:
    def __init__(self, directory: str, img_type: str = "png") -> None:
        self.cache: dict[str, pygame.Surface] = {}
        self.directory = directory
        self.img_type = img_type
        self.add_dir(directory)

    def add_dir(self, directory: str) -> None:
        """Add all images from a directory to the cache."""
        images = glob.glob(directory + "*." + self.img_type)
        for image in images:
            self.add_image(image)

    def add_image(self, key: str) -> None:
        """Add an individual image to the cache by full path."""
        if key not in self.cache:
            self.cache[key] = pygame.image.load(key).convert_alpha()

    def get_image(self, key: str) -> pygame.Surface:
        """Return image by short key (without extension) from the configured directory."""
        actual_key = self.directory + key + "." + self.img_type
        self.add_image(actual_key)
        return self.cache[actual_key]
