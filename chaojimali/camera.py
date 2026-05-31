from settings import SCREEN_WIDTH, CAMERA_FOLLOW_OFFSET

class Camera:
    def __init__(self):
        self.x = 0
    
    def update(self, player_x, world_width):
        target_x = player_x - CAMERA_FOLLOW_OFFSET
        
        # 只有当玩家超过屏幕中央右侧时，才让地图向左滚动
        # 这样玩家可以在屏幕左侧自由移动，不会触发摄像头滚动
        if target_x > self.x and player_x > CAMERA_FOLLOW_OFFSET:
            self.x = min(target_x, world_width - SCREEN_WIDTH)
        
        # 确保摄像头不超出边界
        self.x = max(0, min(self.x, world_width - SCREEN_WIDTH))