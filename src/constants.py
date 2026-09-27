SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

MIN_SCREEN_WIDTH = 960
MIN_SCREEN_HEIGHT = 540

FPS = 60

UI_MARGIN = 24
UI_FONT_SIZE = 24

LINE_WIDTH = 2

PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 200
PLAYER_SPEED = 180

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_LIFETIME = 20.0
ASTEROID_BLINK_TIME = 3.0
ASTEROID_BLINK_INTERVAL = 0.15
ASTEROID_LARGE_SPEED = 20
ASTEROID_MEDIUM_SPEED = 40
ASTEROID_SMALL_SPEED = 100

SHOT_RADIUS = 2
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3

PLAYER_BOOST_MULTIPLIER = 2.0
PLAYER_BOOST_MAX_ENERGY = 100.0
PLAYER_BOOST_DRAIN_RATE = 50.0
PLAYER_BOOST_RECHARGE_RATE = 20.0

POWERUP_RADIUS = 15
POWERUP_LIFETIME = 15.0
POWERUP_SPAWN_RATE_SECONDS = 20.0

DIFFICULTY_MODIFIERS = {
    "EASY": {"spawn_rate": 1.2, "speed_mult": 0.7, "score_mult": 0.5},
    "NORMAL": {"spawn_rate": 1.0, "speed_mult": 1.0, "score_mult": 1.0},
    "HARD": {"spawn_rate": 0.6, "speed_mult": 1.5, "score_mult": 2.0},
}

ASSET_IMAGES = {
    "background": "assets/images/background.png",
    "menu_background": "assets/images/menu_background.png",
    "logo": "assets/images/logo.png",
    "button": "assets/images/button.png",
    "button_active": "assets/images/button_active.png",
    "player": "assets/images/player.png",
    "asteroid_small": "assets/images/asteroid_small.png",
    "asteroid_medium": "assets/images/asteroid_medium.png",
    "asteroid_large": "assets/images/asteroid_large.png",
    "shot": "assets/images/shot.png",
}

ASSET_SOUNDS = {
    "destroyed": "assets/sounds/destroyed.mp3",
    "shoot": "assets/sounds/shoot.mp3",
}

ASSET_FONTS = {
    "main": "assets/fonts/PressStart2P-Regular.ttf",
}
