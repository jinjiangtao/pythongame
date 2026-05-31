from settings import SCREEN_WIDTH

class Camera:
    def __init__(self):
        self.x = 0
    
    def update(self, player_x, world_width):
        # 简单有效的摄像头跟随：让玩家保持在屏幕左侧1/3位置
        # 这样玩家有足够空间看到前方，摄像头会跟随玩家前进
        target_x = player_x - SCREEN_WIDTH // 3
        
        # 始终跟随玩家，只要目标位置比当前位置更靠右就移动
        if target_x > self.x:
            self.x = min(target_x, world_width - SCREEN_WIDTH)
        
        # 确保摄像头不超出边界
        self.x = max(0, min(self.x, world_width - SCREEN_WIDTH))