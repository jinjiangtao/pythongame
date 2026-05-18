from src.config import *

class Bullet:
    def __init__(self, x, y, direction, is_player=True):
        self.x = x
        self.y = y
        self.direction = direction
        self.is_player = is_player
        self.speed = BULLET_SPEED
        self.width = 8
        self.height = 8
        self.active = True
    
    def update(self):
        if self.direction == DIR_UP:
            self.y -= self.speed
        elif self.direction == DIR_DOWN:
            self.y += self.speed
        elif self.direction == DIR_LEFT:
            self.x -= self.speed
        elif self.direction == DIR_RIGHT:
            self.x += self.speed
        
        if (self.x < 0 or self.x > SCREEN_WIDTH or
            self.y < 0 or self.y > SCREEN_HEIGHT):
            self.active = False
    
    def draw(self, screen):
        color = GREEN if self.is_player else RED
        pygame.draw.rect(screen, color, 
                        (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)