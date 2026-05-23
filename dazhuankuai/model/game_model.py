import json
import os

class GameModel:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_level = 1
        self.max_levels = 5
        self.score = 0
        self.high_score = self._load_high_score()
        self.lives = 3
        self.max_lives = 5
        self.game_state = 'start'
        self.paused = False
        self.balls = []
        self.paddle = None
        self.bricks = []
        self.props = []
        self.explosions = []
        self.score_animations = []

    def _load_high_score(self):
        try:
            if os.path.exists('save_data.json'):
                with open('save_data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except:
            pass
        return 0

    def _save_data(self):
        data = {
            'high_score': self.high_score,
            'current_level': self.current_level,
            'score': self.score
        }
        with open('save_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def add_score(self, points, x, y):
        self.score += points
        self.score_animations.append({'x': x, 'y': y, 'points': points, 'frame': 0})
        if self.score > self.high_score:
            self.high_score = self.score
            self._save_data()

    def add_life(self):
        if self.lives < self.max_lives:
            self.lives += 1

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_state = 'game_over'
            self._save_data()

    def next_level(self):
        if self.current_level < self.max_levels:
            self.current_level += 1
            self._save_data()
            return True
        return False

    def reset(self):
        self.current_level = 1
        self.score = 0
        self.lives = 3
        self.game_state = 'start'
        self.paused = False
        self.balls = []
        self.props = []
        self.explosions = []
        self.score_animations = []

    def update_score_animations(self):
        self.score_animations = [anim for anim in self.score_animations if anim['frame'] < 30]
        for anim in self.score_animations:
            anim['frame'] += 1
            anim['y'] -= 1

    def is_level_complete(self):
        return all(brick.destroyed for brick in self.bricks)

    def set_state(self, state):
        self.game_state = state

    def toggle_pause(self):
        self.paused = not self.paused

    def get_speed_multiplier(self):
        return 1.0 + (self.current_level - 1) * 0.2
