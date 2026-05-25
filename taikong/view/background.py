"""
太空背景绘制 - 绘制星空背景和闪烁的星星
"""

import random
import pygame

class Star:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.size = random.uniform(0.5, 2.0)
        self.brightness = random.randint(100, 255)
        self.twinkle_speed = random.uniform(0.02, 0.05)
        self.twinkle_offset = random.uniform(0, 2 * 3.14159)

    def update(self, time):
        self.current_brightness = int(
            self.brightness * (0.5 + 0.5 * abs(self.twinkle_speed * (time + self.twinkle_offset)))
        )
        self.current_brightness = max(50, min(255, self.current_brightness))

    def draw(self, surface):
        color = (self.current_brightness, self.current_brightness, self.current_brightness)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), int(self.size))


class SpaceBackground:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.stars = [Star(screen_width, screen_height) for _ in range(150)]
        self.shooting_stars = []

    def update(self, time):
        for star in self.stars:
            star.update(time)
        
        if random.random() < 0.005:
            self.shooting_stars.append({
                'x': random.randint(0, self.screen_width),
                'y': 0,
                'speed': random.uniform(10, 20),
                'length': random.randint(50, 100)
            })
        
        for star in self.shooting_stars[:]:
            star['y'] += star['speed']
            if star['y'] > self.screen_height:
                self.shooting_stars.remove(star)

    def draw(self, surface):
        surface.fill((0, 0, 10))
        
        for star in self.stars:
            star.draw(surface)
        
        for star in self.shooting_stars:
            end_x = star['x'] - star['length'] * 0.5
            end_y = star['y'] - star['length']
            pygame.draw.line(surface, (255, 255, 255), 
                           (star['x'], star['y']), 
                           (end_x, end_y), 2)
