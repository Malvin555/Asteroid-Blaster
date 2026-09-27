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
    DIFFICULTY_MODIFIERS,
)
from entities.circle_shape import CircleShape
from utils.logger import log_event
from utils.sprite_manager import SpriteManager


class Asteroid(CircleShape):
    def __init__(
        self, x: float, y: float, radius: float, difficulty: str = "NORMAL"
    ) -> None:
        super().__init__(x, y, radius)

        self.score = (ASTEROID_KINDS - (radius // ASTEROID_MIN_RADIUS) + 1) * 10
        self.difficulty = difficulty

        self.image = SpriteManager.get_asteroid_image(self.radius)

        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-100, 100)

        self.lifetime = ASTEROID_LIFETIME

        speed_mult = DIFFICULTY_MODIFIERS.get(difficulty, {}).get("speed_mult", 1.0)
        self.speed = self._get_speed() * speed_mult

        self.velocity = pygame.Vector2(0, 1).rotate(random.uniform(0, 360)) * self.speed

    def _get_speed(self) -> float:
        if self.radius <= ASTEROID_MIN_RADIUS:
            return ASTEROID_SMALL_SPEED

        if self.radius <= ASTEROID_MIN_RADIUS * 2:
            return ASTEROID_MEDIUM_SPEED

        return ASTEROID_LARGE_SPEED

    def draw(
        self, screen: pygame.Surface, offset: pygame.Vector2 = pygame.Vector2(0, 0)
    ) -> None:
        if self.lifetime <= ASTEROID_BLINK_TIME:
            blink = int(self.lifetime / ASTEROID_BLINK_INTERVAL)

            if blink % 2 == 0:
                return

        image = pygame.transform.rotate(
            self.image,
            self.rotation,
        )

        rect = image.get_rect(
            center=self.position - offset,
        )

        screen.blit(image, rect)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

        self.rotation += self.rotation_speed * dt

        self.lifetime -= dt

        if self.lifetime <= 0:
            self.kill()

    def split(self) -> None:
        # Load sound only when an asteroid is destroyed.
        # SpriteManager caches it after the first load.
        destroy_sound = SpriteManager.get_sound("destroyed")

        if destroy_sound:
            destroy_sound.play()

        self.kill()

        # Small asteroids disappear without splitting.
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
            self.difficulty,
        )

        second = Asteroid(
            self.position.x,
            self.position.y,
            new_radius,
            self.difficulty,
        )

        first.velocity = first_velocity * 1.2
        second.velocity = second_velocity * 1.2
