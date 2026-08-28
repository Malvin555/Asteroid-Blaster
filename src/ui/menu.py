import pygame

from utils.assets import AssetLoader


class Menu:
    ITEMS = (
        "START",
        "DIFFICULTY",
        "EXIT",
    )

    DIFFICULTIES = (
        "EASY",
        "NORMAL",
        "HARD",
    )

    def __init__(self, font: pygame.font.Font) -> None:
        self.font = font

        self.logo = AssetLoader.get_image("assets/images/logo.png")

        self.button = AssetLoader.get_image("assets/images/button.png")

        self.button_selected = AssetLoader.get_image("assets/images/button_active.png")

        self.background = AssetLoader.get_image("assets/images/menu_background.png")

        self.selected = 0
        self.difficulty_index = 1

    def handle_event(
        self,
        event: pygame.event.Event,
        screen: pygame.Surface,
    ) -> str | None:

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected -= 1

                if self.selected < 0:
                    self.selected = len(self.ITEMS) - 1

            elif event.key == pygame.K_DOWN:
                self.selected += 1

                if self.selected >= len(self.ITEMS):
                    self.selected = 0

            elif event.key == pygame.K_LEFT:
                self._change_difficulty(-1)

            elif event.key == pygame.K_RIGHT:
                self._change_difficulty(1)

            elif event.key == pygame.K_RETURN:
                return self._select_item()

        elif event.type == pygame.MOUSEMOTION:
            self._handle_hover(
                event.pos,
                screen,
            )

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self._handle_pointer(
                    event.pos,
                    screen,
                )

        elif event.type == pygame.FINGERDOWN:
            position = (
                int(event.x * screen.get_width()),
                int(event.y * screen.get_height()),
            )

            return self._handle_pointer(
                position,
                screen,
            )

        return None

    def _handle_hover(
        self,
        position: tuple[int, int],
        screen: pygame.Surface,
    ) -> None:

        for index in range(len(self.ITEMS)):
            center_y = int(screen.get_height() * (0.48 + index * 0.12))

            rect = self._get_button_rect(
                screen,
                center_y,
            )

            if rect.collidepoint(position):
                self.selected = index
                return

    def _handle_pointer(
        self,
        position: tuple[int, int],
        screen: pygame.Surface,
    ) -> str | None:

        for index, item in enumerate(self.ITEMS):
            center_y = int(screen.get_height() * (0.48 + index * 0.12))

            rect = self._get_button_rect(
                screen,
                center_y,
            )

            if not rect.collidepoint(position):
                continue

            self.selected = index

            if item == "DIFFICULTY":
                self._change_difficulty(1)
                return None

            return self._select_item()

        return None

    def _select_item(self) -> str | None:

        item = self.ITEMS[self.selected]

        if item == "START":
            return "START"

        if item == "EXIT":
            return "EXIT"

        return None

    def _change_difficulty(
        self,
        direction: int,
    ) -> None:

        if self.ITEMS[self.selected] != "DIFFICULTY":
            return

        self.difficulty_index += direction

        if self.difficulty_index < 0:
            self.difficulty_index = len(self.DIFFICULTIES) - 1

        elif self.difficulty_index >= len(self.DIFFICULTIES):
            self.difficulty_index = 0

    def get_difficulty(self) -> str:
        return self.DIFFICULTIES[self.difficulty_index]

    def draw(
        self,
        screen: pygame.Surface,
    ) -> None:

        width, height = screen.get_size()

        self._draw_background(
            screen,
            width,
            height,
        )

        self._draw_logo(
            screen,
            width,
            height,
        )

        self._draw_buttons(
            screen,
            width,
            height,
        )

    def _draw_background(
        self,
        screen: pygame.Surface,
        width: int,
        height: int,
    ) -> None:

        if self.background is None:
            screen.fill("black")
            return

        background = pygame.transform.scale(
            self.background,
            (width, height),
        )

        screen.blit(
            background,
            (0, 0),
        )

    def _draw_logo(
        self,
        screen: pygame.Surface,
        width: int,
        height: int,
    ) -> None:

        center_x = width // 2

        if self.logo is not None:
            logo_width = int(width * 0.55)

            logo_width = min(
                logo_width,
                700,
            )

            scale = logo_width / self.logo.get_width()

            logo_height = int(self.logo.get_height() * scale)

            logo = pygame.transform.smoothscale(
                self.logo,
                (
                    logo_width,
                    logo_height,
                ),
            )

            rect = logo.get_rect(
                center=(
                    center_x,
                    int(height * 0.25),
                ),
            )

            screen.blit(
                logo,
                rect,
            )

            return

        title = self.font.render(
            "ASTEROID BLASTER",
            True,
            "white",
        )

        screen.blit(
            title,
            title.get_rect(
                center=(
                    center_x,
                    int(height * 0.25),
                ),
            ),
        )

    def _draw_buttons(
        self,
        screen: pygame.Surface,
        width: int,
        height: int,
    ) -> None:

        center_x = width // 2

        positions = (
            0.48,
            0.60,
            0.72,
        )

        for index, item in enumerate(self.ITEMS):
            selected = index == self.selected

            if item == "DIFFICULTY":
                text = self._difficulty_text()
            else:
                text = item

            self._draw_button(
                screen,
                text,
                center_x,
                int(height * positions[index]),
                selected,
            )

    def _get_button_rect(
        self,
        screen: pygame.Surface,
        center_y: int,
    ) -> pygame.Rect:

        button_width = int(screen.get_width() * 0.45)

        button_height = int(screen.get_height() * 0.12)

        button_width = max(
            300,
            min(button_width, 600),
        )

        button_height = max(
            55,
            min(button_height, 90),
        )

        rect = pygame.Rect(
            0,
            0,
            button_width,
            button_height,
        )

        rect.center = (
            screen.get_width() // 2,
            center_y,
        )

        return rect

    def _draw_button(
        self,
        screen: pygame.Surface,
        text: str,
        center_x: int,
        center_y: int,
        selected: bool,
    ) -> None:

        button = self.button_selected if selected else self.button

        button_rect = self._get_button_rect(
            screen,
            center_y,
        )

        if button is not None:
            scaled_button = pygame.transform.smoothscale(
                button,
                button_rect.size,
            )

            screen.blit(
                scaled_button,
                button_rect,
            )

        # Same text style as before
        text_color = "yellow" if selected else "white"

        surface = self.font.render(
            text,
            True,
            text_color,
        )

        text_rect = surface.get_rect(
            center=(
                center_x,
                center_y,
            ),
        )

        screen.blit(
            surface,
            text_rect,
        )

    def _difficulty_text(self) -> str:
        return f"< {self.get_difficulty()} >"
