import random

BRICK_TYPES = {
    'normal': {'hits': 1, 'color': (255, 100, 100), 'points': 10},
    'reinforced': {'hits': 2, 'color': (100, 150, 255), 'points': 25},
    'hardened': {'hits': 3, 'color': (150, 100, 255), 'points': 50},
    'unbreakable': {'hits': -1, 'color': (80, 80, 80), 'points': 0},
    'explosive': {'hits': 1, 'color': (255, 200, 50), 'points': 30}
}

class BrickModel:
    def __init__(self, x, y, width, height, brick_type='normal'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = brick_type
        self.max_hits = BRICK_TYPES[brick_type]['hits']
        self.hits_remaining = self.max_hits
        self.color = BRICK_TYPES[brick_type]['color']
        self.points = BRICK_TYPES[brick_type]['points']
        self.destroyed = False
        self.exploded = False

    def hit(self):
        if self.max_hits == -1:
            return False, 0, False
        self.hits_remaining -= 1
        if self.hits_remaining <= 0:
            self.destroyed = True
            return True, self.points, self.type == 'explosive'
        return False, 0, False

    def get_bounds(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def get_center(self):
        return (self.x + self.width // 2, self.y + self.height // 2)

    def get_color(self):
        if self.type == 'normal':
            return self.color
        elif self.type in ['reinforced', 'hardened']:
            intensity = (self.hits_remaining / self.max_hits)
            return tuple(int(c * intensity) for c in self.color)
        return self.color

class BrickGenerator:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.brick_width = 60
        self.brick_height = 25
        self.padding = 5
        self.offset_x = 30
        self.offset_y = 60

    def generate_level(self, level):
        bricks = []
        patterns = [
            self._pattern_grid,
            self._pattern_staggered,
            self._pattern_pyramid,
            self._pattern_diamond,
            self._pattern_random
        ]
        pattern_func = patterns[min(level - 1, len(patterns) - 1)]
        return pattern_func(level)

    def _pattern_grid(self, level):
        bricks = []
        rows = 4 + min(level, 3)
        cols = 10
        for row in range(rows):
            for col in range(cols):
                x = self.offset_x + col * (self.brick_width + self.padding)
                y = self.offset_y + row * (self.brick_height + self.padding)
                brick_type = self._determine_brick_type(level, row, col, rows)
                bricks.append(BrickModel(x, y, self.brick_width, self.brick_height, brick_type))
        return bricks

    def _pattern_staggered(self, level):
        bricks = []
        rows = 5 + min(level, 3)
        cols = 10
        for row in range(rows):
            offset = (self.brick_width + self.padding) // 2 if row % 2 == 1 else 0
            for col in range(cols - (1 if row % 2 == 1 else 0)):
                x = self.offset_x + offset + col * (self.brick_width + self.padding)
                y = self.offset_y + row * (self.brick_height + self.padding)
                brick_type = self._determine_brick_type(level, row, col, rows)
                bricks.append(BrickModel(x, y, self.brick_width, self.brick_height, brick_type))
        return bricks

    def _pattern_pyramid(self, level):
        bricks = []
        rows = 6 + min(level, 2)
        for row in range(rows):
            cols = 10 - row
            offset = row * (self.brick_width + self.padding) // 2
            for col in range(cols):
                x = self.offset_x + offset + col * (self.brick_width + self.padding)
                y = self.offset_y + row * (self.brick_height + self.padding)
                brick_type = self._determine_brick_type(level, row, col, rows)
                bricks.append(BrickModel(x, y, self.brick_width, self.brick_height, brick_type))
        return bricks

    def _pattern_diamond(self, level):
        bricks = []
        max_rows = 7 + min(level, 2)
        for row in range(max_rows):
            if row < max_rows // 2:
                cols = 5 + row
                offset = (10 - cols) * (self.brick_width + self.padding) // 2
            else:
                cols = 5 + (max_rows - 1 - row)
                offset = (10 - cols) * (self.brick_width + self.padding) // 2
            for col in range(cols):
                x = self.offset_x + offset + col * (self.brick_width + self.padding)
                y = self.offset_y + row * (self.brick_height + self.padding)
                brick_type = self._determine_brick_type(level, row, col, max_rows)
                bricks.append(BrickModel(x, y, self.brick_width, self.brick_height, brick_type))
        return bricks

    def _pattern_random(self, level):
        bricks = []
        rows = 5 + min(level, 4)
        cols = 11
        for row in range(rows):
            for col in range(cols):
                if random.random() > 0.2:
                    x = self.offset_x + col * (self.brick_width + self.padding)
                    y = self.offset_y + row * (self.brick_height + self.padding)
                    brick_type = self._determine_brick_type(level, row, col, rows)
                    bricks.append(BrickModel(x, y, self.brick_width, self.brick_height, brick_type))
        return bricks

    def _determine_brick_type(self, level, row, col, total_rows):
        reinforced_chance = min(0.1 + level * 0.08, 0.4)
        hardened_chance = min(0.05 + level * 0.04, 0.2)
        unbreakable_chance = min(0.02 + level * 0.02, 0.1)
        explosive_chance = min(0.05 + level * 0.03, 0.15)
        
        rand = random.random()
        if rand < unbreakable_chance:
            return 'unbreakable'
        rand -= unbreakable_chance
        if rand < hardened_chance:
            return 'hardened'
        rand -= hardened_chance
        if rand < reinforced_chance:
            return 'reinforced'
        rand -= reinforced_chance
        if rand < explosive_chance:
            return 'explosive'
        return 'normal'
