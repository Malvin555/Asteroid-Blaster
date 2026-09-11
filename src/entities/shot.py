import pygame

from constants import SHOT_RADIUS
from entities.circle_shape import CircleShape
from utils.sprite_manager import SpriteManager


class Shot(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)

        self.image = SpriteManager.get_image("shot")

        self.shoot_sound = SpriteManager.get_sound("shoot")

        if self.shoot_sound:
            self.shoot_sound.play()

    def draw(self, screen: pygame.Surface, offset: pygame.Vector2 = pygame.Vector2(0, 0)) -> None:
        if self.image:
            rect = self.image.get_rect(center=self.position - offset)
            screen.blit(self.image, rect)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
