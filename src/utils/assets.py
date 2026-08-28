import os

import pygame

from constants import ASTEROID_MIN_RADIUS


class AssetLoader:
    _asteroid_images: dict[int, pygame.Surface] = {}
    _images: dict[str, pygame.Surface] = {}

    @classmethod
    def get_image(cls, path: str) -> pygame.Surface | None:
        if path in cls._images:
            return cls._images[path]

        if not os.path.exists(path):
            return None

        image = pygame.image.load(path).convert_alpha()
        cls._images[path] = image

        return image

    @classmethod
    def get_asteroid_image(cls, radius: float) -> pygame.Surface:
        radius_key = int(radius)

        if radius_key in cls._asteroid_images:
            return cls._asteroid_images[radius_key]

        if radius_key == ASTEROID_MIN_RADIUS:
            path = "assets/images/asteroid_small.png"
        elif radius_key == ASTEROID_MIN_RADIUS * 2:
            path = "assets/images/asteroid_medium.png"
        else:
            path = "assets/images/asteroid_large.png"

        image = pygame.image.load(path).convert_alpha()

        diameter = int(radius * 2)

        image = pygame.transform.scale(
            image,
            (diameter, diameter),
        )

        cls._asteroid_images[radius_key] = image

        return image
