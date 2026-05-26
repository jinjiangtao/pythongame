import pygame
import math
from bubble import Bubble, BubbleType

class PowerupSystem:
    """道具系统 - 处理道具泡泡的效果"""

    def __init__(self, game):
        """
        初始化道具系统
        
        参数:
            game: 游戏主对象
        """
        self.game = game

    def activate_bomb_bubble(self, bomb_bubble):
        """
        激活炸弹泡泡效果 - 消除周围一圈泡泡
        
        参数:
            bomb_bubble: 炸弹泡泡对象
        """
        if bomb_bubble.bubble_type != BubbleType.BOMB:
            return []
        
        affected_bubbles = []
        bomb_radius = bomb_bubble.radius * 3
        
        for bubble in self.game.bubbles:
            if bubble == bomb_bubble:
                continue
            if bubble.bubble_type == BubbleType.OBSTACLE:
                continue
            
            dx = bomb_bubble.x - bubble.x
            dy = bomb_bubble.y - bubble.y
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance <= bomb_radius:
                affected_bubbles.append(bubble)
        
        return affected_bubbles

    def activate_rainbow_bubble(self, rainbow_bubble):
        """
        激活彩虹泡泡效果 - 可替代任意颜色泡泡
        
        参数:
            rainbow_bubble: 彩虹泡泡对象
        
        返回:
            最优匹配的颜色
        """
        if rainbow_bubble.bubble_type != BubbleType.RAINBOW:
            return rainbow_bubble.color
        
        color_counts = {}
        for bubble in self.game.bubbles:
            if bubble == rainbow_bubble:
                continue
            if bubble.bubble_type == BubbleType.OBSTACLE:
                continue
            
            dx = rainbow_bubble.x - bubble.x
            dy = rainbow_bubble.y - bubble.y
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance <= rainbow_bubble.radius * 3:
                color = bubble.color
                if color not in color_counts:
                    color_counts[color] = 0
                color_counts[color] += 1
        
        if color_counts:
            return max(color_counts, key=color_counts.get)
        
        return Bubble.get_random_color()

    def handle_pierce_collision(self, flying_bubble, target_bubble):
        """
        处理穿透泡泡碰撞
        
        参数:
            flying_bubble: 飞行中的泡泡
            target_bubble: 被碰撞的泡泡
        
        返回:
            bool: 是否应该穿透（不放置）
        """
        if not flying_bubble.can_pierce():
            return False
        
        if target_bubble.bubble_type == BubbleType.OBSTACLE:
            return False
        
        if flying_bubble.color != target_bubble.color:
            flying_bubble.mark_pierced()
            return True
        
        return False

    def should_ignore_collision(self, flying_bubble, target_bubble):
        """
        判断是否应该忽略碰撞
        
        参数:
            flying_bubble: 飞行中的泡泡
            target_bubble: 被碰撞的泡泡
        
        返回:
            bool: 是否忽略碰撞
        """
        if flying_bubble.bubble_type == BubbleType.PIERCE and not flying_bubble.has_pierced:
            if target_bubble.bubble_type != BubbleType.OBSTACLE:
                if flying_bubble.color != target_bubble.color:
                    return True
        
        return False

    def get_random_powerup_bubble(self, x, y):
        """
        随机生成道具泡泡（低概率）
        
        参数:
            x: x坐标
            y: y坐标
        
        返回:
            Bubble: 道具泡泡或普通泡泡
        """
        rand = pygame.time.get_ticks() % 100
        
        if rand < 3:
            return Bubble.create_bomb_bubble(x, y)
        elif rand < 6:
            return Bubble.create_rainbow_bubble(x, y)
        elif rand < 9:
            return Bubble.create_pierce_bubble(x, y)
        
        return Bubble(x, y)