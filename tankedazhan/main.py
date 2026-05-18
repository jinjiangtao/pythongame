import pygame
from src.config import *
from src.game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("坦克大战")
    
    game = Game(screen)
    
    clock = pygame.time.Clock()
    
    running = True
    while running:
        if game.game_state == "quit":
            running = False
            break
        
        game.handle_events()
        
        if game.game_state == "victory":
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.next_level()
        else:
            game.update()
        
        game.draw()
        
        pygame.display.flip()
        
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()