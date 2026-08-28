import random

import pygame

from constants import (
    ASTEROID_BLINK_INTERVAL,
    ASTEROID_BLINK_TIME,
    ASTEROID_KINDS,
    ASTEROID_LARGE_SPEED,
    ASTEROID_LIFETIME,
    ASTEROID_MEDIUM_SPEED,
    ASTEROID_MIN_RADIUS,
    ASTEROID_SMALL_SPEED,
)
from entities.circleshape import CircleShape
from utils.assets import AssetLoader
from utils.logger import log_event


class Asteroid(CircleShape):
    def __init__(
        self,
        x: float,
        y: float,
        radius: float,
    ) -> None:
        super().__init__(x, y, radius)

        self.score = (ASTEROID_KINDS - (radius // ASTEROID_MIN_RADIUS) + 1) * 10

        self.image = AssetLoader.get_asteroid_image(self.radius)

        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-100, 100)

        self.lifetime = ASTEROID_LIFETIME

        self.speed = self._get_speed()

        self.velocity = pygame.Vector2(0, 1).rotate(random.uniform(0, 360)) * self.speed

    def _get_speed(self) -> float:
        if self.radius <= ASTEROID_MIN_RADIUS:
            return ASTEROID_SMALL_SPEED

        if self.radius <= ASTEROID_MIN_RADIUS * 2:
            return ASTEROID_MEDIUM_SPEED

        return ASTEROID_LARGE_SPEED

    def draw(self, screen: pygame.Surface) -> None:
        if self.lifetime <= ASTEROID_BLINK_TIME:
            blink = int(self.lifetime / ASTEROID_BLINK_INTERVAL)

            if blink % 2 == 0:
                return

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

        self.lifetime -= dt

        if self.lifetime <= 0:
            self.kill()

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
