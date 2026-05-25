"""
游戏主控制器 - 协调各层组件
"""

from model import GameData, Spaceship
from view import SpaceBackground, SpaceshipView, AsteroidView, GameUI, MainMenu
from .input_handler import InputHandler
from .game_logic import GameLogic

class GameController:
    def __init__(self, screen_width=800, screen_height=800):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.game_data = GameData()
        self.spaceship = Spaceship(screen_width // 2, screen_height - 100)
        self.background = SpaceBackground(screen_width, screen_height)
        self.spaceship_view = SpaceshipView()
        self.asteroid_view = AsteroidView()
        self.game_ui = GameUI()
        self.main_menu = MainMenu()
        self.input_handler = InputHandler(screen_width, screen_height)
        self.game_logic = GameLogic(screen_width, screen_height)
        
        self.clock = None
        self.delta_time = 0
        self.game_time = 0

    def init_pygame(self):
        import pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.game_ui.init_fonts()
        self.main_menu.init_fonts()

    def reset_game(self):
        self.game_data.reset()
        self.spaceship.reset(self.screen_width // 2, self.screen_height - 100)
        self.game_logic.reset()
        self.game_time = 0

    def start_game(self):
        self.reset_game()
        self.game_data.in_main_menu = False

    def handle_events(self):
        running = self.input_handler.handle_events(
            self.game_data, 
            self.start_game
        )
        return running

    def update(self):
        if self.game_data.in_main_menu:
            self.background.update(self.game_time)
            return
        
        if self.game_data.game_over:
            return
        
        self.delta_time = self.clock.get_rawtime() / 1000.0
        self.game_time += self.delta_time
        
        self.game_data.update_survival_time(self.delta_time)
        self.game_data.update_difficulty(self.game_data.survival_time)
        
        mouse_x, mouse_y = self.input_handler.get_mouse_position()
        self.spaceship.move_to(
            max(30, min(self.screen_width - 30, mouse_x)),
            max(40, min(self.screen_height - 40, mouse_y))
        )
        
        self.game_logic.update_difficulty(self.game_data.difficulty)
        self.game_logic.update_asteroids(self.game_data.difficulty)
        self.game_logic.check_collisions(self.spaceship.get_rect(), self.game_data)
        self.game_logic.update_score(self.delta_time, self.game_data)
        
        self.background.update(self.game_time)

    def draw(self, surface):
        if self.game_data.in_main_menu:
            self.main_menu.draw(surface, self.screen_width, self.screen_height)
            return
        
        self.background.draw(surface)
        
        for asteroid in self.game_logic.get_asteroids():
            self.asteroid_view.draw(surface, asteroid)
        
        self.spaceship_view.draw(surface, self.spaceship)
        
        self.game_ui.draw_score_panel(surface, self.game_data)
        self.game_ui.draw_health_bar(
            surface, 
            self.game_data, 
            self.screen_width - 220, 
            20
        )
        
        if self.game_data.game_over:
            self.game_ui.draw_game_over(
                surface, 
                self.game_data, 
                self.screen_width, 
                self.screen_height
            )

    def run(self, surface):
        running = True
        while running:
            running = self.handle_events()
            
            if not running:
                break
            
            self.update()
            self.draw(surface)
            
            import pygame
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
