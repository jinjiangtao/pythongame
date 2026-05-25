"""
陨石模型 - 定义陨石的属性和行为
"""

import random

class Asteroid:
    def __init__(self, x, y, size=None, speed=None):
        self.x = x
        self.y = y
        
        if size is None:
            self.size = random.randint(15, 50)
        else:
            self.size = size
            
        if speed is None:
            self.speed = random.uniform(2, 5)
        else:
            self.speed = speed
            
        self.rotation = 0
        self.rotation_speed = random.uniform(-3, 3)
        gray = random.randint(100, 180)
        self.color = (gray, gray, gray)
        self.vertices = self._generate_vertices()

    def _generate_vertices(self):
        vertices = []
        num_vertices = random.randint(6, 10)
        for i in range(num_vertices):
            angle = (360 / num_vertices) * i
            radius = self.size * random.uniform(0.7, 1.0)
            vertices.append((angle, radius))
        return vertices

    def update(self, difficulty=1.0):
        self.y += self.speed * difficulty
        self.rotation += self.rotation_speed

    def is_off_screen(self, screen_height):
        return self.y - self.size > screen_height

    def get_rect(self):
        from pygame import Rect
        return Rect(
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size
        )

    def collides_with(self, other_rect):
        return self.get_rect().colliderect(other_rect)
