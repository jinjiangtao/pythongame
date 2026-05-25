"""
飞船模型 - 定义玩家飞船的属性和行为
"""

class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 50
        self.speed = 8
        self.color = (255, 255, 255)
        self.health = 100

    def move_to(self, target_x, target_y):
        self.x = target_x
        self.y = target_y

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def get_rect(self):
        from pygame import Rect
        return Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )

    def get_center(self):
        return (self.x, self.y)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
