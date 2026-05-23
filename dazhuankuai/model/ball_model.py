import math

class BallModel:
    def __init__(self, x, y, radius=8):
        self.x = x
        self.y = y
        self.radius = radius
        self.base_speed = 5.0
        self.speed = self.base_speed
        self.dx = self.speed
        self.dy = -self.speed
        self.trail = []
        self.max_trail_length = 10
        self.stuck = False
        self.stuck_position = 0.0
        self.invincible = False
        self.invincible_timer = 0

    def update(self):
        if not self.stuck:
            self.x += self.dx
            self.y += self.dy
            self.trail.append((self.x, self.y))
            if len(self.trail) > self.max_trail_length:
                self.trail.pop(0)
            if self.invincible:
                self.invincible_timer -= 1
                if self.invincible_timer <= 0:
                    self.invincible = False

    def reflect(self, surface_normal_x, surface_normal_y):
        dot_product = self.dx * surface_normal_x + self.dy * surface_normal_y
        self.dx -= 2 * dot_product * surface_normal_x
        self.dy -= 2 * dot_product * surface_normal_y
        speed_magnitude = math.sqrt(self.dx ** 2 + self.dy ** 2)
        if speed_magnitude > 0:
            self.dx = (self.dx / speed_magnitude) * self.speed
            self.dy = (self.dy / speed_magnitude) * self.speed

    def reflect_horizontal(self):
        self.dx = -self.dx

    def reflect_vertical(self):
        self.dy = -self.dy

    def set_speed(self, speed):
        self.speed = speed
        speed_magnitude = math.sqrt(self.dx ** 2 + self.dy ** 2)
        if speed_magnitude > 0:
            self.dx = (self.dx / speed_magnitude) * self.speed
            self.dy = (self.dy / speed_magnitude) * self.speed

    def accelerate(self, factor):
        self.speed *= factor
        self.set_speed(self.speed)

    def decelerate(self, factor):
        self.speed = max(self.base_speed * 0.5, self.speed * factor)
        self.set_speed(self.speed)

    def split(self):
        new_balls = []
        angle1 = math.radians(-15)
        angle2 = math.radians(15)
        for angle in [angle1, angle2]:
            new_ball = BallModel(self.x, self.y, self.radius)
            new_ball.speed = self.speed
            new_ball.dx = self.dx * math.cos(angle) - self.dy * math.sin(angle)
            new_ball.dy = self.dx * math.sin(angle) + self.dy * math.cos(angle)
            new_balls.append(new_ball)
        return new_balls

    def set_stuck(self, paddle_x, paddle_width):
        self.stuck = True
        self.stuck_position = (self.x - paddle_x) / paddle_width

    def release(self, paddle_x, paddle_width):
        self.stuck = False
        self.x = paddle_x + self.stuck_position * paddle_width
        self.y -= self.radius + 5
        angle = (self.stuck_position - 0.5) * math.pi * 0.7
        self.dx = self.speed * math.sin(angle)
        self.dy = -self.speed * math.cos(angle)

    def activate_invincible(self, duration):
        self.invincible = True
        self.invincible_timer = duration

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.speed = self.base_speed
        self.dx = self.speed
        self.dy = -self.speed
        self.trail = []
        self.stuck = False
        self.stuck_position = 0.0
        self.invincible = False
        self.invincible_timer = 0

    def get_bounds(self):
        return (self.x - self.radius, self.y - self.radius,
                self.x + self.radius, self.y + self.radius)
