"""
游戏逻辑控制器 - 处理碰撞检测、陨石生成、难度递增等
"""

import random
from model import Asteroid

class GameLogic:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.asteroids = []
        self.asteroid_spawn_timer = 0
        self.asteroid_spawn_rate = 60
        self.base_spawn_rate = 60
        self.score_timer = 0

    def reset(self):
        self.asteroids.clear()
        self.asteroid_spawn_timer = 0
        self.asteroid_spawn_rate = self.base_spawn_rate
        self.score_timer = 0

    def update_difficulty(self, difficulty):
        self.asteroid_spawn_rate = max(15, int(self.base_spawn_rate / difficulty))

    def spawn_asteroid(self, difficulty=1.0):
        x = random.randint(50, self.screen_width - 50)
        y = -50
        
        size = random.randint(
            int(15 / (difficulty * 0.5)),
            int(50 / (difficulty * 0.5))
        )
        size = max(10, min(60, size))
        
        speed = random.uniform(2, 5) * difficulty
        
        asteroid = Asteroid(x, y, size, speed)
        self.asteroids.append(asteroid)

    def update_asteroids(self, difficulty):
        self.asteroid_spawn_timer += 1
        
        if self.asteroid_spawn_timer >= self.asteroid_spawn_rate:
            self.spawn_asteroid(difficulty)
            self.asteroid_spawn_timer = 0
        
        for asteroid in self.asteroids[:]:
            asteroid.update(difficulty)
            if asteroid.is_off_screen(self.screen_height):
                self.asteroids.remove(asteroid)

    def check_collisions(self, spaceship_rect, game_data):
        collision_occurred = False
        
        for asteroid in self.asteroids:
            if asteroid.collides_with(spaceship_rect):
                damage = int(asteroid.size * 0.8)
                game_data.take_damage(damage)
                self.asteroids.remove(asteroid)
                collision_occurred = True
        
        return collision_occurred

    def update_score(self, delta_time, game_data):
        self.score_timer += delta_time
        
        if self.score_timer >= 0.1:
            game_data.update_score(10)
            self.score_timer = 0

    def get_asteroids(self):
        return self.asteroids
