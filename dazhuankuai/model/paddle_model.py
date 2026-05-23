class PaddleModel:
    def __init__(self, x, y, width=100, height=15):
        self.x = x
        self.y = y
        self.base_width = width
        self.width = width
        self.height = height
        self.speed = 8.0
        self.target_x = x
        self.suck_balls = False
        self.suck_timer = 0

    def update(self):
        dx = self.target_x - self.x
        if abs(dx) < self.speed:
            self.x = self.target_x
        else:
            self.x += self.speed * (1 if dx > 0 else -1)
        if self.suck_balls:
            self.suck_timer -= 1
            if self.suck_timer <= 0:
                self.suck_balls = False

    def move_left(self, screen_width):
        self.target_x = max(self.width // 2, self.target_x - self.speed)

    def move_right(self, screen_width):
        self.target_x = min(screen_width - self.width // 2, self.target_x + self.speed)

    def set_position(self, x, screen_width):
        self.target_x = max(self.width // 2, min(screen_width - self.width // 2, x))

    def expand(self, factor=1.5):
        self.width = min(self.base_width * 2, self.width * factor)

    def shrink(self, factor=0.7):
        self.width = max(self.base_width * 0.5, self.width * factor)

    def reset_width(self):
        self.width = self.base_width

    def activate_suck(self, duration):
        self.suck_balls = True
        self.suck_timer = duration

    def get_bounds(self):
        return (self.x - self.width // 2, self.y - self.height // 2,
                self.x + self.width // 2, self.y + self.height // 2)

    def get_top_center(self):
        return (self.x, self.y - self.height // 2)
