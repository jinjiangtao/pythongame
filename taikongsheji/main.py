import pygame
from settings import *
from game import Game

def main():
    game = Game()
    running = True

    while running:
        running = game.handle_events()
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
