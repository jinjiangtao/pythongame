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
        self.angle = -math.pi / 2
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
        
        min_angle = -math.pi + 0.1
        max_angle = -0.1
        if self.angle < min_angle:
            self.angle = min_angle
        elif self.angle > max_angle:
            self.angle = max_angle

    def draw(self, screen, game_area_left=0, game_area_right=800, height=600):
        """
        在屏幕上绘制炮台
        
        参数:
            screen: pygame显示表面
            game_area_left: 游戏区域左边界
            game_area_right: 游戏区域右边界
            height: 屏幕高度
        """
        self._draw_aim_line(screen, game_area_left, game_area_right, height)
        
        base_color = (100, 100, 100)
        base_radius = 25
        pygame.draw.circle(screen, base_color, (int(self.x), int(self.y)), base_radius)
        pygame.draw.circle(screen, (80, 80, 80), (int(self.x), int(self.y)), base_radius, 2)
        
        barrel_length = 30
        barrel_width = 8
        barrel_x = self.x + math.cos(self.angle) * barrel_length
        barrel_y = self.y + math.sin(self.angle) * barrel_length
        
        angle_deg = math.degrees(self.angle)
        barrel_surface = pygame.Surface((barrel_length * 2, barrel_width * 2), pygame.SRCALPHA)
        barrel_surface.fill((0, 0, 0, 0))
        pygame.draw.rect(barrel_surface, (150, 150, 150), 
                        (0, barrel_width // 2, barrel_length, barrel_width))
        
        rotated_barrel = pygame.transform.rotate(barrel_surface, -angle_deg)
        barrel_rect = rotated_barrel.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_barrel, barrel_rect)
        
        if self.current_bubble and self.is_ready:
            bubble_offset_x = math.cos(self.angle) * (barrel_length + self.current_bubble.radius)
            bubble_offset_y = math.sin(self.angle) * (barrel_length + self.current_bubble.radius)
            temp_x = self.x + bubble_offset_x
            temp_y = self.y + bubble_offset_y
            
            pygame.draw.circle(screen, self.current_bubble.color, (int(temp_x), int(temp_y)), self.current_bubble.radius)
            
            highlight_color = (255, 255, 255)
            highlight_radius = self.current_bubble.radius // 3
            highlight_x = temp_x - self.current_bubble.radius // 3
            highlight_y = temp_y - self.current_bubble.radius // 3
            pygame.draw.circle(screen, highlight_color, (int(highlight_x), int(highlight_y)), highlight_radius)
            
            pygame.draw.circle(screen, (0, 0, 0), (int(temp_x), int(temp_y)), self.current_bubble.radius, 1)

    def _draw_aim_line(self, screen, game_area_left, game_area_right, height):
        """
        绘制辅助瞄准线
        
        参数:
            screen: pygame显示表面
            game_area_left: 游戏区域左边界
            game_area_right: 游戏区域右边界
            height: 屏幕高度
        """
        if not self.is_ready:
            return
        
        aim_points = []
        current_x = self.x + math.cos(self.angle) * 35
        current_y = self.y + math.sin(self.angle) * 35
        current_angle = self.angle
        
        max_bounces = 10
        bounce_count = 0
        
        while bounce_count < max_bounces:
            aim_points.append((current_x, current_y))
            
            t_left = (game_area_left + 15 - current_x) / math.cos(current_angle) if math.cos(current_angle) != 0 else float('inf')
            t_right = (game_area_right - 15 - current_x) / math.cos(current_angle) if math.cos(current_angle) != 0 else float('inf')
            t_top = (15 - current_y) / math.sin(current_angle) if math.sin(current_angle) != 0 else float('inf')
            
            t_min = float('inf')
            wall = None
            
            if t_left > 0 and t_left < t_min:
                t_min = t_left
                wall = 'left'
            if t_right > 0 and t_right < t_min:
                t_min = t_right
                wall = 'right'
            if t_top > 0 and t_top < t_min:
                t_min = t_top
                wall = 'top'
            
            if t_min == float('inf') or t_min > 1000:
                end_x = current_x + math.cos(current_angle) * 1000
                end_y = current_y + math.sin(current_angle) * 1000
                aim_points.append((end_x, end_y))
                break
            
            current_x += math.cos(current_angle) * t_min
            current_y += math.sin(current_angle) * t_min
            
            if wall in ['left', 'right']:
                current_angle = math.pi - current_angle
            elif wall == 'top':
                current_angle = -current_angle
            
            bounce_count += 1
        
        if len(aim_points) >= 2:
            for i in range(len(aim_points) - 1):
                alpha = 255 - i * 20
                if alpha < 50:
                    alpha = 50
                pygame.draw.line(screen, (200, 200, 200, alpha), 
                               (int(aim_points[i][0]), int(aim_points[i][1])),
                               (int(aim_points[i+1][0]), int(aim_points[i+1][1])), 2)

    def launch_bubble(self, game_area_left=0, game_area_right=800, height=600):
        """
        发射泡泡
        
        参数:
            game_area_left: 游戏区域左边界
            game_area_right: 游戏区域右边界
            height: 游戏区域高度
        
        返回:
            Bubble: 发射出去的泡泡
        """
        if not self.is_ready or not self.current_bubble:
            return None
        
        bubble = Bubble(self.x, self.y)
        bubble.color = self.current_bubble.color
        bubble.bubble_type = self.current_bubble.bubble_type
        bubble.set_flying(self.angle)
        
        barrel_length = 40
        bubble.x = self.x + math.cos(self.angle) * (barrel_length + bubble.radius)
        bubble.y = self.y + math.sin(self.angle) * (barrel_length + bubble.radius)
        
        bubble.x = max(game_area_left + bubble.radius + 5, min(bubble.x, game_area_right - bubble.radius - 5))
        bubble.y = max(bubble.radius + 5, min(bubble.y, height - 100))
        
        self.current_bubble = self.next_bubble
        self.next_bubble = Bubble(self.x, self.y - 20)
        self.is_ready = False
        
        return bubble

    def set_ready(self):
        """设置炮台为就绪状态"""
        self.is_ready = True

    def set_bubble_type(self, bubble_type):
        """
        设置当前泡泡类型
        
        参数:
            bubble_type: 泡泡类型
        """
        if self.current_bubble:
            self.current_bubble.bubble_type = bubble_type