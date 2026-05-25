import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_ROWS, GRID_COLS
from model.farm_model import FarmModel
from view.farm_view import FarmView
from controller.farm_controller import FarmController


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("农场经营游戏")
    
    model = FarmModel(GRID_ROWS, GRID_COLS)
    view = FarmView(screen)
    controller = FarmController(model, view)
    
    controller.run()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
