import random
from model.brick_model import BrickGenerator
from model.ball_model import BallModel
from model.paddle_model import PaddleModel

class LevelController:
    def __init__(self, game_model, screen_width, screen_height):
        self.game_model = game_model
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.brick_generator = BrickGenerator(screen_width, screen_height)
        self.countdown = 0

    def start_level(self, level):
        self.game_model.bricks = self.brick_generator.generate_level(level)
        self.game_model.paddle = PaddleModel(self.screen_width // 2, self.screen_height - 50)
        self.game_model.balls = [BallModel(self.screen_width // 2, self.screen_height - 70)]
        self.game_model.props = []
        self.game_model.explosions = []
        self.countdown = 3

    def update_countdown(self):
        if self.countdown > 0:
            self.countdown -= 1
            return self.countdown
        return 0

    def is_countdown_complete(self):
        return self.countdown <= 0

    def handle_ball_brick_collisions(self, ball_controller, prop_generator):
        ball = ball_controller.get_ball()
        if ball.stuck:
            return
        
        ball_left, ball_top, ball_right, ball_bottom = ball.get_bounds()
        
        for brick in self.game_model.bricks:
            if brick.destroyed:
                continue
            
            brick_left, brick_top, brick_right, brick_bottom = brick.get_bounds()
            
            if (ball_right > brick_left and ball_left < brick_right and
                ball_bottom > brick_top and ball_top < brick_bottom):
                
                destroyed, points, is_explosive = brick.hit()
                
                if destroyed:
                    self.game_model.add_score(points, brick.get_center()[0], brick.get_center()[1])
                    
                    prop = prop_generator.generate(brick.get_center()[0], brick.get_center()[1])
                    if prop:
                        self.game_model.props.append(prop)
                    
                    if is_explosive:
                        self._trigger_explosion(brick.get_center()[0], brick.get_center()[1], prop_generator)
                
                self._reflect_ball_on_brick(ball, brick)
                break

    def _reflect_ball_on_brick(self, ball, brick):
        ball_center_x, ball_center_y = ball.x, ball.y
        brick_center_x, brick_center_y = brick.get_center()
        
        dx = ball_center_x - brick_center_x
        dy = ball_center_y - brick_center_y
        
        brick_width = brick.width
        brick_height = brick.height
        
        if abs(dx / brick_width) > abs(dy / brick_height):
            ball.reflect_horizontal()
        else:
            ball.reflect_vertical()

    def _trigger_explosion(self, x, y, prop_generator):
        self.game_model.explosions.append({'x': x, 'y': y, 'radius': 80, 'frame': 0})
        
        for brick in self.game_model.bricks:
            if brick.destroyed:
                continue
            
            bx, by = brick.get_center()
            distance = ((bx - x) ** 2 + (by - y) ** 2) ** 0.5
            
            if distance < 100:
                brick.destroyed = True
                self.game_model.add_score(brick.points, bx, by)
                
                if random.random() < 0.3:
                    prop = prop_generator.generate(bx, by)
                    if prop:
                        self.game_model.props.append(prop)

    def update_explosions(self):
        self.game_model.explosions = [exp for exp in self.game_model.explosions if exp['frame'] < 30]
        for exp in self.game_model.explosions:
            exp['frame'] += 1
            exp['radius'] += 2

    def check_level_complete(self):
        return self.game_model.is_level_complete()

    def get_paddle(self):
        return self.game_model.paddle
