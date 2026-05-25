"""
太空陨石躲避战 - 主程序入口
Pygame 太空生存小游戏
MVC 架构，纯代码绘制，无需图片资源
"""

import pygame
from controller import GameController

def main():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    
    pygame.init()
    pygame.display.set_caption("太空陨石躲避战 - Space Asteroid Survival")
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    game = GameController(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.init_pygame()
    
    game.run(screen)

if __name__ == "__main__":
    main()
