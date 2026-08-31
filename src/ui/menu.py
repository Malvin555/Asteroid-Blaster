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

    LOGO_Y = 0.23
    BUTTON_START_Y = 0.48
    BUTTON_SPACING = 0.13

    def __init__(self, font: pygame.font.Font) -> None:
        self.font = font

        self.logo = AssetLoader.get_image("assets/images/logo.png")

        self.button = AssetLoader.get_image("assets/images/button.png")

        self.button_selected = AssetLoader.get_image("assets/images/button_active.png")

        self.background = AssetLoader.get_image("assets/images/menu_background.png")

        self.selected = 0
        self.difficulty_index = 1

        self.hover_scale = 1.0
        self.animation_speed = 8.0

    def handle_event(
        self,
        event: pygame.event.Event,
        screen: pygame.Surface,
    ) -> str | None:

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.ITEMS)

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.ITEMS)

            elif event.key == pygame.K_LEFT:
                self._change_difficulty(-1)

            elif event.key == pygame.K_RIGHT:
                self._change_difficulty(1)

            elif event.key in (
                pygame.K_RETURN,
                pygame.K_SPACE,
            ):
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

    def update(
        self,
        dt: float,
    ) -> None:

        target = 1.06 if self.selected >= 0 else 1.0

        self.hover_scale += (target - self.hover_scale) * self.animation_speed * dt

        self.hover_scale = max(
            1.0,
            min(
                self.hover_scale,
                1.06,
            ),
        )

    def _handle_hover(
        self,
        position: tuple[int, int],
        screen: pygame.Surface,
    ) -> None:

        for index in range(len(self.ITEMS)):
            rect = self._get_item_rect(
                screen,
                index,
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
            rect = self._get_item_rect(
                screen,
                index,
            )

            if not rect.collidepoint(position):
                continue

            self.selected = index

            if item == "DIFFICULTY":
                self._change_difficulty(1)

                return None

            return self._select_item()

        return None

    def _select_item(
        self,
    ) -> str | None:

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

        self.difficulty_index = (self.difficulty_index + direction) % len(
            self.DIFFICULTIES
        )

    def get_difficulty(
        self,
    ) -> str:

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

        self._draw_dark_overlay(
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
        )

    def _draw_background(
        self,
        screen: pygame.Surface,
        width: int,
        height: int,
    ) -> None:

        if self.background is None:
            screen.fill((10, 15, 30))

            return

        image_width = self.background.get_width()

        image_height = self.background.get_height()

        scale = max(
            width / image_width,
            height / image_height,
        )

        scaled_width = int(image_width * scale)

        scaled_height = int(image_height * scale)

        background = pygame.transform.smoothscale(
            self.background,
            (
                scaled_width,
                scaled_height,
            ),
        )

        x = (width - scaled_width) // 2

        y = (height - scaled_height) // 2

        screen.blit(
            background,
            (
                x,
                y,
            ),
        )

    def _draw_dark_overlay(
        self,
        screen: pygame.Surface,
        width: int,
        height: int,
    ) -> None:

        overlay = pygame.Surface(
            (
                width,
                height,
            ),
            pygame.SRCALPHA,
        )

        overlay.fill(
            (
                0,
                0,
                0,
                70,
            )
        )

        screen.blit(
            overlay,
            (
                0,
                0,
            ),
        )

    def _draw_logo(
        self,
        screen: pygame.Surface,
        width: int,
        height: int,
    ) -> None:

        center_x = width // 2

        if self.logo is not None:
            logo_width = int(width * 0.58)

            logo_width = max(
                280,
                min(
                    logo_width,
                    750,
                ),
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
                    int(height * self.LOGO_Y),
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

        rect = title.get_rect(
            center=(
                center_x,
                int(height * self.LOGO_Y),
            ),
        )

        screen.blit(
            title,
            rect,
        )

    def _get_item_center_y(
        self,
        screen: pygame.Surface,
        index: int,
    ) -> int:

        height = screen.get_height()

        position = self.BUTTON_START_Y + index * self.BUTTON_SPACING

        return int(height * position)

    def _get_item_rect(
        self,
        screen: pygame.Surface,
        index: int,
    ) -> pygame.Rect:

        width = screen.get_width()
        height = screen.get_height()

        button_width = int(width * 0.46)

        button_height = int(height * 0.105)

        button_width = max(
            280,
            min(
                button_width,
                620,
            ),
        )

        button_height = max(
            52,
            min(
                button_height,
                90,
            ),
        )

        rect = pygame.Rect(
            0,
            0,
            button_width,
            button_height,
        )

        rect.center = (
            width // 2,
            self._get_item_center_y(
                screen,
                index,
            ),
        )

        return rect

    def _draw_buttons(
        self,
        screen: pygame.Surface,
    ) -> None:

        for index, item in enumerate(self.ITEMS):
            selected = index == self.selected

            if item == "DIFFICULTY":
                text = self._difficulty_text()

            else:
                text = item

            self._draw_button(
                screen,
                text,
                index,
                selected,
            )

    def _draw_button(
        self,
        screen: pygame.Surface,
        text: str,
        index: int,
        selected: bool,
    ) -> None:

        button_rect = self._get_item_rect(
            screen,
            index,
        )

        button = self.button_selected if selected else self.button

        if selected:
            scale = self.hover_scale

            animated_size = (
                int(button_rect.width * scale),
                int(button_rect.height * scale),
            )

            draw_rect = pygame.Rect(
                0,
                0,
                *animated_size,
            )

            draw_rect.center = button_rect.center

        else:
            draw_rect = button_rect

        if button is not None:
            scaled_button = pygame.transform.smoothscale(
                button,
                draw_rect.size,
            )

            screen.blit(
                scaled_button,
                draw_rect,
            )

        else:
            # Fallback button
            pygame.draw.rect(
                screen,
                (
                    70,
                    80,
                    110,
                )
                if not selected
                else (
                    120,
                    100,
                    40,
                ),
                draw_rect,
                border_radius=12,
            )

        # Text
        text_color = "yellow" if selected else "white"

        text_surface = self.font.render(
            text,
            True,
            text_color,
        )

        text_rect = text_surface.get_rect(center=draw_rect.center)

        screen.blit(
            text_surface,
            text_rect,
        )

    def _difficulty_text(
        self,
    ) -> str:

        return f"< {self.get_difficulty()} >"
