import random

class BrickType:
    NORMAL = 'normal'
    REINFORCED = 'reinforced'
    INDESTRUCTIBLE = 'indestructible'
    EXPLOSIVE = 'explosive'

class Brick:
    def __init__(self, x, y, width, height, brick_type=BrickType.NORMAL):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = brick_type
        self.health = self._get_initial_health()
        self.max_health = self.health
        self.destroyed = False
        self.hit_count = 0

    def _get_initial_health(self):
        if self.type == BrickType.NORMAL:
            return 1
        elif self.type == BrickType.REINFORCED:
            return random.randint(2, 3)
        elif self.type == BrickType.INDESTRUCTIBLE:
            return 999
        elif self.type == BrickType.EXPLOSIVE:
            return 1
        return 1

    def hit(self):
        if self.type == BrickType.INDESTRUCTIBLE:
            return False, False
        
        self.hit_count += 1
        self.health -= 1
        
        if self.health <= 0:
            self.destroyed = True
            return True, self.type == BrickType.EXPLOSIVE
        
        return False, False

    def get_rect(self):
        return (self.x, self.y, self.width, self.height)

    def is_destroyed(self):
        return self.destroyed

class BrickManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bricks = []
        self.brick_width = 70
        self.brick_height = 25
        self.padding = 5
        self.offset_x = 35
        self.offset_y = 60

    def generate_level(self, level):
        self.bricks = []
        rows = self._get_rows_by_level(level)
        cols = self._get_cols_by_level(level)
        self._adjust_brick_size(rows, cols)
        
        brick_types = self._get_brick_types_distribution(level)
        
        for row in range(rows):
            for col in range(cols):
                x = self.offset_x + col * (self.brick_width + self.padding)
                y = self.offset_y + row * (self.brick_height + self.padding)
                
                if x + self.brick_width > self.screen_width:
                    continue
                
                brick_type = self._select_brick_type(brick_types, row, rows)
                brick = Brick(x, y, self.brick_width, self.brick_height, brick_type)
                self.bricks.append(brick)

    def _get_rows_by_level(self, level):
        return min(5 + level, 10)

    def _get_cols_by_level(self, level):
        return min(10 + level // 2, 12)

    def _adjust_brick_size(self, rows, cols):
        total_width = cols * (self.brick_width + self.padding) - self.padding
        total_height = rows * (self.brick_height + self.padding) - self.padding
        
        if total_width > self.screen_width - 70:
            scale = (self.screen_width - 70) / total_width
            self.brick_width = int(self.brick_width * scale)
            self.brick_height = int(self.brick_height * scale)
        
        self.offset_x = (self.screen_width - cols * (self.brick_width + self.padding) + self.padding) // 2

    def _get_brick_types_distribution(self, level):
        return {
            BrickType.NORMAL: max(60 - level * 5, 20),
            BrickType.REINFORCED: min(25 + level * 5, 50),
            BrickType.INDESTRUCTIBLE: min(5 + level * 2, 15),
            BrickType.EXPLOSIVE: min(10 + level, 15)
        }

    def _select_brick_type(self, types_dist, row, total_rows):
        rand = random.randint(1, 100)
        cumulative = 0
        
        for brick_type, percentage in types_dist.items():
            cumulative += percentage
            if rand <= cumulative:
                return brick_type
        
        return BrickType.NORMAL

    def check_collision(self, ball_rect):
        hit_bricks = []
        explosive_hits = []
        
        for brick in self.bricks:
            if brick.is_destroyed():
                continue
            
            bx, by, bw, bh = brick.get_rect()
            if (ball_rect[0] < bx + bw and 
                ball_rect[0] + ball_rect[2] > bx and 
                ball_rect[1] < by + bh and 
                ball_rect[1] + ball_rect[3] > by):
                
                destroyed, is_explosive = brick.hit()
                hit_bricks.append(brick)
                
                if is_explosive:
                    explosive_hits.append(brick)
        
        for explosive_brick in explosive_hits:
            self._trigger_explosion(explosive_brick)
        
        return hit_bricks

    def _trigger_explosion(self, explosive_brick):
        ex, ey, ew, eh = explosive_brick.get_rect()
        explosion_radius = 80
        
        for brick in self.bricks:
            if brick.is_destroyed() or brick is explosive_brick:
                continue
            
            bx, by, bw, bh = brick.get_rect()
            brick_center_x = bx + bw // 2
            brick_center_y = by + bh // 2
            explosive_center_x = ex + ew // 2
            explosive_center_y = ey + eh // 2
            
            distance = ((brick_center_x - explosive_center_x) ** 2 + 
                        (brick_center_y - explosive_center_y) ** 2) ** 0.5
            
            if distance < explosion_radius:
                if brick.type != BrickType.INDESTRUCTIBLE:
                    brick.destroyed = True

    def get_all_bricks(self):
        return self.bricks

    def get_active_bricks(self):
        return [brick for brick in self.bricks if not brick.is_destroyed()]

    def is_level_complete(self):
        return all(brick.is_destroyed() or brick.type == BrickType.INDESTRUCTIBLE 
                   for brick in self.bricks)