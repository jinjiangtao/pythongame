"""
游戏数据模型 - 存储全局游戏状态和配置
"""

class GameData:
    def __init__(self):
        self.reset()

    def reset(self):
        self.score = 0
        self.health = 100
        self.max_health = 100
        self.survival_time = 0.0
        self.difficulty = 1.0
        self.game_over = False
        self.is_paused = False
        self.in_main_menu = True

    def update_score(self, points):
        self.score += points

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.game_over = True

    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)

    def update_survival_time(self, delta_time):
        self.survival_time += delta_time

    def update_difficulty(self, time):
        self.difficulty = 1.0 + (time / 30.0) * 0.5

    def get_display_time(self):
        minutes = int(self.survival_time) // 60
        seconds = int(self.survival_time) % 60
        return f"{minutes:02d}:{seconds:02d}"
