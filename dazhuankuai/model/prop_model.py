import random

PROP_TYPES = {
    'expand_paddle': {'color': (0, 255, 0), 'symbol': '+', 'duration': 600},
    'shrink_paddle': {'color': (255, 0, 0), 'symbol': '-', 'duration': 400},
    'speed_up': {'color': (255, 100, 0), 'symbol': '↑', 'duration': 500},
    'speed_down': {'color': (0, 100, 255), 'symbol': '↓', 'duration': 500},
    'multi_ball': {'color': (255, 0, 255), 'symbol': '×2', 'duration': 0},
    'extra_life': {'color': (255, 255, 0), 'symbol': '❤', 'duration': 0},
    'suck_paddle': {'color': (100, 255, 255), 'symbol': '○', 'duration': 400},
    'invincible': {'color': (255, 255, 255), 'symbol': '★', 'duration': 300}
}

class PropModel:
    def __init__(self, x, y, prop_type):
        self.x = x
        self.y = y
        self.type = prop_type
        self.color = PROP_TYPES[prop_type]['color']
        self.symbol = PROP_TYPES[prop_type]['symbol']
        self.duration = PROP_TYPES[prop_type]['duration']
        self.speed = 2.0
        self.radius = 12
        self.collected = False

    def update(self):
        self.y += self.speed

    def get_bounds(self):
        return (self.x - self.radius, self.y - self.radius,
                self.x + self.radius, self.y + self.radius)

class PropGenerator:
    def __init__(self):
        self.drop_chance = 0.15

    def set_drop_chance(self, level):
        self.drop_chance = max(0.05, 0.15 - level * 0.015)

    def generate(self, x, y):
        if random.random() < self.drop_chance:
            prop_types = list(PROP_TYPES.keys())
            weights = [20, 10, 15, 20, 5, 8, 12, 10]
            prop_type = random.choices(prop_types, weights=weights)[0]
            return PropModel(x, y, prop_type)
        return None
