import pygame
import random
from constants import *

class Obstacle:
    def __init__(self, obstacle_type="normal"):
        self.type = obstacle_type
        self.width = OBSTACLE_WIDTH
        self.height = self._get_height_by_type()
        self.x = SCREEN_WIDTH
        self.y = self._get_y_by_type()
        self.passed = False
    
    def _get_height_by_type(self):
        if self.type == "low":
            return random.randint(20, 40)
        elif self.type == "tall":
            return random.randint(OBSTACLE_MAX_HEIGHT, OBSTACLE_TALL_HEIGHT)
        elif self.type == "floating":
            return random.randint(30, 60)
        else:
            return random.randint(OBSTACLE_MIN_HEIGHT, OBSTACLE_MAX_HEIGHT)
    
    def _get_y_by_type(self):
        if self.type == "floating":
            return random.randint(100, GROUND_Y - self.height - 50)
        else:
            return GROUND_Y - self.height
    
    def update(self, speed):
        self.x -= speed
    
    def draw(self, screen):
        body_color = self._get_color_by_type()
        detail_color = ORANGE
        
        pygame.draw.rect(screen, body_color, (self.x, self.y, self.width, self.height))
        
        pygame.draw.rect(screen, detail_color, (self.x + 5, self.y + 10, self.width - 10, 5))
        pygame.draw.rect(screen, detail_color, (self.x + 5, self.y + self.height - 15, self.width - 10, 5))
        
        if self.type == "floating":
            pygame.draw.rect(screen, GRAY, (self.x + 5, self.y + self.height, self.width - 10, 3))
    
    def _get_color_by_type(self):
        if self.type == "low":
            return (0, 150, 0)
        elif self.type == "tall":
            return (139, 0, 0)
        elif self.type == "floating":
            return PURPLE
        else:
            return RED
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_mask(self):
        mask = pygame.mask.Mask((self.width, self.height), False)
        for y in range(self.height):
            for x in range(self.width):
                if y < 5 or y >= self.height - 5:
                    mask.set_at((x, y), True)
                elif x < 5 or x >= self.width - 5:
                    mask.set_at((x, y), True)
                elif y >= 5 and y < self.height - 5 and x >= 5 and x < self.width - 5:
                    mask.set_at((x, y), True)
        return mask
    
    def is_off_screen(self):
        return self.x + self.width < 0

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.last_spawn_time = 0
        self.spawn_interval = random.randint(OBSTACLE_SPAWN_INTERVAL_MIN, OBSTACLE_SPAWN_INTERVAL_MAX)
        self.consecutive_count = 0
        self.max_consecutive = 3
    
    def spawn_obstacle(self, score):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_interval:
            types = ["normal", "low", "tall", "floating"]
            
            if score > 500:
                types.extend(["normal", "tall", "floating"])
            
            chosen_type = random.choice(types)
            
            if self.consecutive_count < self.max_consecutive and random.random() < 0.3:
                self.obstacles.append(Obstacle(chosen_type))
                self.consecutive_count += 1
                self.spawn_interval = random.randint(500, 1000)
            else:
                self.obstacles.append(Obstacle(chosen_type))
                self.consecutive_count = 0
                self.spawn_interval = random.randint(OBSTACLE_SPAWN_INTERVAL_MIN, OBSTACLE_SPAWN_INTERVAL_MAX)
            
            self.last_spawn_time = current_time
    
    def update(self, speed):
        for obstacle in self.obstacles[:]:
            obstacle.update(speed)
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
    
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    
    def get_obstacles(self):
        return self.obstacles