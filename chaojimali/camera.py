from settings import SCREEN_WIDTH, CAMERA_FOLLOW_OFFSET

class Camera:
    def __init__(self):
        self.x = 0
    
    def update(self, player_x, world_width):
        target_x = player_x - CAMERA_FOLLOW_OFFSET
        
        if target_x > self.x:
            self.x = min(target_x, world_width - SCREEN_WIDTH)
        
        if self.x < 0:
            self.x = 0