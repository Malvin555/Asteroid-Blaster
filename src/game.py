from enum import Enum, auto

import pygame

from constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from entities.asteroid import Asteroid
from entities.asteroidfield import AsteroidField
from entities.player import Player
from entities.shot import Shot
from ui.menu import Menu
from utils.logger import log_event, log_state


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
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
        self._create_game_objects()

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

    def _create_game_objects(self) -> None:
        self.player = Player(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
        )

        self.asteroid_field = AsteroidField()

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

            if event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_RETURN:
                        self.state = GameState.PLAYING

    def update(self) -> None:
        self.updatable.update(self.dt)

    def handle_collisions(self) -> None:
        for asteroid in self.asteroids:
            self._handle_player_collision(asteroid)
            self._handle_shot_collisions(asteroid)

    def _handle_player_collision(self, asteroid: Asteroid) -> None:
        if not asteroid.collides_with(self.player):
            return

        log_event("player_hit")

        print(f"Score: {self.score}")
        print("Game over!")

        self.state = GameState.GAME_OVER

    def _handle_shot_collisions(self, asteroid: Asteroid) -> None:
        for shot in self.shots:
            if not asteroid.collides_with(shot):
                continue

            log_event("asteroid_shot")

            self.score += asteroid.score

            asteroid.split()
            shot.kill()

    def draw(self) -> None:
        if self.state == GameState.MENU:
            self.menu.draw(self.screen)

        elif self.state == GameState.PLAYING:
            self._draw_game()

        elif self.state == GameState.GAME_OVER:
            self._draw_game_over()

        pygame.display.flip()

    def _draw_game(self) -> None:
        self.screen.fill("black")

        self._draw_game_objects()
        self._draw_score()

    def _draw_game_over(self) -> None:
        self.screen.fill("black")

        game_over = self.font.render(
            "GAME OVER",
            True,
            "white",
        )

        self.screen.blit(
            game_over,
            game_over.get_rect(
                center=(
                    SCREEN_WIDTH / 2,
                    SCREEN_HEIGHT / 2,
                )
            ),
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
