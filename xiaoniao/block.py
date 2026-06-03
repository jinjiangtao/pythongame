# block.py - 方块类

import pygame
from settings import BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_COLOR

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BLOCK_WIDTH
        self.height = BLOCK_HEIGHT
        self.hp = 1
        self.alive = True
    
    def hit(self):
        """方块被击中"""
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False
    
    def draw(self, screen):
        """绘制方块"""
        if not self.alive:
            return
        
        pygame.draw.rect(screen, BLOCK_COLOR, 
                        (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (0, 0, 0), 
                        (self.x, self.y, self.width, self.height), 2)