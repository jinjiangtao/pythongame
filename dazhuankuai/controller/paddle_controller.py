class PaddleController:
    def __init__(self, paddle_model):
        self.paddle_model = paddle_model
        self.keys = {'left': False, 'right': False}
    
    def handle_key_down(self, key):
        if key == 'left':
            self.keys['left'] = True
        elif key == 'right':
            self.keys['right'] = True
    
    def handle_key_up(self, key):
        if key == 'left':
            self.keys['left'] = False
        elif key == 'right':
            self.keys['right'] = False
    
    def handle_mouse_move(self, mouse_x):
        self.paddle_model.move_to(mouse_x)
    
    def update(self):
        if self.keys['left']:
            self.paddle_model.move_left()
        if self.keys['right']:
            self.paddle_model.move_right()
        
        self.paddle_model.update()