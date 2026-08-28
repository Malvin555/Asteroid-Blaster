import pygame

from constants import (
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
)
from entities.circleshape import CircleShape
from entities.shot import Shot
from utils.assets import AssetLoader


class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)

        self.rotation = 0
        self.shoot_cooldown = 0

        self.image = AssetLoader.get_image("assets/images/player.png")

    def draw(self, screen: pygame.Surface) -> None:
        image = pygame.transform.rotate(
            self.image,
            -self.rotation,
        )

        rect = image.get_rect(
            center=self.position,
        )

        screen.blit(image, rect)

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt: float) -> None:
        direction = pygame.Vector2(0, 1).rotate(self.rotation)

        self.position += direction * PLAYER_SPEED * dt

    def shoot(self) -> None:
        if self.shoot_cooldown > 0:
            return

        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

        shot = Shot(
            self.position.x,
            self.position.y,
        )

        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def update(self, dt: float) -> None:
        self.shoot_cooldown -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(-dt)

        if keys[pygame.K_SPACE]:
            self.shoot()

        self.wrap_screen()
