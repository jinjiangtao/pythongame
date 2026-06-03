# utils.py - 辅助函数模块

import math
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

def distance(x1, y1, x2, y2):
    """计算两点之间的距离"""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def circle_circle_collision(x1, y1, r1, x2, y2, r2):
    """检测两个圆形是否碰撞"""
    return distance(x1, y1, x2, y2) < (r1 + r2)

def circle_rect_collision(cx, cy, cr, rx, ry, rw, rh):
    """检测圆形与矩形是否碰撞"""
    closest_x = max(rx, min(cx, rx + rw))
    closest_y = max(ry, min(cy, ry + rh))
    return distance(cx, cy, closest_x, closest_y) < cr

class Particle:
    """粒子类，用于碰撞特效"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 4
        angle = math.radians(math.random() * 360)
        speed = 3 + math.random() * 3
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 1.0
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.life -= 0.03
        self.radius *= 0.97
    
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * self.life)
            color = (*self.color[:3], alpha)
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.radius))

def create_particles(x, y, color, count=5):
    """创建粒子特效"""
    particles = []
    for _ in range(count):
        particles.append(Particle(x, y, color))
    return particles