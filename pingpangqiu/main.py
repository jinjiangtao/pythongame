import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.game_core import GameCore


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("乒乓球对战")

    game = GameCore(screen)
    clock = pygame.time.Clock()

    running = True
    while running:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(FPS)


if __name__ == "__main__":
    main()