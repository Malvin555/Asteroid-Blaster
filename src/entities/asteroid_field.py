import random
import pygame

from constants import (
    ASTEROID_KINDS,
    ASTEROID_MAX_RADIUS,
    ASTEROID_MIN_RADIUS,
    ASTEROID_SPAWN_RATE_SECONDS,
    DIFFICULTY_MODIFIERS,
)
from entities.asteroid import Asteroid


class AsteroidField(pygame.sprite.Sprite):
    containers: pygame.sprite.Group

    def __init__(self, difficulty: str = "NORMAL") -> None:
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.difficulty = difficulty
        self.camera_rect = pygame.Rect(0, 0, 0, 0) # Set from game.py

    def spawn(
        self, radius: float, position: pygame.Vector2, velocity: pygame.Vector2
    ) -> None:
        asteroid = Asteroid(position.x, position.y, radius, self.difficulty)
        asteroid.velocity = velocity

    def update(self, dt: float) -> None:
        self.spawn_timer += dt
        
        rate_mult = DIFFICULTY_MODIFIERS.get(self.difficulty, {}).get("spawn_rate", 1.0)
        current_spawn_rate = ASTEROID_SPAWN_RATE_SECONDS * rate_mult
        
        if self.spawn_timer > current_spawn_rate:
            self.spawn_timer = 0

            # Spawn just outside the camera rect
            margin = ASTEROID_MAX_RADIUS
            edges = [
                # Top edge
                (pygame.Vector2(0, 1), lambda: pygame.Vector2(random.uniform(self.camera_rect.left - margin, self.camera_rect.right + margin), self.camera_rect.top - margin)),
                # Bottom edge
                (pygame.Vector2(0, -1), lambda: pygame.Vector2(random.uniform(self.camera_rect.left - margin, self.camera_rect.right + margin), self.camera_rect.bottom + margin)),
                # Left edge
                (pygame.Vector2(1, 0), lambda: pygame.Vector2(self.camera_rect.left - margin, random.uniform(self.camera_rect.top - margin, self.camera_rect.bottom + margin))),
                # Right edge
                (pygame.Vector2(-1, 0), lambda: pygame.Vector2(self.camera_rect.right + margin, random.uniform(self.camera_rect.top - margin, self.camera_rect.bottom + margin))),
            ]

            edge = random.choice(edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1]()
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
