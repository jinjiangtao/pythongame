from src.config import DIFFICULTY_SETTINGS, ENEMY_TYPES, SCREEN_WIDTH, SCREEN_HEIGHT
import random
import math

class GameCore:
    def __init__(self, difficulty='normal'):
        self.score = 0
        self.level = 1
        self.bomb_count = 1
        self.game_over = False
        self.game_paused = False
        self.boss_defeated = False
        self.current_difficulty = difficulty
        self.settings = DIFFICULTY_SETTINGS[difficulty]
        self.last_spawn_time = 0
        self.last_boss_spawn = False
        
    def add_score(self, points):
        self.score += points
        self.check_level_up()
        self.check_boss_spawn()
        
    def check_level_up(self):
        threshold = self.settings['score_threshold']
        new_level = (self.score // threshold) + 1
        if new_level > self.level:
            self.level = new_level
            
    def check_boss_spawn(self):
        if self.score >= self.settings['boss_score'] and not self.last_boss_spawn:
            self.last_boss_spawn = True
            return True
        return False
    
    def reset_boss_spawn(self):
        self.last_boss_spawn = False
        
    def get_spawn_rate(self):
        base_rate = self.settings['base_spawn_rate']
        min_rate = self.settings['min_spawn_rate']
        decrease = self.settings['spawn_rate_decrease']
        
        rate = base_rate - (self.level - 1) * decrease
        return max(rate, min_rate)
    
    def get_enemy_type(self):
        rand = random.random()
        if self.level >= 5 and rand < 0.05:
            return 'heavy'
        elif self.level >= 3 and rand < 0.15:
            return 'fast'
        else:
            return 'normal'
        
    def get_enemy_spawn_x(self, enemy_type):
        size = ENEMY_TYPES[enemy_type]['size']
        return random.randint(size // 2, SCREEN_WIDTH - size // 2)
    
    def use_bomb(self):
        if self.bomb_count > 0:
            self.bomb_count -= 1
            return True
        return False
    
    def add_bomb(self):
        self.bomb_count += 1
        
    def is_game_over(self):
        return self.game_over
    
    def set_game_over(self):
        self.game_over = True
        
    def toggle_pause(self):
        self.game_paused = not self.game_paused
        
    def is_paused(self):
        return self.game_paused
    
    def reset(self):
        self.score = 0
        self.level = 1
        self.bomb_count = 1
        self.game_over = False
        self.game_paused = False
        self.boss_defeated = False
        self.last_boss_spawn = False
        self.last_spawn_time = 0
        
    def get_difficulty_multiplier(self):
        multipliers = {'easy': 0.7, 'normal': 1.0, 'hard': 1.3}
        return multipliers[self.current_difficulty]