import os

import pygame

from constants import ASSET_FONTS, ASSET_IMAGES, ASSET_SOUNDS, ASTEROID_MIN_RADIUS


class SpriteManager:button_image
    _asteroid_images: dict[int, pygame.Surface] = {}
    _images: dict[str, pygame.Surface] = {}
    _sounds: dict[str, pygame.mixer.Sound] = {}
    _fonts: dict[tuple[str, int], pygame.font.Font] = {}

    @classmethod
    def get_image(cls, name: str) -> pygame.Surface | None:
        if name in cls._images:
            return cls._images[name]

        path = ASSET_IMAGES.get(name)
        if not path or not os.path.exists(path):
            return None

        image = pygame.image.load(path).convert_alpha()
        cls._images[name] = image
        return image

    @classmethod
    def get_sound(cls, name: str) -> pygame.mixer.Sound | None:
        if name in cls._sounds:
            return cls._sounds[name]

        path = ASSET_SOUNDS.get(name)
        if not path or not os.path.exists(path):
            return None

        sound = pygame.mixer.Sound(path)
        cls._sounds[name] = sound
        return sound

    @classmethod
    def get_font(cls, name: str, size: int) -> pygame.font.Font | None:
        key = (name, size)
        if key in cls._fonts:
            return cls._fonts[key]

        path = ASSET_FONTS.get(name)
        if not path or not os.path.exists(path):
            return None

        font = pygame.font.Font(path, size)
        cls._fonts[key] = font
        return font

    @classmethod
    def get_asteroid_image(cls, radius: float) -> pygame.Surface:
        radius_key = int(radius)
        if radius_key in cls._asteroid_images:
            return cls._asteroid_images[radius_key]

        if radius_key == ASTEROID_MIN_RADIUS:
            image_name = "asteroid_small"
        elif radius_key == ASTEROID_MIN_RADIUS * 2:
            image_name = "asteroid_medium"
        else:
            image_name = "asteroid_large"

        image = cls.get_image(image_name)
        if not image:
            image = pygame.Surface((int(radius * 2), int(radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(
                image, "white", (int(radius), int(radius)), int(radius), 2
            )

        diameter = int(radius * 2)
        image = pygame.transform.scale(image, (diameter, diameter))

        cls._asteroid_images[radius_key] = image
        return image
