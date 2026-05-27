import pygame
import sys
from game import Game

def main():
    pygame.init()
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"游戏运行出错: {e}")
        sys.exit(1)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
