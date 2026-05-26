import pygame
import math

class BubbleType:
    """泡泡类型枚举"""
    NORMAL = 'normal'
    BOMB = 'bomb'
    RAINBOW = 'rainbow'
    PIERCE = 'pierce'
    OBSTACLE = 'obstacle'

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
        bubble_type: 泡泡类型
        has_pierced: 是否已经穿透过一个泡泡
    """

    COLORS = [
        (255, 0, 0),       # 红色
        (0, 255, 0),       # 绿色
        (0, 0, 255),       # 蓝色
        (255, 255, 0),     # 黄色
        (255, 165, 0),     # 橙色
        (128, 0, 128),     # 紫色
        (255, 192, 203),   # 粉色
    ]

    def __init__(self, x, y, color=None, bubble_type=BubbleType.NORMAL):
        """
        初始化泡泡对象
        
        参数:
            x: 初始x坐标
            y: 初始y坐标
            color: 泡泡颜色，若为None则随机选择
            bubble_type: 泡泡类型
        """
        self.x = x
        self.y = y
        self.radius = 15
        self.color = color if color else Bubble.COLORS[pygame.time.get_ticks() % len(Bubble.COLORS)]
        self.angle = 0
        self.speed = 6
        self.is_flying = False
        self.grid_pos = None
        self.bubble_type = bubble_type
        self.has_pierced = False
        self.scale = 1.0
        self.scale_direction = 1
        self.pulse_speed = 0.03
        self.target_color = self.color
        self.color_progress = 0

    def draw(self, screen):
        """
        在屏幕上绘制泡泡
        
        参数:
            screen: pygame显示表面
        """
        if self.bubble_type == BubbleType.OBSTACLE:
            self._draw_obstacle_bubble(screen)
        elif self.bubble_type == BubbleType.BOMB:
            self._draw_bomb_bubble(screen)
        elif self.bubble_type == BubbleType.RAINBOW:
            self._draw_rainbow_bubble(screen)
        elif self.bubble_type == BubbleType.PIERCE:
            self._draw_pierce_bubble(screen)
        else:
            self._draw_normal_bubble(screen)

    def _draw_normal_bubble(self, screen):
        """绘制普通泡泡"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius * self.scale))
        highlight_color = (255, 255, 255)
        highlight_radius = int((self.radius // 3) * self.scale)
        highlight_x = self.x - (self.radius // 3)
        highlight_y = self.y - (self.radius // 3)
        pygame.draw.circle(screen, highlight_color, (int(highlight_x), int(highlight_y)), highlight_radius)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), int(self.radius * self.scale), 1)

    def _draw_bomb_bubble(self, screen):
        """绘制炸弹泡泡 - 带有爆炸图标"""
        pygame.draw.circle(screen, (255, 100, 100), (int(self.x), int(self.y)), int(self.radius * self.scale))
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), int(self.radius * self.scale), 2)
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), int(self.radius * 0.5 * self.scale))
        pygame.draw.polygon(screen, (0, 0, 0), [
            (int(self.x), int(self.y) - 5),
            (int(self.x) + 3, int(self.y)),
            (int(self.x), int(self.y) + 5),
            (int(self.x) - 3, int(self.y))
        ])

    def _draw_rainbow_bubble(self, screen):
        """绘制彩虹泡泡 - 动态变色"""
        self.color_progress += 0.05
        rainbow_colors = [
            (255, 0, 0), (255, 127, 0), (255, 255, 0),
            (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)
        ]
        idx = int(self.color_progress % len(rainbow_colors))
        current_color = rainbow_colors[idx]
        pygame.draw.circle(screen, current_color, (int(self.x), int(self.y)), int(self.radius * self.scale))
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), int(self.radius * self.scale), 2)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x - 5), int(self.y - 5)), 5)

    def _draw_pierce_bubble(self, screen):
        """绘制穿透泡泡 - 带有箭头图标"""
        pygame.draw.circle(screen, (100, 200, 255), (int(self.x), int(self.y)), int(self.radius * self.scale))
        pygame.draw.circle(screen, (0, 0, 255), (int(self.x), int(self.y)), int(self.radius * self.scale), 2)
        for i in range(4):
            angle = i * math.pi / 2
            arrow_x = self.x + math.cos(angle) * (self.radius * 0.6)
            arrow_y = self.y + math.sin(angle) * (self.radius * 0.6)
            pygame.draw.polygon(screen, (255, 255, 255), [
                (arrow_x, arrow_y),
                (arrow_x + math.cos(angle) * 4, arrow_y + math.sin(angle) * 4),
                (arrow_x + math.cos(angle + 0.3) * 3, arrow_y + math.sin(angle + 0.3) * 3),
                (arrow_x + math.cos(angle - 0.3) * 3, arrow_y + math.sin(angle - 0.3) * 3)
            ])

    def _draw_obstacle_bubble(self, screen):
        """绘制障碍物泡泡 - 不可消除"""
        pygame.draw.circle(screen, (60, 60, 60), (int(self.x), int(self.y)), int(self.radius * self.scale))
        pygame.draw.circle(screen, (100, 100, 100), (int(self.x), int(self.y)), int(self.radius * 0.8 * self.scale))
        pygame.draw.circle(screen, (80, 80, 80), (int(self.x), int(self.y)), int(self.radius * self.scale), 2)
        pygame.draw.line(screen, (150, 150, 150), 
                        (int(self.x - self.radius * 0.5), int(self.y - self.radius * 0.5)),
                        (int(self.x + self.radius * 0.5), int(self.y + self.radius * 0.5)), 2)
        pygame.draw.line(screen, (150, 150, 150), 
                        (int(self.x + self.radius * 0.5), int(self.y - self.radius * 0.5)),
                        (int(self.x - self.radius * 0.5), int(self.y + self.radius * 0.5)), 2)

    def update(self):
        """更新飞行泡泡的位置"""
        if self.is_flying:
            self.x += math.cos(self.angle) * self.speed
            self.y += math.sin(self.angle) * self.speed
            if self.bubble_type == BubbleType.BOMB:
                self.scale += self.pulse_speed * self.scale_direction
                if self.scale >= 1.1 or self.scale <= 0.9:
                    self.scale_direction *= -1

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

    def check_wall_collision(self, left_bound, right_bound, top_bound, bottom_bound):
        """
        检测与墙壁的碰撞
        
        参数:
            left_bound: 左边界
            right_bound: 右边界
            top_bound: 上边界
            bottom_bound: 下边界
        
        返回:
            str: 碰撞方向 'left', 'right', 'top', 'bottom', None
        """
        if self.x - self.radius < left_bound:
            return 'left'
        if self.x + self.radius > right_bound:
            return 'right'
        if self.y - self.radius < top_bound:
            return 'top'
        if self.y + self.radius > bottom_bound:
            return 'bottom'
        return None

    def reflect(self, wall):
        """
        根据碰撞墙壁进行反弹
        
        参数:
            wall: 碰撞方向 'left', 'right', 'top', 'bottom'
        """
        if wall in ['left', 'right']:
            self.angle = math.pi - self.angle
        elif wall in ['top', 'bottom']:
            self.angle = -self.angle

    def can_pierce(self):
        """检查是否可以穿透"""
        return self.bubble_type == BubbleType.PIERCE and not self.has_pierced

    def mark_pierced(self):
        """标记已经穿透"""
        self.has_pierced = True

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

    @classmethod
    def create_bomb_bubble(cls, x, y):
        """创建炸弹泡泡"""
        return cls(x, y, color=(255, 100, 100), bubble_type=BubbleType.BOMB)

    @classmethod
    def create_rainbow_bubble(cls, x, y):
        """创建彩虹泡泡"""
        return cls(x, y, color=(255, 255, 255), bubble_type=BubbleType.RAINBOW)

    @classmethod
    def create_pierce_bubble(cls, x, y):
        """创建穿透泡泡"""
        return cls(x, y, color=(100, 200, 255), bubble_type=BubbleType.PIERCE)

    @classmethod
    def create_obstacle_bubble(cls, x, y):
        """创建障碍物泡泡"""
        return cls(x, y, color=(60, 60, 60), bubble_type=BubbleType.OBSTACLE)