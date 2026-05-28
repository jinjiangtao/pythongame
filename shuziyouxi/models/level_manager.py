class LevelManager:
    """关卡管理器 - 管理关卡进度和难度设置"""
    
    def __init__(self):
        self.current_level = 1
        self.questions_per_level = 5
        self.current_question = 0
        self.level_configs = {
            1: {"min_count": 1, "max_count": 3, "name": "入门级"},
            2: {"min_count": 2, "max_count": 5, "name": "初级"},
            3: {"min_count": 3, "max_count": 7, "name": "中级"},
            4: {"min_count": 4, "max_count": 9, "name": "高级"},
            5: {"min_count": 5, "max_count": 10, "name": "挑战级"},
            6: {"min_count": 6, "max_count": 12, "name": "大师级"},
            7: {"min_count": 7, "max_count": 14, "name": "专家级"},
            8: {"min_count": 8, "max_count": 15, "name": "王者级"},
        }
    
    @property
    def current_config(self):
        """获取当前关卡配置"""
        level = min(self.current_level, max(self.level_configs.keys()))
        return self.level_configs[level]
    
    @property
    def level_name(self):
        """获取当前关卡名称"""
        return self.current_config["name"]
    
    @property
    def min_count(self):
        """获取当前关卡最小数量"""
        return self.current_config["min_count"]
    
    @property
    def max_count(self):
        """获取当前关卡最大数量"""
        return self.current_config["max_count"]
    
    def next_question(self):
        """进入下一题"""
        self.current_question += 1
    
    def check_level_up(self):
        """检查是否需要升级"""
        if self.current_question >= self.questions_per_level:
            self.level_up()
            return True
        return False
    
    def level_up(self):
        """升级到下一关"""
        if self.current_level < max(self.level_configs.keys()):
            self.current_level += 1
        self.current_question = 0
    
    def reset(self):
        """重置关卡到初始状态"""
        self.current_level = 1
        self.current_question = 0
    
    def get_progress(self):
        """获取当前关卡进度 (当前题目数/每关题目数)"""
        return (self.current_question, self.questions_per_level)