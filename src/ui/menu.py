import pygame


class Menu:
    def __init__(self, font: pygame.font.Font) -> None:
        self.font = font

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill("black")

        width, height = screen.get_size()

        title = self.font.render(
            "ASTEROIDS",
            True,
            "white",
        )

        start = self.font.render(
            "PRESS ENTER TO START",
            True,
            "white",
        )

        screen.blit(
            title,
            title.get_rect(
                center=(
                    width / 2,
                    height / 2 - 40,
                )
            ),
        )

        screen.blit(
            start,
            start.get_rect(
                center=(
                    width / 2,
                    height / 2 + 40,
                )
            ),
        )
