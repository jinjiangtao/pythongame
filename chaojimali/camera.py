from settings import SCREEN_WIDTH, CAMERA_FOLLOW_OFFSET

class Camera:
    def __init__(self):
        self.x = 0
    
    def update(self, player_x, world_width):
        target_x = player_x - CAMERA_FOLLOW_OFFSET
        
        # 让摄像头跟随玩家，平滑移动
        if target_x > self.x:
            # 向右移动
            self.x = min(target_x, world_width - SCREEN_WIDTH)
        elif target_x < self.x - 50:  # 增加一些缓冲，避免来回晃荡
            # 向左移动，有缓冲避免过度移动
            self.x = max(target_x, 0)
        
        # 确保摄像头不超出边界
        self.x = max(0, min(self.x, world_width - SCREEN_WIDTH))