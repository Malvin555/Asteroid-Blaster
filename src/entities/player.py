import pygame

from constants import (
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    PLAYER_BOOST_MAX_ENERGY,
    PLAYER_BOOST_DRAIN_RATE,
    PLAYER_BOOST_RECHARGE_RATE,
    PLAYER_BOOST_MULTIPLIER,
)
from entities.circle_shape import CircleShape
from entities.shot import Shot
from utils.sprite_manager import SpriteManager


class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)

        self.rotation = 0
        self.shoot_cooldown = 0
        
        # Boost System
        self.boost_energy = PLAYER_BOOST_MAX_ENERGY
        self.is_boosting = False
        
        # Powerup System
        self.rapid_fire_timer = 0.0
        self.shield_timer = 0.0

        self.image = SpriteManager.get_image("player")

    def draw(self, screen: pygame.Surface, offset: pygame.Vector2 = pygame.Vector2(0, 0)) -> None:
        image = pygame.transform.rotate(
            self.image,
            -self.rotation,
        )

        rect = image.get_rect(
            center=self.position - offset,
        )

        screen.blit(image, rect)
        
        # Draw Shield
        if self.shield_timer > 0:
            pygame.draw.circle(screen, (100, 200, 255), self.position - offset, self.radius + 10, 3)

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt: float) -> None:
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        
        speed = PLAYER_SPEED
        if self.is_boosting:
            speed *= PLAYER_BOOST_MULTIPLIER

        self.position += direction * speed * dt

    def shoot(self) -> None:
        if self.shoot_cooldown > 0:
            return

        cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        if self.rapid_fire_timer > 0:
            cooldown *= 0.3 # 3x faster shooting

        self.shoot_cooldown = cooldown

        shot = Shot(
            self.position.x,
            self.position.y,
        )

        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def update(self, dt: float) -> None:
        self.shoot_cooldown -= dt
        
        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer -= dt
            
        if self.shield_timer > 0:
            self.shield_timer -= dt

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        # Handle Boost
        is_moving = keys[pygame.K_w] or keys[pygame.K_s]
        if keys[pygame.K_SPACE] and self.boost_energy > 0 and is_moving:
            self.is_boosting = True
            self.boost_energy = max(0, self.boost_energy - PLAYER_BOOST_DRAIN_RATE * dt)
        else:
            self.is_boosting = False
            self.boost_energy = min(PLAYER_BOOST_MAX_ENERGY, self.boost_energy + PLAYER_BOOST_RECHARGE_RATE * dt)

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(-dt)

        # Left mouse click or Enter to shoot
        if mouse[0] or keys[pygame.K_RETURN]:
            self.shoot()
