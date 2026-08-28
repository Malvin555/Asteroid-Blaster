import pygame

from constants import SHOT_RADIUS
from entities.circleshape import CircleShape
from utils.assets import AssetLoader


class Shot(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)

        self.image = AssetLoader.get_image("assets/images/shot.png")

    def draw(self, screen: pygame.Surface) -> None:
        rect = self.image.get_rect(center=self.position)
        screen.blit(self.image, rect)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
