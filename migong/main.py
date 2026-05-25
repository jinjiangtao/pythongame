import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controller.game_controller import GameController

def main():
    pygame.init()
    
    SCREEN_WIDTH = 750 + 180
    SCREEN_HEIGHT = 750 + 60
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("迷宫探险闯关游戏")
    
    controller = GameController(screen)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        running = controller.handle_events()
        controller.update()
        controller.render()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()