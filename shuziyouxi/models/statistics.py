class Statistics:
    """数据统计模块 - 记录答题数据和计算正确率"""
    
    def __init__(self):
        self.total_questions = 0
        self.correct_answers = 0
        self.wrong_attempts = 0
    
    @property
    def accuracy(self):
        """计算正确率百分比"""
        if self.total_questions == 0:
            return 0
        return round((self.correct_answers / self.total_questions) * 100, 1)
    
    def record_correct(self):
        """记录正确答案"""
        self.total_questions += 1
        self.correct_answers += 1
    
    def record_wrong(self):
        """记录错误答案"""
        self.wrong_attempts += 1
    
    def reset(self):
        """重置所有统计数据"""
        self.total_questions = 0
        self.correct_answers = 0
        self.wrong_attempts = 0
    
    def get_summary(self):
        """获取统计摘要"""
        return {
            "total": self.total_questions,
            "correct": self.correct_answers,
            "wrong_attempts": self.wrong_attempts,
            "accuracy": self.accuracy
        }