import random

class PropType:
    PADDLE_EXPAND = 'paddle_expand'
    PADDLE_SHRINK = 'paddle_shrink'
    BALL_ACCELERATE = 'ball_accelerate'
    BALL_DECELERATE = 'ball_decelerate'
    BALL_SPLIT = 'ball_split'
    EXTRA_LIFE = 'extra_life'
    STICKY_PADDLE = 'sticky_paddle'
    INVINCIBLE = 'invincible'

class PropModel:
    def __init__(self, x, y, prop_type):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.type = prop_type
        self.speed = 3
        self.active = True
        self.picked = False

    def update(self):
        if self.active:
            self.y += self.speed

    def get_rect(self):
        return (self.x, self.y, self.width, self.height)

    def is_out_of_bounds(self, screen_height):
        return self.y > screen_height + 50

    def pick(self):
        self.picked = True
        self.active = False

class PropManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.props = []
        self.drop_probability = 0.2
        self.invincible_active = False
        self.invincible_timer = 0

    def set_drop_probability(self, level):
        self.drop_probability = max(0.1, 0.3 - level * 0.03)

    def create_prop(self, brick_x, brick_y, brick_width, brick_height):
        if random.random() > self.drop_probability:
            return
        
        prop_types = [
            PropType.PADDLE_EXPAND,
            PropType.PADDLE_SHRINK,
            PropType.BALL_ACCELERATE,
            PropType.BALL_DECELERATE,
            PropType.BALL_SPLIT,
            PropType.EXTRA_LIFE,
            PropType.STICKY_PADDLE,
            PropType.INVINCIBLE
        ]
        
        weights = [20, 15, 10, 15, 15, 10, 10, 5]
        total_weight = sum(weights)
        rand = random.randint(1, total_weight)
        
        cumulative = 0
        prop_type = PropType.PADDLE_EXPAND
        for i, weight in enumerate(weights):
            cumulative += weight
            if rand <= cumulative:
                prop_type = prop_types[i]
                break
        
        x = brick_x + brick_width // 2 - 10
        y = brick_y + brick_height
        prop = PropModel(x, y, prop_type)
        self.props.append(prop)

    def update(self):
        for prop in self.props[:]:
            prop.update()
            if prop.is_out_of_bounds(self.screen_height):
                self.props.remove(prop)
        
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible_active = False

    def check_collision(self, paddle_rect):
        collected_props = []
        
        for prop in self.props[:]:
            px, py, pw, ph = prop.get_rect()
            pad_x, pad_y, pad_w, pad_h = paddle_rect
            
            if (px < pad_x + pad_w and 
                px + pw > pad_x and 
                py < pad_y + pad_h and 
                py + ph > pad_y):
                
                prop.pick()
                collected_props.append(prop)
                self.props.remove(prop)
        
        return collected_props

    def activate_invincible(self, duration=3):
        self.invincible_active = True
        self.invincible_timer = duration * 60

    def is_invincible(self):
        return self.invincible_active

    def get_active_props(self):
        return self.props

    def clear_props(self):
        self.props = []