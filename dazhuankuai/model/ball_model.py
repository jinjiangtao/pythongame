import math

class BallModel:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.width = 10
        self.height = 10
        
        self.base_speed = 5
        self.speed = self.base_speed
        self.max_speed = 12
        self.min_speed = 3
        
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - 60
        
        self.dx = 0
        self.dy = -self.speed
        
        self.gravity = 0.02
        self.bounce_factor = 0.98
        
        self.trail = []
        self.max_trail_length = 10
        
        self.active = True
        self.has_collided = False

    def reset(self, paddle_x, paddle_width):
        self.x = paddle_x + paddle_width // 2 - self.width // 2
        self.y = self.screen_height - 60
        self.dx = 0
        self.dy = -self.speed
        self.active = True
        self.trail = []

    def set_speed(self, speed):
        self.speed = max(self.min_speed, min(self.max_speed, speed))
        current_speed = math.sqrt(self.dx ** 2 + self.dy ** 2)
        if current_speed > 0:
            self.dx = (self.dx / current_speed) * self.speed
            self.dy = (self.dy / current_speed) * self.speed

    def accelerate(self, factor=1.1):
        new_speed = self.speed * factor
        self.set_speed(new_speed)

    def decelerate(self, factor=0.9):
        new_speed = self.speed * factor
        self.set_speed(new_speed)

    def update(self):
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        
        self.dy += self.gravity
        
        self.x += self.dx
        self.y += self.dy
        
        if self.x <= 0 or self.x + self.width >= self.screen_width:
            self.dx = -self.dx * self.bounce_factor
            self.x = max(0, min(self.screen_width - self.width, self.x))
        
        if self.y <= 0:
            self.dy = -self.dy * self.bounce_factor
            self.y = 0

    def bounce_off_paddle(self, hit_position):
        angle = (hit_position - 0.5) * math.pi * 0.7
        speed = math.sqrt(self.dx ** 2 + self.dy ** 2)
        
        self.dx = speed * math.sin(angle)
        self.dy = -abs(speed * math.cos(angle))
        
        if abs(self.dx) < 0.5:
            self.dx = 0.5 if self.dx > 0 else -0.5

    def bounce_off_brick(self, ball_rect, brick_rect):
        bx, by, bw, bh = ball_rect
        rx, ry, rw, rh = brick_rect
        
        overlap_left = bx + bw - rx
        overlap_right = rx + rw - bx
        overlap_top = by + bh - ry
        overlap_bottom = ry + rh - by
        
        min_overlap_x = min(overlap_left, overlap_right)
        min_overlap_y = min(overlap_top, overlap_bottom)
        
        if min_overlap_x < min_overlap_y:
            self.dx = -self.dx
        else:
            self.dy = -self.dy

    def get_rect(self):
        return (self.x, self.y, self.width, self.height)

    def is_out_of_bounds(self):
        return self.y > self.screen_height + 20

    def get_trail(self):
        return self.trail

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False
        self.trail = []