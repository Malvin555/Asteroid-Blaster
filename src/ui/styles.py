"""
UI Style System for Asteroids (Pygame-based).
 replaces CSS with Python dictionaries for colors, sizes, and layouts.
"""

# Color palette
COLORS = {
    "white": (255, 255, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "dark_gray": (50, 50, 50),
    "light_gray": (200, 200, 200),
    "red": (255, 100, 100),
    "green": (100, 200, 100),
    "boost_bar_bg": (50, 50, 50),
    "boost_bar_fill": (0, 255, 255),
    "shield_color": (100, 200, 255),
    "rapid_fire_color": (255, 100, 100),
    "button_bg": (70, 80, 110),
    "button_bg_selected": (120, 100, 40),
    "button_border": (120, 100, 40),
    "button_text_selected": "yellow",
    "button_text": "white",
    "menu_bg": (10, 15, 30),
    "menu_bg_alpha": 70,
    "pause_overlay": (0, 0, 0, 150),
    "game_over": "white",
}

# Size constants
SIZES = {
    "ui_font": 24,
    "small_font": 18,
    "button_width": 200,
    "button_height": 50,
    "button_padding_x": 20,
    "button_padding_y": 10,
    "margin": 24,
    "pause_button_width": 100,
    "pause_button_height": 40,
    "pause_margin": 20,
    "boost_bar_width": 200,
    "boost_bar_height": 20,
    "score_text_offset": 20,
}

# Layout constants
LAYOUT = {
    "hud": {
        "score_y": 20,
        "high_score_y": 60,
        "boost_bar_y": None,  # calculated from screen height
        "timer_y": 100,
    },
    "menu": {
        "logo_y": 0.23,
        "button_start_y": 0.48,
        "button_spacing": 0.13,
        "button_width_percent": 0.46,
        "button_height_percent": 0.105,
    },
    "pause": {
        "overlay_opacity": 150,
        "title_scale": 1.0,
        "button_scale_hover": 1.06,
    },
}

# Border radii for UI elements
BORDER_RADIUS = {
    "button": 12,
    "pause_button": 8,
}

# Text alignment
ALIGNMENT = {
    "center": "center",
    "left": "left",
    "right": "right",
}

# Shadow settings (optional for future use)
SHADOW = {
    "enabled": False,
    "offset": (2, 2),
    "color": (0, 0, 0, 100),
}

print("UI Style System loaded successfully!")