import random
from typing import Tuple, List

class QuestionGenerator:
    """题目生成器 - 负责随机生成题目和图案"""
    
    PATTERNS = ["🍎", "🍊", "🍋", "🍇", "🍓", "🌸", "🌺", "🐱", "🐶", "🐰", "🐼", "🦋", "⭐", "🌙", "🌈"]
    
    def __init__(self):
        self.used_patterns = []
        self.used_numbers = []
    
    def generate_question(self, min_count: int, max_count: int) -> Tuple[int, str]:
        """生成一道题目
        
        Args:
            min_count: 图案数量最小值
            max_count: 图案数量最大值
            
        Returns:
            (数量, 图案字符)
        """
        available_patterns = [p for p in self.PATTERNS if p not in self.used_patterns]
        if not available_patterns:
            self.used_patterns.clear()
            available_patterns = self.PATTERNS
        
        pattern = random.choice(available_patterns)
        self.used_patterns.append(pattern)
        
        available_numbers = [n for n in range(min_count, max_count + 1) if n not in self.used_numbers]
        if not available_numbers:
            self.used_numbers.clear()
            available_numbers = list(range(min_count, max_count + 1))
        
        count = random.choice(available_numbers)
        self.used_numbers.append(count)
        
        return count, pattern
    
    def generate_positions(self, count: int, canvas_width: int, canvas_height: int, pattern_size: int) -> List[Tuple[int, int]]:
        """生成图案在画布上的随机位置，避免重叠
        
        Args:
            count: 图案数量
            canvas_width: 画布宽度
            canvas_height: 画布高度
            pattern_size: 图案大小
            
        Returns:
            位置坐标列表
        """
        positions = []
        padding = pattern_size // 2 + 20
        
        for _ in range(count):
            while True:
                x = random.randint(padding, canvas_width - padding)
                y = random.randint(padding, canvas_height - padding)
                
                # 检查是否与已有位置重叠
                overlap = False
                for (px, py) in positions:
                    distance = ((x - px) ** 2 + (y - py) ** 2) ** 0.5
                    if distance < pattern_size + 10:
                        overlap = True
                        break
                
                if not overlap:
                    positions.append((x, y))
                    break
        
        return positions
    
    def reset(self):
        """重置已使用的图案和数字记录"""
        self.used_patterns.clear()
        self.used_numbers.clear()