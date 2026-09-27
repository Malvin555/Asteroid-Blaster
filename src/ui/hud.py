import pygame

from ui.styles import COLORS, SIZES, LAYOUT, BORDER_RADIUS


class HUD:
    def __init__(self, font: pygame.font.Font):
        self.font = font
        self.small_font = pygame.font.Font(None, SIZES["small_font"])

    def draw_score(
        self,
        screen: pygame.Surface,
        score: int,
        high_score: int,
        boost_energy: float,
        max_boost: float,
        shield_timer: float = 0.0,
        rapid_fire_timer: float = 0.0,
    ) -> None:

        score_text = self.font.render(f"Score: {score}", True, COLORS["white"])
        high_score_text = self.font.render(
            f"High Score: {high_score}", True, COLORS["light_gray"]
        )

        screen.blit(score_text, (SIZES["margin"], SIZES["margin"]))
        screen.blit(
            high_score_text, (SIZES["margin"], SIZES["margin"] * 3)
        )

        # Boost Meter
        width, height = screen.get_size()
        bar_width = SIZES["boost_bar_width"]
        bar_height = SIZES["boost_bar_height"]
        x = SIZES["margin"]
        y = height - SIZES["margin"] - bar_height

        pygame.draw.rect(
            screen, COLORS["boost_bar_bg"], (x, y, bar_width, bar_height)
        )
        fill_width = int(bar_width * (boost_energy / max_boost))
        pygame.draw.rect(
            screen, COLORS["boost_bar_fill"], (x, y, fill_width, bar_height)
        )

        boost_label = self.font.render("BOOST", True, COLORS["white"])
        boost_label = pygame.transform.scale(
            boost_label,
            (int(boost_label.get_width() * 0.6), int(boost_label.get_height() * 0.6)),
        )
        screen.blit(boost_label, (x, y - 25))

        # Powerup Timers
        timer_y = LAYOUT["hud"]["timer_y"]
        small_font = self.small_font

        if shield_timer > 0:
            shield_text = small_font.render(
                f"Shield: {shield_timer:.1f}s", True, COLORS["shield_color"]
            )
            shield_text = pygame.transform.scale(
                shield_text,
                (
                    int(shield_text.get_width() * 0.6),
                    int(shield_text.get_height() * 0.6),
                ),
            )
            screen.blit(shield_text, (SIZES["margin"], timer_y))
            timer_y += 30

        if rapid_fire_timer > 0:
            rapid_text = small_font.render(
                f"Rapid Fire: {rapid_fire_timer:.1f}s", True, COLORS["rapid_fire_color"]
            )
            rapid_text = pygame.transform.scale(
                rapid_text,
                (int(rapid_text.get_width() * 0.6), int(rapid_text.get_height() * 0.6)),
            )
            screen.blit(rapid_text, (SIZES["margin"], timer_y))

    def draw_keypad_overlay(
        self,
        screen: pygame.Surface,
        player,
        font: pygame.font.Font,
    ) -> None:
        """Draw WASD control overlay in corner."""
        width, height = screen.get_size()

        # Semi-transparent background
        overlay = pygame.Surface((200, 180), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (width - 210, height - 190))

        # Title
        title = font.render("CONTROLS", True, COLORS["white"])
        screen.blit(
            title,
            title.get_rect(
                center=(width - 110, height - 170)
            ),
        )

        # Controls text
        controls = [
            "W - Accelerate",
            "S - Reverse",
            "A - Rotate Left",
            "D - Rotate Right",
            "SPACE - Boost",
            "C / LEFT CLICK - Shoot",
            "LSHIFT / RCTRL - Boost (hold)",
        ]

        control_font = pygame.font.Font(None, 20)
        for i, text in enumerate(controls):
            surf = control_font.render(text, True, COLORS["white"])
            screen.blit(
                surf,
                (width - 200, height - 170 + 30 + i * 25),
            )