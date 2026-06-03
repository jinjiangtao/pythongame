# bird.py - 小鸟类

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT, GRAVITY, BIRD_RADIUS, BIRD_COLOR, SLINGSHOT_X, SLINGSHOT_Y

class Bird:
    def __init__(self):
        self.x = SLINGSHOT_X
        self.y = SLINGSHOT_Y - 30
        self.vx = 0
        self.vy = 0
        self.radius = BIRD_RADIUS
        self.is_flying = False
    
    def launch(self, force_x, force_y):
        """发射小鸟"""
        self.vx = force_x
        self.vy = force_y
        self.is_flying = True
    
    def update(self):
        """更新小鸟位置（飞行中）"""
        if not self.is_flying:
            return
        
        self.x += self.vx
        self.y += self.vy
        self.vy += GRAVITY
    
    def check_bounds(self):
        """检测边界条件"""
        if self.is_flying:
            if self.x < 0 or self.x > SCREEN_WIDTH or self.y > GROUND_HEIGHT:
                self.is_flying = False
    
    def reset(self):
        """重置小鸟到弹弓位置"""
        self.x = SLINGSHOT_X
        self.y = SLINGSHOT_Y - 30
        self.vx = 0
        self.vy = 0
        self.is_flying = False
    
    def draw(self, screen):
        """绘制小鸟"""
        pygame.draw.circle(screen, BIRD_COLOR, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x) - 5, int(self.y) - 3), 3)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x) + 5, int(self.y) - 3), 3)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x) - 4, int(self.y) - 4), 1)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x) + 6, int(self.y) - 4), 1)