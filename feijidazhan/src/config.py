import pygame

pygame.init()

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 720

PLAYER_SIZE = 50
PLAYER_SPEED = 8
PLAYER_BULLET_SPEED = 12
PLAYER_MAX_BULLETS = 10
PLAYER_INITIAL_HEALTH = 100
PLAYER_MAX_HEALTH = 100
PLAYER_INVINCIBLE_DURATION = 2000
PLAYER_FIRE_RATE = 150

ENEMY_TYPES = {
    'normal': {
        'size': 40,
        'speed': 3,
        'health': 20,
        'score': 100,
        'fire_rate': 2000,
        'bullet_speed': 6
    },
    'fast': {
        'size': 35,
        'speed': 6,
        'health': 10,
        'score': 150,
        'fire_rate': 1500,
        'bullet_speed': 8
    },
    'heavy': {
        'size': 60,
        'speed': 2,
        'health': 60,
        'score': 300,
        'fire_rate': 1000,
        'bullet_speed': 5
    },
    'boss': {
        'size': 120,
        'speed': 1,
        'health': 500,
        'score': 2000,
        'fire_rate': 500,
        'bullet_speed': 7
    }
}

BULLET_TYPES = {
    'player_single': {'size': 6, 'speed': PLAYER_BULLET_SPEED, 'damage': 10},
    'player_double': {'size': 6, 'speed': PLAYER_BULLET_SPEED, 'damage': 10},
    'player_triple': {'size': 6, 'speed': PLAYER_BULLET_SPEED, 'damage': 10},
    'enemy_normal': {'size': 8, 'speed': 6, 'damage': 10},
    'enemy_fast': {'size': 6, 'speed': 8, 'damage': 15},
    'enemy_heavy': {'size': 10, 'speed': 5, 'damage': 20},
    'boss_bullet': {'size': 12, 'speed': 7, 'damage': 25},
    'boss_spread': {'size': 10, 'speed': 6, 'damage': 20},
    'boss_fan': {'size': 8, 'speed': 8, 'damage': 15}
}

PROP_TYPES = {
    'power_up': {'color': (0, 255, 0), 'duration': 10000},
    'shield': {'color': (0, 128, 255), 'duration': 5000},
    'health': {'color': (255, 0, 0), 'heal_amount': 30},
    'bomb': {'color': (255, 255, 0), 'count': 1}
}

DIFFICULTY_SETTINGS = {
    'easy': {
        'base_spawn_rate': 2000,
        'min_spawn_rate': 800,
        'spawn_rate_decrease': 100,
        'score_threshold': 500,
        'boss_score': 5000
    },
    'normal': {
        'base_spawn_rate': 1500,
        'min_spawn_rate': 500,
        'spawn_rate_decrease': 120,
        'score_threshold': 800,
        'boss_score': 8000
    },
    'hard': {
        'base_spawn_rate': 1000,
        'min_spawn_rate': 300,
        'spawn_rate_decrease': 150,
        'score_threshold': 1000,
        'boss_score': 10000
    }
}

GAME_COLORS = {
    'background': (0, 0, 0),
    'player': (0, 255, 0),
    'player_bullet': (255, 255, 255),
    'enemy_normal': (255, 100, 100),
    'enemy_fast': (255, 255, 100),
    'enemy_heavy': (150, 50, 200),
    'boss': (255, 0, 255),
    'boss_attack': (255, 100, 255)
}

FONT_PATH = 'arial.ttf'
FONT_SIZE = 24

FPS = 60