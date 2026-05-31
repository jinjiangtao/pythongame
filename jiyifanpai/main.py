import pygame
import sys
import config
import game

def main():
    pygame.init()
    pygame.display.set_caption("Memory Match - Complex Edition")
    
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    game_instance = game.Game()
    game_instance.initialize_cards()
    
    running = True
    
    while running:
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                if not game_instance.is_input_blocked():
                    if not game_instance.handle_events(event):
                        running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        game_instance.reset()
        
        game_instance.update(dt)
        game_instance.draw(screen)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
