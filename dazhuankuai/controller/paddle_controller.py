import pygame

class PaddleController:
    def __init__(self, paddle_model, screen_width):
        self.paddle_model = paddle_model
        self.screen_width = screen_width
        self.keys = {'left': False, 'right': False}

    def handle_key_down(self, key):
        if key == pygame.K_LEFT or key == pygame.K_a:
            self.keys['left'] = True
        if key == pygame.K_RIGHT or key == pygame.K_d:
            self.keys['right'] = True

    def handle_key_up(self, key):
        if key == pygame.K_LEFT or key == pygame.K_a:
            self.keys['left'] = False
        if key == pygame.K_RIGHT or key == pygame.K_d:
            self.keys['right'] = False

    def handle_mouse_motion(self, x):
        self.paddle_model.set_position(x, self.screen_width)

    def update(self):
        if self.keys['left']:
            self.paddle_model.move_left(self.screen_width)
        if self.keys['right']:
            self.paddle_model.move_right(self.screen_width)
        self.paddle_model.update()
