import pygame
import math
from bubble import Bubble

class Cannon:
    """
    炮台类 - 负责发射泡泡的装置
    
    属性:
        x: 炮台中心x坐标
        y: 炮台中心y坐标
        angle: 炮台当前角度（弧度）
        current_bubble: 当前待发射的泡泡
        next_bubble: 下一个待发射的泡泡
        is_ready: 是否准备好发射
    """
    
    def __init__(self, x, y):
        """
        初始化炮台对象
        
        参数:
            x: 炮台中心x坐标
            y: 炮台中心y坐标
        """
        self.x = x
        self.y = y
        self.angle = -math.pi / 2  # 初始角度向上
        self.current_bubble = None
        self.next_bubble = None
        self.is_ready = True
        self._generate_bubbles()
    
    def _generate_bubbles(self):
        """生成当前和下一个泡泡"""
        from bubble import Bubble
        self.current_bubble = Bubble(self.x, self.y - 20)
        self.next_bubble = Bubble(self.x, self.y - 20)
    
    def update_angle(self, mouse_x, mouse_y):
        """
        根据鼠标位置更新炮台角度
        
        参数:
            mouse_x: 鼠标x坐标
            mouse_y: 鼠标y坐标
        """
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        self.angle = math.atan2(dy, dx)
        
        # 限制角度范围在 -pi 到 -0.1 之间（向上发射）
        min_angle = -math.pi + 0.1
        max_angle = -0.1
        if self.angle < min_angle:
            self.angle = min_angle
        elif self.angle > max_angle:
            self.angle = max_angle
    
    def draw(self, screen):
        """
        在屏幕上绘制炮台
        
        参数:
            screen: pygame显示表面
        """
        # 绘制炮台底座
        base_color = (100, 100, 100)
        base_radius = 25
        pygame.draw.circle(screen, base_color, (int(self.x), int(self.y)), base_radius)
        
        # 绘制炮台发射管
        barrel_length = 30
        barrel_width = 8
        barrel_x = self.x + math.cos(self.angle) * barrel_length
        barrel_y = self.y + math.sin(self.angle) * barrel_length
        
        # 绘制发射管矩形
        angle_deg = math.degrees(self.angle)
        barrel_surface = pygame.Surface((barrel_length * 2, barrel_width * 2), pygame.SRCALPHA)
        barrel_surface.fill((0, 0, 0, 0))
        pygame.draw.rect(barrel_surface, (150, 150, 150), 
                        (0, barrel_width // 2, barrel_length, barrel_width))
        
        # 旋转发射管
        rotated_barrel = pygame.transform.rotate(barrel_surface, -angle_deg)
        barrel_rect = rotated_barrel.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_barrel, barrel_rect)
        
        # 绘制当前待发射泡泡
        if self.current_bubble and self.is_ready:
            bubble_offset_x = math.cos(self.angle) * (barrel_length + self.current_bubble.radius)
            bubble_offset_y = math.sin(self.angle) * (barrel_length + self.current_bubble.radius)
            temp_x = self.x + bubble_offset_x
            temp_y = self.y + bubble_offset_y
            
            # 绘制泡泡主体
            pygame.draw.circle(screen, self.current_bubble.color, (int(temp_x), int(temp_y)), self.current_bubble.radius)
            
            # 绘制高光
            highlight_color = (255, 255, 255)
            highlight_radius = self.current_bubble.radius // 3
            highlight_x = temp_x - self.current_bubble.radius // 3
            highlight_y = temp_y - self.current_bubble.radius // 3
            pygame.draw.circle(screen, highlight_color, (int(highlight_x), int(highlight_y)), highlight_radius)
            
            # 绘制边框
            pygame.draw.circle(screen, (0, 0, 0), (int(temp_x), int(temp_y)), self.current_bubble.radius, 1)
    
    def launch_bubble(self):
        """
        发射泡泡
        
        返回:
            Bubble: 发射出去的泡泡
        """
        if not self.is_ready or not self.current_bubble:
            return None
        
        # 创建发射的泡泡
        bubble = Bubble(self.x, self.y)
        bubble.color = self.current_bubble.color
        bubble.set_flying(self.angle)
        
        # 移动泡泡到发射管口位置
        barrel_length = 30
        bubble.x = self.x + math.cos(self.angle) * (barrel_length + bubble.radius)
        bubble.y = self.y + math.sin(self.angle) * (barrel_length + bubble.radius)
        
        # 生成新的泡泡
        self.current_bubble = self.next_bubble
        self.next_bubble = Bubble(self.x, self.y - 20)
        self.is_ready = False
        
        return bubble
    
    def set_ready(self):
        """设置炮台为就绪状态"""
        self.is_ready = True