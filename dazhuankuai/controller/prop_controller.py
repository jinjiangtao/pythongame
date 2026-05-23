class PropController:
    def __init__(self, prop_model, paddle_model, game_model, ball_controllers):
        self.prop_model = prop_model
        self.paddle_model = paddle_model
        self.game_model = game_model
        self.ball_controllers = ball_controllers

    def update(self):
        self.prop_model.update()
        self._check_paddle_collision()

    def _check_paddle_collision(self):
        if not self.paddle_model or self.prop_model.collected:
            return
        
        paddle_left, paddle_top, paddle_right, paddle_bottom = self.paddle_model.get_bounds()
        prop_left, prop_top, prop_right, prop_bottom = self.prop_model.get_bounds()
        
        if (prop_bottom >= paddle_top and prop_top <= paddle_bottom and
            prop_right >= paddle_left and prop_left <= paddle_right):
            self.prop_model.collected = True
            self._apply_effect()

    def _apply_effect(self):
        prop_type = self.prop_model.type
        
        if prop_type == 'expand_paddle':
            self.paddle_model.expand()
        
        elif prop_type == 'shrink_paddle':
            self.paddle_model.shrink()
        
        elif prop_type == 'speed_up':
            for bc in self.ball_controllers:
                bc.get_ball().accelerate(1.3)
        
        elif prop_type == 'speed_down':
            for bc in self.ball_controllers:
                bc.get_ball().decelerate(0.7)
        
        elif prop_type == 'multi_ball':
            new_balls = []
            for bc in self.ball_controllers:
                ball = bc.get_ball()
                if not ball.stuck:
                    new_balls.extend(ball.split())
            self.game_model.balls.extend(new_balls)
        
        elif prop_type == 'extra_life':
            self.game_model.add_life()
        
        elif prop_type == 'suck_paddle':
            self.paddle_model.activate_suck(self.prop_model.duration)
        
        elif prop_type == 'invincible':
            for bc in self.ball_controllers:
                bc.get_ball().activate_invincible(self.prop_model.duration)

    def is_off_screen(self, screen_height):
        return self.prop_model.y > screen_height + self.prop_model.radius

    def get_prop(self):
        return self.prop_model
