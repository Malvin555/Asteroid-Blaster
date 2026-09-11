import random
import pygame

from constants import POWERUP_RADIUS, POWERUP_LIFETIME
from entities.circle_shape import CircleShape


class PowerUp(CircleShape):
    def __init__(self, x: float, y: float, type_name: str) -> None:
        super().__init__(x, y, POWERUP_RADIUS)
        self.type_name = type_name # 'shield' or 'rapid_fire'
        self.lifetime = POWERUP_LIFETIME
        self.velocity = pygame.Vector2(0, 1).rotate(random.uniform(0, 360)) * random.uniform(30, 70)
        
    def draw(self, screen: pygame.Surface, offset: pygame.Vector2 = pygame.Vector2(0, 0)) -> None:
        # Blink when about to expire
        if self.lifetime < 3.0:
            if int(self.lifetime * 10) % 2 == 0:
                return

        color = (100, 200, 255) if self.type_name == "shield" else (255, 100, 100)
        pygame.draw.circle(screen, color, self.position - offset, self.radius)
        
        # Inner symbol
        if self.type_name == "shield":
            pygame.draw.circle(screen, (255, 255, 255), self.position - offset, self.radius - 5, 2)
        else:
            pygame.draw.line(screen, (255, 255, 255), self.position - offset - pygame.Vector2(0, 5), self.position - offset + pygame.Vector2(0, 5), 2)
            pygame.draw.line(screen, (255, 255, 255), self.position - offset - pygame.Vector2(5, 0), self.position - offset + pygame.Vector2(5, 0), 2)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
