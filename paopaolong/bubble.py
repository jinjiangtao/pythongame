import pygame
import math

class Bubble:
    """
    泡泡类 - 表示游戏中的单个泡泡
    
    属性:
        x: 泡泡中心的x坐标
        y: 泡泡中心的y坐标
        radius: 泡泡半径
        color: 泡泡颜色
        angle: 飞行泡泡的运动角度
        speed: 飞行泡泡的运动速度
        is_flying: 是否正在飞行中
        grid_pos: 六边形网格中的位置 (row, col)
    """
    
    # 泡泡颜色定义
    COLORS = [
        (255, 0, 0),       # 红色
        (0, 255, 0),       # 绿色
        (0, 0, 255),       # 蓝色
        (255, 255, 0),     # 黄色
        (255, 165, 0),     # 橙色
        (128, 0, 128),     # 紫色
        (255, 192, 203),   # 粉色
    ]
    
    def __init__(self, x, y, color=None):
        """
        初始化泡泡对象
        
        参数:
            x: 初始x坐标
            y: 初始y坐标
            color: 泡泡颜色，若为None则随机选择
        """
        self.x = x
        self.y = y
        self.radius = 15
        self.color = color if color else Bubble.COLORS[pygame.time.get_ticks() % len(Bubble.COLORS)]
        self.angle = 0
        self.speed = 6
        self.is_flying = False
        self.grid_pos = None
    
    def draw(self, screen):
        """
        在屏幕上绘制泡泡
        
        参数:
            screen: pygame显示表面
        """
        # 绘制泡泡主体
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # 绘制泡泡高光效果
        highlight_color = (255, 255, 255)
        highlight_radius = self.radius // 3
        highlight_x = self.x - self.radius // 3
        highlight_y = self.y - self.radius // 3
        pygame.draw.circle(screen, highlight_color, (int(highlight_x), int(highlight_y)), highlight_radius)
        
        # 绘制泡泡边框
        border_color = (0, 0, 0)
        pygame.draw.circle(screen, border_color, (int(self.x), int(self.y)), self.radius, 1)
    
    def update(self):
        """更新飞行泡泡的位置"""
        if self.is_flying:
            self.x += math.cos(self.angle) * self.speed
            self.y += math.sin(self.angle) * self.speed
    
    def set_flying(self, angle):
        """
        设置泡泡为飞行状态
        
        参数:
            angle: 飞行角度（弧度）
        """
        self.is_flying = True
        self.angle = angle
    
    def stop_flying(self):
        """停止泡泡飞行"""
        self.is_flying = False
    
    def check_collision(self, other):
        """
        检测与另一个泡泡的碰撞
        
        参数:
            other: 另一个泡泡对象
        
        返回:
            bool: 是否发生碰撞
        """
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx * dx + dy * dy)
        return distance <= self.radius + other.radius
    
    def check_wall_collision(self, screen_width, screen_height):
        """
        检测与墙壁的碰撞
        
        参数:
            screen_width: 屏幕宽度
            screen_height: 屏幕高度
        
        返回:
            str: 碰撞方向 'left', 'right', 'top', None
        """
        if self.x - self.radius <= 0:
            return 'left'
        if self.x + self.radius >= screen_width:
            return 'right'
        if self.y - self.radius <= 0:
            return 'top'
        return None
    
    def reflect(self, wall):
        """
        根据碰撞墙壁进行反弹
        
        参数:
            wall: 碰撞方向 'left', 'right', 'top'
        """
        if wall in ['left', 'right']:
            self.angle = math.pi - self.angle
        elif wall == 'top':
            self.angle = -self.angle
    
    @classmethod
    def get_random_color(cls):
        """获取随机泡泡颜色"""
        return cls.COLORS[pygame.time.get_ticks() % len(cls.COLORS)]
    
    @classmethod
    def get_color_by_index(cls, index):
        """
        根据索引获取颜色
        
        参数:
            index: 颜色索引
        
        返回:
            颜色元组
        """
        return cls.COLORS[index % len(cls.COLORS)]