import json
import os

class GameState:
    START = 'start'
    PLAYING = 'playing'
    PAUSED = 'paused'
    LEVEL_COMPLETE = 'level_complete'
    GAME_OVER = 'game_over'

class GameModel:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.score = 0
        self.high_score = self._load_high_score()
        self.lives = 3
        self.max_lives = 5
        self.level = 1
        self.max_levels = 10
        
        self.game_state = GameState.START
        self.prev_state = GameState.START
        
        self.save_file = 'game_save.json'

    def _load_high_score(self):
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except Exception:
            pass
        return 0

    def _save_game(self):
        try:
            data = {
                'high_score': self.high_score,
                'level': self.level,
                'score': self.score
            }
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f)
        except Exception:
            pass

    def add_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            self._save_game()

    def add_life(self):
        if self.lives < self.max_lives:
            self.lives += 1
            return True
        return False

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_state = GameState.GAME_OVER
            self._save_game()
            return True
        return False

    def next_level(self):
        if self.level < self.max_levels:
            self.level += 1
            self.game_state = GameState.LEVEL_COMPLETE
            self._save_game()
            return True
        return False

    def reset_level(self):
        self.game_state = GameState.PLAYING

    def start_game(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_state = GameState.PLAYING

    def continue_game(self, saved_level=None, saved_score=None):
        if saved_level is not None:
            self.level = saved_level
        if saved_score is not None:
            self.score = saved_score
        self.game_state = GameState.PLAYING

    def pause_game(self):
        if self.game_state == GameState.PLAYING:
            self.prev_state = self.game_state
            self.game_state = GameState.PAUSED

    def resume_game(self):
        if self.game_state == GameState.PAUSED:
            self.game_state = self.prev_state

    def reset_game(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_state = GameState.START

    def get_game_state(self):
        return self.game_state

    def set_game_state(self, state):
        self.game_state = state

    def get_level_speed_multiplier(self):
        return 1.0 + (self.level - 1) * 0.1

    def load_progress(self):
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('level', 1), data.get('score', 0)
        except Exception:
            pass
        return 1, 0

    def is_game_over(self):
        return self.game_state == GameState.GAME_OVER

    def is_playing(self):
        return self.game_state == GameState.PLAYING

    def is_paused(self):
        return self.game_state == GameState.PAUSED

    def is_level_complete(self):
        return self.game_state == GameState.LEVEL_COMPLETE