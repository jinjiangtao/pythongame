class BallController:
    def __init__(self, ball_model, paddle_model):
        self.ball_model = ball_model
        self.paddle_model = paddle_model
        self.is_launched = False
    
    def update(self):
        if not self.is_launched:
            if self.paddle_model.is_holding_ball:
                new_x = self.paddle_model.x + self.paddle_model.ball_offset - self.ball_model.width // 2
                self.ball_model.x = new_x
                self.ball_model.y = self.paddle_model.y - self.ball_model.height
            return
        
        self.ball_model.update()
        
        self._check_paddle_collision()
    
    def _check_paddle_collision(self):
        collision, hit_position = self.paddle_model.check_collision(self.ball_model.get_rect())
        
        if collision:
            self.ball_model.bounce_off_paddle(hit_position)
            
            if self.paddle_model.sticky:
                self.paddle_model.hold_ball(self.ball_model)
                self.is_launched = False
    
    def launch(self):
        if not self.is_launched:
            self.is_launched = True
            self.paddle_model.is_holding_ball = False
    
    def reset(self):
        self.is_launched = False
        self.ball_model.reset(self.paddle_model.x, self.paddle_model.width)
    
    def is_active(self):
        return self.ball_model.active
    
    def is_out_of_bounds(self):
        return self.ball_model.is_out_of_bounds()
    
    def get_ball(self):
        return self.ball_model