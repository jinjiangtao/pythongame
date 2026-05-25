"""
陨石绘制 - 绘制不规则多边形陨石
"""

import pygame
import math

class AsteroidView:
    @staticmethod
    def draw(surface, asteroid):
        vertices_screen = []
        for angle, radius in asteroid.vertices:
            rad = math.radians(angle + asteroid.rotation)
            vx = asteroid.x + radius * math.cos(rad)
            vy = asteroid.y + radius * math.sin(rad)
            vertices_screen.append((vx, vy))
        
        if len(vertices_screen) >= 3:
            pygame.draw.polygon(surface, asteroid.color, vertices_screen)
            pygame.draw.polygon(surface, (80, 80, 80), vertices_screen, 2)
        
        for _ in range(3):
            crater_x = asteroid.x + asteroid.size * 0.3 * math.cos(math.radians(asteroid.rotation + _ * 120))
            crater_y = asteroid.y + asteroid.size * 0.3 * math.sin(math.radians(asteroid.rotation + _ * 120))
            pygame.draw.circle(surface, (60, 60, 60), 
                              (int(crater_x), int(crater_y)), 
                              int(asteroid.size * 0.15))
