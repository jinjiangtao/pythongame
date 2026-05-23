import math

class BallController:
    def __init__(self, ball_model, paddle_model, screen_width, screen_height):
        self.ball_model = ball_model
        self.paddle_model = paddle_model
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        self.ball_model.update()
        self._check_boundary_collisions()
        self._check_paddle_collision()

    def _check_boundary_collisions(self):
        left, top, right, bottom = self.ball_model.get_bounds()
        
        if left <= 0 or right >= self.screen_width:
            self.ball_model.reflect_horizontal()
            self.ball_model.x = max(self.ball_model.radius, min(self.screen_width - self.ball_model.radius, self.ball_model.x))
        
        if top <= 0:
            self.ball_model.reflect_vertical()
            self.ball_model.y = self.ball_model.radius

    def _check_paddle_collision(self):
        if not self.paddle_model:
            return
        
        paddle_left, paddle_top, paddle_right, paddle_bottom = self.paddle_model.get_bounds()
        ball_left, ball_top, ball_right, ball_bottom = self.ball_model.get_bounds()
        
        if (ball_bottom >= paddle_top and ball_top <= paddle_bottom and
            ball_right >= paddle_left and ball_left <= paddle_right):
            
            if self.paddle_model.suck_balls and not self.ball_model.stuck:
                self.ball_model.set_stuck(self.paddle_model.x, self.paddle_model.width)
                return
            
            hit_pos = (self.ball_model.x - paddle_left) / (paddle_right - paddle_left)
            angle = (hit_pos - 0.5) * math.pi * 0.7
            speed = math.sqrt(self.ball_model.dx ** 2 + self.ball_model.dy ** 2)
            self.ball_model.dx = speed * math.sin(angle)
            self.ball_model.dy = -abs(speed * math.cos(angle))
            self.ball_model.y = paddle_top - self.ball_model.radius

    def release_ball(self):
        if self.ball_model.stuck and self.paddle_model:
            self.ball_model.release(self.paddle_model.x, self.paddle_model.width)

    def is_off_screen(self):
        return self.ball_model.y > self.screen_height + self.ball_model.radius

    def reset(self, x, y):
        self.ball_model.reset(x, y)

    def get_ball(self):
        return self.ball_model
