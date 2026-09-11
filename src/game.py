from enum import Enum, auto

import pygame

from constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, POWERUP_SPAWN_RATE_SECONDS, PLAYER_BOOST_MAX_ENERGY
from entities.asteroid import Asteroid
from entities.asteroid_field import AsteroidField
from entities.player import Player
from entities.shot import Shot
from entities.power_up import PowerUp
from ui.menu import Menu
from ui.hud import HUD
from systems.camera import Camera
from utils.sprite_manager import SpriteManager
from utils.high_score_manager import HighScoreManager
from utils.logger import log_event, log_state
import random


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.RESIZABLE,
        )

        self.clock = pygame.time.Clock()

        self.font = SpriteManager.get_font("main", 24) or pygame.font.SysFont("Arial", 24)
        
        self.background = SpriteManager.get_image("background")

        self.dt = 0.0
        self.running = True
        self.score = 0
        self.high_score = HighScoreManager.load_high_score()
        self.powerup_timer = 0.0
        self.state = GameState.MENU

        self.menu = Menu(self.font)
        self.hud = HUD(self.font)
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()

        self._setup_containers()

    def _setup_containers(self) -> None:
        Player.containers = (
            self.updatable,
            self.drawable,
        )

        Asteroid.containers = (
            self.asteroids,
            self.updatable,
            self.drawable,
        )

        Shot.containers = (
            self.shots,
            self.updatable,
            self.drawable,
        )
        
        PowerUp.containers = (
            self.power_ups,
            self.updatable,
            self.drawable,
        )

        AsteroidField.containers = self.updatable

    def run(self) -> None:
        print("Starting Asteroids")
        print(f"Screen width: {SCREEN_WIDTH}")
        print(f"Screen height: {SCREEN_HEIGHT}")

        while self.running:
            log_state()

            self.handle_events()

            if self.state == GameState.PLAYING:
                self.update()
                self.handle_collisions()

            self.draw()

            self.dt = self.clock.tick(FPS) / 1000

        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                continue

            if event.type == pygame.VIDEORESIZE:
                self.camera.width = event.w
                self.camera.height = event.h
                self.camera.camera_rect.size = (event.w, event.h)

            if self.state == GameState.MENU:
                self._handle_menu_event(event)

            elif self.state == GameState.PLAYING:
                self._handle_game_event(event)

            elif self.state == GameState.PAUSED:
                self._handle_pause_event(event)

            elif self.state == GameState.GAME_OVER:
                self._handle_game_over_event(event)

    def _handle_menu_event(
        self,
        event: pygame.event.Event,
    ) -> None:
        action = self.menu.handle_event(
            event,
            self.screen,
        )

        if action == "START":
            self.start_game()

        elif action == "EXIT":
            self.running = False

    def _handle_game_event(
        self,
        event: pygame.event.Event,
    ) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.pause_game()
                return

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self._pause_button_rect().collidepoint(event.pos):
                    self.pause_game()

        elif event.type == pygame.FINGERDOWN:
            width, height = self.screen.get_size()

            position = (
                int(event.x * width),
                int(event.y * height),
            )

            if self._pause_button_rect().collidepoint(position):
                self.pause_game()

    def _handle_pause_event(
        self,
        event: pygame.event.Event,
    ) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (
                pygame.K_ESCAPE,
                pygame.K_RETURN,
            ):
                self.resume_game()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self._pause_button_rect().collidepoint(event.pos):
                    self.resume_game()

        elif event.type == pygame.FINGERDOWN:
            width, height = self.screen.get_size()

            position = (
                int(event.x * width),
                int(event.y * height),
            )

            if self._pause_button_rect().collidepoint(position):
                self.resume_game()

    def _handle_game_over_event(
        self,
        event: pygame.event.Event,
    ) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.state = GameState.MENU

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.state = GameState.MENU

        elif event.type == pygame.FINGERDOWN:
            self.state = GameState.MENU

    def pause_game(self) -> None:
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED

    def resume_game(self) -> None:
        if self.state == GameState.PAUSED:
            self.state = GameState.PLAYING

    def start_game(self) -> None:
        self.score = 0
        self.powerup_timer = 0.0

        self.updatable.empty()
        self.drawable.empty()
        self.asteroids.empty()
        self.shots.empty()
        self.power_ups.empty()

        width, height = self.screen.get_size()

        self.player = Player(
            width / 2,
            height / 2,
        )

        difficulty = self.menu.get_difficulty()
        self.asteroid_field = AsteroidField(difficulty)

        print(f"Starting game on {difficulty} difficulty")

        self.state = GameState.PLAYING

    def update(self) -> None:
        self.updatable.update(self.dt)
        if hasattr(self, 'player'):
            self.camera.update(self.player.position, self.dt)
        if hasattr(self, 'asteroid_field'):
            self.asteroid_field.camera_rect = self.camera.camera_rect
            
        # Spawn Powerups
        self.powerup_timer += self.dt
        if self.powerup_timer > POWERUP_SPAWN_RATE_SECONDS:
            self.powerup_timer = 0.0
            
            # Spawn just outside camera view
            margin = 50
            camera = self.camera.camera_rect
            edges = [
                (pygame.Vector2(0, 1), lambda: pygame.Vector2(random.uniform(camera.left - margin, camera.right + margin), camera.top - margin)),
                (pygame.Vector2(0, -1), lambda: pygame.Vector2(random.uniform(camera.left - margin, camera.right + margin), camera.bottom + margin)),
                (pygame.Vector2(1, 0), lambda: pygame.Vector2(camera.left - margin, random.uniform(camera.top - margin, camera.bottom + margin))),
                (pygame.Vector2(-1, 0), lambda: pygame.Vector2(camera.right + margin, random.uniform(camera.top - margin, camera.bottom + margin))),
            ]
            edge = random.choice(edges)
            pos = edge[1]()
            ptype = random.choice(["shield", "rapid_fire"])
            PowerUp(pos.x, pos.y, ptype)

    def handle_collisions(self) -> None:
        # Check powerup collisions
        if hasattr(self, 'player'):
            for power_up in self.power_ups:
                if self.player.collides_with(power_up):
                    if power_up.type_name == "shield":
                        self.player.shield_timer = 15.0
                    elif power_up.type_name == "rapid_fire":
                        self.player.rapid_fire_timer = 10.0
                    power_up.kill()
                    log_event(f"powerup_{power_up.type_name}")

        for asteroid in self.asteroids:
            self._handle_player_collision(asteroid)
            self._handle_shot_collisions(asteroid)

    def _handle_player_collision(
        self,
        asteroid: Asteroid,
    ) -> None:
        if not asteroid.collides_with(self.player):
            return
            
        if getattr(self.player, "shield_timer", 0) > 0:
            asteroid.kill()
            # Disable shield when hit
            self.player.shield_timer = 0
            log_event("shield_absorbed_hit")
            return

        log_event("player_hit")

        print(f"Score: {self.score}")
        print("Game over!")
        
        HighScoreManager.save_high_score(self.score)
        if self.score > self.high_score:
            self.high_score = self.score

        self.state = GameState.GAME_OVER

    def _handle_shot_collisions(
        self,
        asteroid: Asteroid,
    ) -> None:
        for shot in self.shots:
            if not asteroid.collides_with(shot):
                continue

            log_event("asteroid_shot")

            # Apply difficulty multiplier
            difficulty = self.menu.get_difficulty()
            from constants import DIFFICULTY_MODIFIERS
            score_mult = DIFFICULTY_MODIFIERS.get(difficulty, {}).get("score_mult", 1.0)
            self.score += int(asteroid.score * score_mult)

            asteroid.split()
            shot.kill()

            break

    def draw(self) -> None:
        if self.state == GameState.MENU:
            self._draw_background(parallax=False)
            self.menu.draw(self.screen)

        elif self.state == GameState.PLAYING:
            self._draw_game()

        elif self.state == GameState.PAUSED:
            self._draw_game()
            self.hud.draw_pause_overlay(
                self.screen, self._pause_button_rect(), self.menu.button, self.menu.button_selected
            )

        elif self.state == GameState.GAME_OVER:
            self._draw_background(parallax=False)
            self.hud.draw_game_over(self.screen, self.score)

        pygame.display.flip()

    def _draw_game(self) -> None:
        self._draw_background(parallax=True)
        self._draw_game_objects()
        
        boost_energy = getattr(self.player, "boost_energy", 0) if hasattr(self, 'player') else 0
        shield_timer = getattr(self.player, "shield_timer", 0.0) if hasattr(self, 'player') else 0.0
        rapid_fire_timer = getattr(self.player, "rapid_fire_timer", 0.0) if hasattr(self, 'player') else 0.0
        
        self.hud.draw_score(self.screen, self.score, self.high_score, boost_energy, PLAYER_BOOST_MAX_ENERGY, shield_timer, rapid_fire_timer)
        
        is_paused = self.state == GameState.PAUSED
        button_image = self.menu.button_selected if is_paused else self.menu.button
        self.hud.draw_pause_button(self.screen, self._pause_button_rect(), button_image, is_paused)

    def _pause_button_rect(self) -> pygame.Rect:
        width, height = self.screen.get_size()

        button_width = max(120, min(int(width * 0.12), 180))
        button_height = max(50, min(int(height * 0.09), 70))
        margin = max(16, int(width * 0.02))

        return pygame.Rect(
            width - button_width - margin,
            margin,
            button_width,
            button_height,
        )

    def _draw_background(self, parallax: bool = False) -> None:
        if self.background is None:
            self.screen.fill("black")
            return

        screen_size = self.screen.get_size()
        bg_w, bg_h = screen_size
        background = pygame.transform.scale(self.background, screen_size)

        if not parallax:
            self.screen.blit(background, (0, 0))
            return

        # Parallax scrolling
        parallax_factor = 0.3
        offset_x = (self.camera.offset.x * parallax_factor) % bg_w
        offset_y = (self.camera.offset.y * parallax_factor) % bg_h

        # Draw 4 tiles to cover the screen wrapping
        self.screen.blit(background, (-offset_x, -offset_y))
        self.screen.blit(background, (-offset_x + bg_w, -offset_y))
        self.screen.blit(background, (-offset_x, -offset_y + bg_h))
        self.screen.blit(background, (-offset_x + bg_w, -offset_y + bg_h))

    def _draw_game_objects(self) -> None:
        offset = self.camera.offset
        for obj in self.drawable:
            obj.draw(self.screen, offset)
