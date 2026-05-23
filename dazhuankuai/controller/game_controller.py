import pygame
import random
from controller.paddle_controller import PaddleController
from controller.ball_controller import BallController
from controller.prop_controller import PropController
from controller.level_controller import LevelController
from model.prop_model import PropGenerator
from model.ball_model import BallModel

class GameController:
    def __init__(self, game_model, screen_width, screen_height):
        self.game_model = game_model
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level_controller = LevelController(game_model, screen_width, screen_height)
        self.paddle_controller = None
        self.ball_controllers = []
        self.prop_controllers = []
        self.prop_generator = PropGenerator()
        self.level_started = False

    def start_game(self):
        self.game_model.set_state('playing')
        self.level_controller.start_level(self.game_model.current_level)
        self._init_controllers()
        self.level_started = False
        self.prop_generator.set_drop_chance(self.game_model.current_level)

    def continue_game(self):
        self.start_game()

    def _init_controllers(self):
        paddle = self.level_controller.get_paddle()
        self.paddle_controller = PaddleController(paddle, self.screen_width)
        self.ball_controllers = []
        for ball in self.game_model.balls:
            bc = BallController(ball, paddle, self.screen_width, self.screen_height)
            self.ball_controllers.append(bc)
        self.prop_controllers = []
        for prop in self.game_model.props:
            pc = PropController(prop, paddle, self.game_model, self.ball_controllers)
            self.prop_controllers.append(pc)

    def handle_key_down(self, key):
        if self.game_model.game_state == 'start':
            return
        
        if key == pygame.K_SPACE:
            if self.game_model.paused:
                self.game_model.toggle_pause()
            elif not self.level_started and self.level_controller.is_countdown_complete():
                self.level_started = True
                for bc in self.ball_controllers:
                    bc.release_ball()
            elif self.game_model.game_state == 'playing':
                self.game_model.toggle_pause()
        
        elif key == pygame.K_ESCAPE:
            if self.game_model.game_state == 'playing':
                self.game_model.set_state('start')
                self.game_model.paused = False
        
        if self.paddle_controller and not self.game_model.paused:
            self.paddle_controller.handle_key_down(key)

    def handle_key_up(self, key):
        if self.paddle_controller and not self.game_model.paused:
            self.paddle_controller.handle_key_up(key)

    def handle_mouse_motion(self, x):
        if self.paddle_controller and not self.game_model.paused:
            self.paddle_controller.handle_mouse_motion(x)

    def handle_mouse_click(self, x, y):
        if not self.level_started and self.level_controller.is_countdown_complete():
            self.level_started = True
            for bc in self.ball_controllers:
                bc.release_ball()

    def update(self):
        if self.game_model.game_state != 'playing':
            return
        
        if not self.level_controller.is_countdown_complete():
            self.level_controller.update_countdown()
            return
        
        if self.game_model.paused:
            return
        
        self.paddle_controller.update()
        
        for bc in self.ball_controllers[:]:
            bc.update()
            self.level_controller.handle_ball_brick_collisions(bc, self.prop_generator)
            
            if bc.is_off_screen():
                if bc.get_ball().invincible:
                    bc.reset(self.game_model.paddle.x, self.screen_height - 70)
                    bc.get_ball().set_stuck(self.game_model.paddle.x, self.game_model.paddle.width)
                else:
                    self.ball_controllers.remove(bc)
        
        if len(self.ball_controllers) == 0:
            self.game_model.lose_life()
            if self.game_model.lives > 0:
                self.game_model.balls = [BallModel(self.game_model.paddle.x, self.screen_height - 70)]
                self._init_controllers()
                self.level_started = False
        
        for pc in self.prop_controllers[:]:
            pc.update()
            if pc.is_off_screen(self.screen_height) or pc.get_prop().collected:
                self.prop_controllers.remove(pc)
        
        self.game_model.props = [p for p in self.game_model.props if not p.collected and p.y < self.screen_height + p.radius]
        
        self.level_controller.update_explosions()
        self.game_model.update_score_animations()
        
        if self.level_controller.check_level_complete():
            if self.game_model.next_level():
                self.game_model.set_state('level_transition')
            else:
                self.game_model.set_state('game_over')
                if self.game_model.score >= self.game_model.high_score:
                    self.game_model._save_data()
