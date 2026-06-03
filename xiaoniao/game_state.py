# game_state.py - 游戏状态管理

from settings import INITIAL_BIRDS, PIG_SCORE, BLOCK_SCORE

class GameState:
    def __init__(self):
        self.score = 0
        self.birds_left = INITIAL_BIRDS
        self.win = False
        self.lose = False
    
    def add_score(self, points):
        """增加分数"""
        self.score += points
    
    def check_win(self, pigs):
        """检查是否胜利（所有猪头被消灭）"""
        if all(not pig.alive for pig in pigs):
            self.win = True
    
    def check_lose(self):
        """检查是否失败（没有小鸟且猪头还在）"""
        if self.birds_left <= 0:
            self.lose = True
    
    def is_game_over(self):
        """检查游戏是否结束"""
        return self.win or self.lose
    
    def reset(self):
        """重置游戏状态"""
        self.score = 0
        self.birds_left = INITIAL_BIRDS
        self.win = False
        self.lose = False