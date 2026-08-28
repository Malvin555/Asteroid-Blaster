import random

import pygame

from constants import ASTEROID_KINDS, ASTEROID_MIN_RADIUS
from entities.circleshape import CircleShape
from utils.logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

        self.score = (ASTEROID_KINDS - (radius // ASTEROID_MIN_RADIUS) + 1) * 10

        self.image = self._load_image()

        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-100, 100)

    def _load_image(self) -> pygame.Surface:
        if self.radius == ASTEROID_MIN_RADIUS:
            path = "assets/images/asteroid_small.png"
        elif self.radius == ASTEROID_MIN_RADIUS * 2:
            path = "assets/images/asteroid_medium.png"
        else:
            path = "assets/images/asteroid_large.png"

        image = pygame.image.load(path).convert_alpha()

        diameter = int(self.radius * 2)

        return pygame.transform.scale(
            image,
            (diameter, diameter),
        )

    def draw(self, screen: pygame.Surface) -> None:
        image = pygame.transform.rotate(
            self.image,
            self.rotation,
        )

        rect = image.get_rect(
            center=self.position,
        )

        screen.blit(image, rect)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.rotation += self.rotation_speed * dt

    def split(self) -> None:
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        angle = random.uniform(20, 50)

        first_velocity = self.velocity.rotate(angle)
        second_velocity = self.velocity.rotate(-angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        first = Asteroid(
            self.position.x,
            self.position.y,
            new_radius,
        )

        second = Asteroid(
            self.position.x,
            self.position.y,
            new_radius,
        )

        first.velocity = first_velocity * 1.2
        second.velocity = second_velocity * 1.2
