import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, WHITE, MAX_HINTS
from modules.game_logic import GameLogic
from modules.game_stats import GameStats
from modules.ui_manager import UIManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        self.game_logic = GameLogic()
        self.game_stats = GameStats()
        self.ui_manager = UIManager()
        
        self.hints_remaining = MAX_HINTS
        self.hint_cell = None
        
        self.setup_callbacks()
        self.ui_manager.show_menu()
    
    def setup_callbacks(self):
        self.ui_manager.set_callbacks(
            self.start_game,
            self.show_level_select,
            self.show_rules,
            self.quit_game,
            self.back_to_menu,
            self.restart_level,
            self.use_hint,
            self.next_level
        )
    
    def start_game(self):
        self.game_logic.init_board(SCREEN_WIDTH, SCREEN_HEIGHT, 0)
        self.game_stats.reset()
        self.game_stats.start_timer()
        self.hints_remaining = MAX_HINTS
        self.hint_cell = None
        self.ui_manager.show_game_ui(self.hints_remaining)
    
    def show_level_select(self):
        self.ui_manager.show_level_select(self.game_logic)
    
    def show_rules(self):
        self.ui_manager.show_rules()
    
    def quit_game(self):
        pygame.quit()
        sys.exit()
    
    def back_to_menu(self):
        self.game_stats.stop_timer()
        self.hints_remaining = MAX_HINTS
        self.hint_cell = None
        self.ui_manager.show_menu()
    
    def restart_level(self):
        self.game_logic.reset_level()
        self.game_stats.reset()
        self.game_stats.start_timer()
        self.hints_remaining = MAX_HINTS
        self.hint_cell = None
        self.ui_manager.show_game_ui(self.hints_remaining)
    
    def use_hint(self):
        if self.hints_remaining > 0:
            hint = self.game_logic.get_hint()
            if hint:
                self.hint_cell = hint
                self.hints_remaining -= 1
                self.game_stats.use_hint()
                self.ui_manager.update_hint_button(self.hints_remaining)
    
    def next_level(self):
        next_level = self.game_logic.current_level + 1
        if next_level < self.game_logic.get_total_levels():
            self.game_logic.init_board(SCREEN_WIDTH, SCREEN_HEIGHT, next_level)
            self.game_stats.reset()
            self.game_stats.start_timer()
            self.hints_remaining = MAX_HINTS
            self.hint_cell = None
            self.ui_manager.show_game_ui(self.hints_remaining)
        else:
            self.back_to_menu()
    
    def start_level(self, level_index):
        self.game_logic.init_board(SCREEN_WIDTH, SCREEN_HEIGHT, level_index)
        self.game_stats.reset()
        self.game_stats.start_timer()
        self.hints_remaining = MAX_HINTS
        self.hint_cell = None
        self.ui_manager.show_game_ui(self.hints_remaining)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.ui_manager.get_current_screen() == "game":
                    if self.ui_manager.handle_click(mouse_pos):
                        pass
                    elif self.game_logic.handle_click(mouse_pos):
                        self.game_stats.increment_steps()
                        self.hint_cell = None
                        
                        if self.game_logic.check_win():
                            self.game_stats.stop_timer()
                            self.game_logic.unlock_next_level()
                            self.ui_manager.show_win_dialog()
                else:
                    self.ui_manager.handle_click(mouse_pos)
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.ui_manager.update(mouse_pos)
        
        if self.ui_manager.get_current_screen() == "game":
            self.game_logic.update_hover(mouse_pos)
            self.game_stats.update()
    
    def draw(self):
        current_screen = self.ui_manager.get_current_screen()
        
        if current_screen == "game":
            self.screen.fill((50, 50, 60))
            self.game_stats.draw(self.screen, self.game_logic.get_level_info(self.game_logic.current_level)["name"])
            self.game_logic.draw(self.screen)
            
            if self.hint_cell:
                row, col = self.hint_cell
                cell = self.game_logic.cells[row][col]
                pygame.draw.rect(self.screen, (255, 0, 0), cell.rect, 4, border_radius=4)
            
            self.ui_manager.draw(self.screen)
        
        elif current_screen == "win_dialog":
            self.game_logic.draw(self.screen)
            self.game_stats.draw_win_screen(self.screen, self.game_logic.get_level_info(self.game_logic.current_level)["name"])
            self.ui_manager.draw(self.screen)
        
        else:
            self.ui_manager.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()