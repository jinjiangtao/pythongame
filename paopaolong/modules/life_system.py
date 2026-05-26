class LifeSystem:
    """生命系统 - 管理玩家生命值"""

    def __init__(self, game, max_lives=3):
        """
        初始化生命系统
        
        参数:
            game: 游戏主对象
            max_lives: 最大生命值
        """
        self.game = game
        self.max_lives = max_lives
        self.lives = max_lives
        self.invincible_timer = 0
        self.is_invincible = False

    def lose_life(self):
        """扣除一条生命"""
        if self.is_invincible:
            return False
        
        self.lives -= 1
        self.is_invincible = True
        self.invincible_timer = 2000  # 2秒无敌时间
        
        if self.lives <= 0:
            self.lives = 0
            self.game.game_state = 'gameover'
            return False
        
        return True

    def add_life(self):
        """增加一条生命"""
        if self.lives < self.max_lives:
            self.lives += 1
            return True
        return False

    def reset_lives(self):
        """重置生命值"""
        self.lives = self.max_lives
        self.is_invincible = False
        self.invincible_timer = 0

    def update(self):
        """更新生命系统状态"""
        if self.is_invincible:
            self.invincible_timer -= 16  # 约60fps
            if self.invincible_timer <= 0:
                self.is_invincible = False
                self.invincible_timer = 0

    def is_game_over(self):
        """检查游戏是否结束"""
        return self.lives <= 0

    def get_life_percentage(self):
        """获取生命值百分比"""
        return self.lives / self.max_lives

    def draw(self, screen):
        """绘制生命值显示"""
        center_x = self.game.width // 2
        y = self.game.height - 25
        
        for i in range(self.max_lives):
            x = center_x - (self.max_lives - 1) * 20 + i * 40
            
            if i < self.lives:
                color = (255, 100, 100)
            else:
                color = (50, 50, 50)
            
            pygame.draw.polygon(screen, color, [
                (x, y + 8),
                (x - 12, y),
                (x - 12, y + 6),
                (x, y + 12),
                (x + 12, y + 6),
                (x + 12, y),
            ])

import pygame