from model.prop_model import PropType

class PropController:
    def __init__(self, prop_manager, paddle_model, ball_controllers, game_model):
        self.prop_manager = prop_manager
        self.paddle_model = paddle_model
        self.ball_controllers = ball_controllers
        self.game_model = game_model
        
        self.prop_effects = {
            PropType.PADDLE_EXPAND: self._expand_paddle,
            PropType.PADDLE_SHRINK: self._shrink_paddle,
            PropType.BALL_ACCELERATE: self._accelerate_balls,
            PropType.BALL_DECELERATE: self._decelerate_balls,
            PropType.BALL_SPLIT: self._split_balls,
            PropType.EXTRA_LIFE: self._add_life,
            PropType.STICKY_PADDLE: self._make_sticky,
            PropType.INVINCIBLE: self._make_invincible
        }
    
    def update(self):
        self.prop_manager.update()
        
        collected_props = self.prop_manager.check_collision(self.paddle_model.get_rect())
        for prop in collected_props:
            self._apply_prop_effect(prop)
    
    def create_prop(self, brick_x, brick_y, brick_width, brick_height):
        self.prop_manager.create_prop(brick_x, brick_y, brick_width, brick_height)
    
    def _apply_prop_effect(self, prop):
        effect_func = self.prop_effects.get(prop.type)
        if effect_func:
            effect_func()
    
    def _expand_paddle(self):
        self.paddle_model.expand(factor=1.5, duration=10)
    
    def _shrink_paddle(self):
        self.paddle_model.shrink(factor=0.7, duration=10)
    
    def _accelerate_balls(self):
        for ball_ctrl in self.ball_controllers[:]:
            ball_ctrl.ball_model.accelerate(factor=1.15)
    
    def _decelerate_balls(self):
        for ball_ctrl in self.ball_controllers[:]:
            ball_ctrl.ball_model.decelerate(factor=0.85)
    
    def _split_balls(self):
        if len(self.ball_controllers) >= 5:
            return
        
        new_balls = []
        for ball_ctrl in self.ball_controllers[:]:
            if ball_ctrl.is_active():
                ball = ball_ctrl.ball_model
                speed = (ball.dx ** 2 + ball.dy ** 2) ** 0.5
                
                new_ball1 = type(ball)(ball.screen_width, ball.screen_height)
                new_ball1.x = ball.x
                new_ball1.y = ball.y
                new_ball1.dx = ball.dx * 0.8 - ball.dy * 0.3
                new_ball1.dy = ball.dy * 0.8 + ball.dx * 0.3
                new_ball1.set_speed(speed)
                
                new_ball2 = type(ball)(ball.screen_width, ball.screen_height)
                new_ball2.x = ball.x
                new_ball2.y = ball.y
                new_ball2.dx = ball.dx * 0.8 + ball.dy * 0.3
                new_ball2.dy = ball.dy * 0.8 - ball.dx * 0.3
                new_ball2.set_speed(speed)
                
                new_ctrl1 = type(ball_ctrl)(new_ball1, self.paddle_model)
                new_ctrl2 = type(ball_ctrl)(new_ball2, self.paddle_model)
                
                new_ctrl1.is_launched = True
                new_ctrl2.is_launched = True
                
                new_balls.extend([new_ctrl1, new_ctrl2])
        
        self.ball_controllers.extend(new_balls)
    
    def _add_life(self):
        self.game_model.add_life()
    
    def _make_sticky(self):
        self.paddle_model.set_sticky(duration=5)
    
    def _make_invincible(self):
        self.prop_manager.activate_invincible(duration=3)
    
    def is_invincible(self):
        return self.prop_manager.is_invincible()
    
    def get_props(self):
        return self.prop_manager.get_active_props()
    
    def clear_props(self):
        self.prop_manager.clear_props()
    
    def set_drop_probability(self, level):
        self.prop_manager.set_drop_probability(level)