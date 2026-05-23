import pygame
import sys
from model.game_model import GameModel
from view.game_view import GameView
from view.start_view import StartView
from view.end_view import EndView
from view.level_view import LevelView
from controller.game_controller import GameController

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600

def main():
    pygame.init()
    pygame.display.set_caption("打砖块")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    game_model = GameModel(SCREEN_WIDTH, SCREEN_HEIGHT)
    game_controller = GameController(game_model, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    game_view = GameView(screen)
    start_view = StartView(screen)
    end_view = EndView(screen)
    level_view = LevelView(screen)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if game_model.game_state == 'start':
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        game_controller.start_game()
                else:
                    game_controller.handle_key_down(event.key)
            
            elif event.type == pygame.KEYUP:
                game_controller.handle_key_up(event.key)
            
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                game_controller.handle_mouse_motion(x)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if game_model.game_state == 'start':
                    action = start_view.handle_click((x, y))
                    if action == 'start':
                        game_model.reset()
                        game_controller.start_game()
                    elif action == 'continue':
                        game_controller.continue_game()
                elif game_model.game_state == 'game_over':
                    action = end_view.handle_click((x, y))
                    if action == 'restart':
                        game_model.reset()
                        game_controller.start_game()
                    elif action == 'menu':
                        game_model.set_state('start')
                else:
                    game_controller.handle_mouse_click(x, y)
        
        game_controller.update()
        
        if game_model.game_state == 'start':
            start_view.render(game_model.high_score)
        
        elif game_model.game_state == 'playing':
            if not game_controller.level_controller.is_countdown_complete():
                countdown = game_controller.level_controller.countdown
                level_view.render(game_model.current_level, countdown)
            else:
                game_view.render(game_model)
        
        elif game_model.game_state == 'level_transition':
            game_controller.start_game()
        
        elif game_model.game_state == 'game_over':
            is_new_high_score = game_model.score >= game_model.high_score
            end_view.render(game_model.score, game_model.current_level, 
                          game_model.high_score, is_new_high_score)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
