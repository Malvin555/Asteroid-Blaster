from enum import Enum, auto

import pygame

from constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from entities.asteroid import Asteroid
from entities.asteroidfield import AsteroidField
from entities.player import Player
from entities.shot import Shot
from ui.menu import Menu
from utils.assets import AssetLoader
from utils.logger import log_event, log_state


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

        self.font = pygame.font.Font(
            "assets/fonts/PressStart2P-Regular.ttf",
            24,
        )

        self.background = AssetLoader.get_image("assets/images/background.png")

        self.dt = 0.0
        self.running = True
        self.score = 0
        self.state = GameState.MENU

        self.menu = Menu(self.font)

        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()

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

        self.updatable.empty()
        self.drawable.empty()
        self.asteroids.empty()
        self.shots.empty()

        width, height = self.screen.get_size()

        self.player = Player(
            width / 2,
            height / 2,
        )

        self.asteroid_field = AsteroidField()

        difficulty = self.menu.get_difficulty()

        print(f"Starting game on {difficulty} difficulty")

        self.state = GameState.PLAYING

    def update(self) -> None:
        self.updatable.update(self.dt)

    def handle_collisions(self) -> None:
        for asteroid in self.asteroids:
            self._handle_player_collision(asteroid)
            self._handle_shot_collisions(asteroid)

    def _handle_player_collision(
        self,
        asteroid: Asteroid,
    ) -> None:
        if not asteroid.collides_with(self.player):
            return

        log_event("player_hit")

        print(f"Score: {self.score}")
        print("Game over!")

        self.state = GameState.GAME_OVER

    def _handle_shot_collisions(
        self,
        asteroid: Asteroid,
    ) -> None:
        for shot in self.shots:
            if not asteroid.collides_with(shot):
                continue

            log_event("asteroid_shot")

            self.score += asteroid.score

            asteroid.split()
            shot.kill()

            break

    def draw(self) -> None:
        if self.state == GameState.MENU:
            self._draw_menu()

        elif self.state == GameState.PLAYING:
            self._draw_game()

        elif self.state == GameState.PAUSED:
            self._draw_game()
            self._draw_pause_overlay()

        elif self.state == GameState.GAME_OVER:
            self._draw_game_over()

        pygame.display.flip()

    def _draw_menu(self) -> None:
        self._draw_background()
        self.menu.draw(self.screen)

    def _draw_game(self) -> None:
        self._draw_background()
        self._draw_game_objects()
        self._draw_score()
        self._draw_pause_button()

    def _pause_button_rect(self) -> pygame.Rect:
        width, height = self.screen.get_size()

        button_width = max(
            120,
            min(int(width * 0.12), 180),
        )

        button_height = max(
            50,
            min(int(height * 0.09), 70),
        )

        margin = max(
            16,
            int(width * 0.02),
        )

        return pygame.Rect(
            width - button_width - margin,
            margin,
            button_width,
            button_height,
        )

    def _draw_pause_button(self) -> None:
        if self.state == GameState.PLAYING:
            button = self.menu.button
            text = "PAUSE"
            text_color = "white"
        else:
            button = self.menu.button_selected
            text = "RESUME"
            text_color = "yellow"

        rect = self._pause_button_rect()

        if button is not None:
            scaled_button = pygame.transform.smoothscale(
                button,
                rect.size,
            )

            self.screen.blit(
                scaled_button,
                rect,
            )

        surface = self.font.render(
            text,
            True,
            text_color,
        )

        text_rect = surface.get_rect(
            center=rect.center,
        )

        self.screen.blit(
            surface,
            text_rect,
        )

    def _draw_pause_overlay(self) -> None:
        width, height = self.screen.get_size()

        overlay = pygame.Surface(
            (width, height),
            pygame.SRCALPHA,
        )

        overlay.fill(
            (0, 0, 0, 150),
        )

        self.screen.blit(
            overlay,
            (0, 0),
        )

        title = self.font.render(
            "PAUSED",
            True,
            "yellow",
        )

        text = self.font.render(
            "PRESS ESC TO RESUME",
            True,
            "white",
        )

        self.screen.blit(
            title,
            title.get_rect(
                center=(
                    width // 2,
                    int(height * 0.42),
                ),
            ),
        )

        self.screen.blit(
            text,
            text.get_rect(
                center=(
                    width // 2,
                    int(height * 0.55),
                ),
            ),
        )

        self._draw_pause_button()

    def _draw_game_over(self) -> None:
        self._draw_background()

        width, height = self.screen.get_size()

        game_over = self.font.render(
            "GAME OVER",
            True,
            "white",
        )

        score = self.font.render(
            f"SCORE: {self.score}",
            True,
            "white",
        )

        restart = self.font.render(
            "PRESS ENTER",
            True,
            "white",
        )

        self.screen.blit(
            game_over,
            game_over.get_rect(
                center=(
                    width // 2,
                    int(height * 0.40),
                ),
            ),
        )

        self.screen.blit(
            score,
            score.get_rect(
                center=(
                    width // 2,
                    int(height * 0.50),
                ),
            ),
        )

        self.screen.blit(
            restart,
            restart.get_rect(
                center=(
                    width // 2,
                    int(height * 0.60),
                ),
            ),
        )

    def _draw_background(self) -> None:
        if self.background is None:
            self.screen.fill("black")
            return

        screen_size = self.screen.get_size()

        background = pygame.transform.scale(
            self.background,
            screen_size,
        )

        self.screen.blit(
            background,
            (0, 0),
        )

    def _draw_game_objects(self) -> None:
        for obj in self.drawable:
            obj.draw(self.screen)

    def _draw_score(self) -> None:
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            "white",
        )

        self.screen.blit(
            score_text,
            (20, 20),
        )
