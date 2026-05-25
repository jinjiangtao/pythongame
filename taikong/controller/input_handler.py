"""
输入处理控制器 - 处理鼠标和键盘输入
"""

import pygame

class InputHandler:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.mouse_pos = (screen_width // 2, screen_height // 2)
        self.mouse_pressed = False

    def handle_events(self, game_data, callback_start_game=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed = True
                if game_data.in_main_menu and callback_start_game:
                    callback_start_game()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r and game_data.game_over:
                    callback_start_game()

        return True

    def get_mouse_position(self):
        return self.mouse_pos

    def is_mouse_pressed(self):
        return self.mouse_pressed
