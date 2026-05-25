import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from view.game_view import GameView
from controller.game_controller import GameController

def main():
    pygame.init()
    pygame.font.init()
    
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("弓箭射击游戏")
    
    view = GameView(screen)
    controller = GameController(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    controller.run(view)

if __name__ == "__main__":
    main()