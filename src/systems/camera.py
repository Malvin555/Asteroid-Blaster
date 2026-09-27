import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH


class Camera:
    def __init__(self, width: int, height: int):
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def update(self, target_pos: pygame.Vector2, dt: float = 1.0):
        target_x = target_pos.x - self.width // 2
        target_y = target_pos.y - self.height // 2

        lerp_factor = 5.0 * dt
        self.camera_rect.x += int((target_x - self.camera_rect.x) * lerp_factor)
        self.camera_rect.y += int((target_y - self.camera_rect.y) * lerp_factor)

    def apply(self, entity_rect: pygame.Rect) -> pygame.Rect:
        return entity_rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def apply_pos(self, pos: pygame.Vector2) -> pygame.Vector2:
        return pygame.Vector2(pos.x - self.camera_rect.x, pos.y - self.camera_rect.y)

    @property
    def offset(self) -> pygame.Vector2:
        return pygame.Vector2(self.camera_rect.x, self.camera_rect.y)
