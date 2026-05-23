class PaddleModel:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.base_width = 120
        self.base_height = 15
        self.width = self.base_width
        self.height = self.base_height
        
        self.x = (screen_width - self.width) // 2
        self.y = screen_height - 40
        
        self.speed = 8
        self.max_speed = 12
        
        self.is_holding_ball = False
        self.ball_offset = 0
        
        self.size_multiplier = 1.0
        self.size_effect_timer = 0
        
        self.sticky = False
        self.sticky_timer = 0

    def move_left(self):
        self.x = max(0, self.x - self.speed)

    def move_right(self):
        self.x = min(self.screen_width - self.width, self.x + self.speed)

    def move_to(self, x):
        self.x = max(0, min(self.screen_width - self.width, x - self.width // 2))

    def get_rect(self):
        return (self.x, self.y, self.width, self.height)

    def get_center_x(self):
        return self.x + self.width // 2

    def expand(self, factor=1.5, duration=10):
        self.size_multiplier = factor
        self.width = int(self.base_width * factor)
        self.size_effect_timer = duration * 60
        
        if self.x + self.width > self.screen_width:
            self.x = self.screen_width - self.width

    def shrink(self, factor=0.7, duration=10):
        self.size_multiplier = factor
        self.width = int(self.base_width * factor)
        self.size_effect_timer = duration * 60

    def reset_size(self):
        self.width = self.base_width
        self.size_multiplier = 1.0
        self.size_effect_timer = 0

    def set_sticky(self, duration=5):
        self.sticky = True
        self.sticky_timer = duration * 60

    def clear_sticky(self):
        self.sticky = False
        self.sticky_timer = 0

    def update(self):
        if self.size_effect_timer > 0:
            self.size_effect_timer -= 1
            if self.size_effect_timer <= 0:
                self.reset_size()
        
        if self.sticky_timer > 0:
            self.sticky_timer -= 1
            if self.sticky_timer <= 0:
                self.clear_sticky()

    def check_collision(self, ball_rect):
        px, py, pw, ph = self.get_rect()
        bx, by, bw, bh = ball_rect
        
        if (bx < px + pw and 
            bx + bw > px and 
            by < py + ph and 
            by + bh > py):
            
            hit_position = (bx + bw // 2 - px) / pw
            return True, hit_position
        
        return False, 0.0

    def hold_ball(self, ball):
        self.is_holding_ball = True
        self.ball_offset = ball.x + ball.width // 2 - self.x

    def release_ball(self):
        self.is_holding_ball = False
        return self.x + self.ball_offset