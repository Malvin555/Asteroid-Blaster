import pygame

class HUD:
    def __init__(self, font: pygame.font.Font):
        self.font = font

    def draw_score(self, screen: pygame.Surface, score: int, high_score: int, boost_energy: float, max_boost: float, shield_timer: float = 0.0, rapid_fire_timer: float = 0.0) -> None:
        # Score and High Score
        score_text = self.font.render(f"Score: {score}", True, "white")
        high_score_text = self.font.render(f"High Score: {high_score}", True, (200, 200, 200))
        
        screen.blit(score_text, (20, 20))
        screen.blit(high_score_text, (20, 60))

        # Boost Meter
        width, height = screen.get_size()
        bar_width = 200
        bar_height = 20
        x = 20
        y = height - 40
        
        pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
        fill_width = int(bar_width * (boost_energy / max_boost))
        pygame.draw.rect(screen, (0, 255, 255), (x, y, fill_width, bar_height))
        
        boost_label = self.font.render("BOOST", True, "white")
        boost_label = pygame.transform.scale(boost_label, (int(boost_label.get_width() * 0.6), int(boost_label.get_height() * 0.6)))
        screen.blit(boost_label, (x, y - 25))

        # Powerup Timers
        timer_y = 100
        small_font = pygame.font.Font(None, 24) if not self.font else self.font
        
        if shield_timer > 0:
            shield_text = small_font.render(f"Shield: {shield_timer:.1f}s", True, (100, 200, 255))
            shield_text = pygame.transform.scale(shield_text, (int(shield_text.get_width() * 0.6), int(shield_text.get_height() * 0.6)))
            screen.blit(shield_text, (20, timer_y))
            timer_y += 30

        if rapid_fire_timer > 0:
            rapid_text = small_font.render(f"Rapid Fire: {rapid_fire_timer:.1f}s", True, (255, 100, 100))
            rapid_text = pygame.transform.scale(rapid_text, (int(rapid_text.get_width() * 0.6), int(rapid_text.get_height() * 0.6)))
            screen.blit(rapid_text, (20, timer_y))

    def draw_pause_overlay(
        self, screen: pygame.Surface, pause_button_rect: pygame.Rect, 
        button_image: pygame.Surface | None, button_selected: pygame.Surface | None
    ) -> None:
        width, height = screen.get_size()

        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        title = self.font.render("PAUSED", True, "yellow")
        text = self.font.render("PRESS ESC TO RESUME", True, "white")

        screen.blit(title, title.get_rect(center=(width // 2, int(height * 0.42))))
        screen.blit(text, text.get_rect(center=(width // 2, int(height * 0.55))))

        self.draw_pause_button(screen, pause_button_rect, button_selected, True)

    def draw_pause_button(
        self, screen: pygame.Surface, rect: pygame.Rect, 
        button_image: pygame.Surface | None, is_paused: bool
    ) -> None:
        text = "RESUME" if is_paused else "PAUSE"
        text_color = "yellow" if is_paused else "white"

        if button_image is not None:
            scaled_button = pygame.transform.smoothscale(button_image, rect.size)
            screen.blit(scaled_button, rect)

        surface = self.font.render(text, True, text_color)
        text_rect = surface.get_rect(center=rect.center)
        screen.blit(surface, text_rect)

    def draw_game_over(self, screen: pygame.Surface, score: int) -> None:
        width, height = screen.get_size()

        game_over = self.font.render("GAME OVER", True, "white")
        score_text = self.font.render(f"SCORE: {score}", True, "white")
        restart = self.font.render("PRESS ENTER", True, "white")

        screen.blit(game_over, game_over.get_rect(center=(width // 2, int(height * 0.40))))
        screen.blit(score_text, score_text.get_rect(center=(width // 2, int(height * 0.50))))
        screen.blit(restart, restart.get_rect(center=(width // 2, int(height * 0.60))))
