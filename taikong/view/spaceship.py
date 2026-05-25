"""
飞船绘制 - 纯代码绘制三角形飞船
"""

import pygame
import math

class SpaceshipView:
    @staticmethod
    def draw(surface, spaceship):
        center_x = spaceship.x
        center_y = spaceship.y
        
        body_points = [
            (center_x, center_y - 25),
            (center_x - 15, center_y + 20),
            (center_x, center_y + 10),
            (center_x + 15, center_y + 20)
        ]
        pygame.draw.polygon(surface, (200, 200, 200), body_points)
        pygame.draw.polygon(surface, (150, 150, 150), body_points, 2)
        
        pygame.draw.circle(surface, (100, 200, 255), (center_x, center_y - 5), 5)
        
        flame_points = [
            (center_x - 8, center_y + 15),
            (center_x, center_y + 30 + abs(math.sin(pygame.time.get_ticks() * 0.01) * 10)),
            (center_x + 8, center_y + 15)
        ]
        pygame.draw.polygon(surface, (255, 100, 50), flame_points)
        pygame.draw.polygon(surface, (255, 200, 50), [
            (center_x - 4, center_y + 15),
            (center_x, center_y + 22 + abs(math.sin(pygame.time.get_ticks() * 0.015) * 5)),
            (center_x + 4, center_y + 15)
        ])
        
        wing_left = [
            (center_x - 15, center_y + 10),
            (center_x - 25, center_y + 20),
            (center_x - 18, center_y + 18)
        ]
        pygame.draw.polygon(surface, (180, 180, 180), wing_left)
        
        wing_right = [
            (center_x + 15, center_y + 10),
            (center_x + 25, center_y + 20),
            (center_x + 18, center_y + 18)
        ]
        pygame.draw.polygon(surface, (180, 180, 180), wing_right)
