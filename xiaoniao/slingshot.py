# slingshot.py - 弹弓类

import math
import pygame
from settings import SLINGSHOT_X, SLINGSHOT_Y, MAX_DRAG_DISTANCE, FORCE_MULTIPLIER

class Slingshot:
    def __init__(self):
        self.x = SLINGSHOT_X
        self.y = SLINGSHOT_Y
        self.top_x = SLINGSHOT_X
        self.top_y = SLINGSHOT_Y - 30
        self.is_dragging = False
        self.drag_start = (0, 0)
        self.drag_end = (0, 0)
    
    def handle_event(self, event, bird, game_state):
        """处理鼠标事件"""
        if game_state.is_game_over():
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.is_near_bird(mouse_x, mouse_y, bird) and not bird.is_flying:
                self.is_dragging = True
                self.drag_start = (mouse_x, mouse_y)
                self.drag_end = (mouse_x, mouse_y)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_dragging:
                self.is_dragging = False
                if not bird.is_flying and game_state.birds_left > 0:
                    self.launch_bird(bird, game_state)
        
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - self.top_x
                dy = mouse_y - self.top_y
                distance = math.sqrt(dx * dx + dy * dy)
                
                if distance > MAX_DRAG_DISTANCE:
                    ratio = MAX_DRAG_DISTANCE / distance
                    mouse_x = self.top_x + dx * ratio
                    mouse_y = self.top_y + dy * ratio
                
                self.drag_end = (mouse_x, mouse_y)
    
    def is_near_bird(self, x, y, bird):
        """检测鼠标是否在小鸟附近"""
        distance = math.sqrt((x - bird.x)**2 + (y - bird.y)**2)
        return distance < 100
    
    def launch_bird(self, bird, game_state):
        """发射小鸟"""
        dx = self.top_x - self.drag_end[0]
        dy = self.top_y - self.drag_end[1]
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > 0:
            force = distance * (FORCE_MULTIPLIER / MAX_DRAG_DISTANCE) * 40
            force_x = (dx / distance) * force
            force_y = (dy / distance) * force
            bird.launch(force_x, force_y)
            game_state.birds_left -= 1
    
    def get_bird_position(self):
        """获取小鸟当前应该显示的位置"""
        if self.is_dragging:
            return self.drag_end
        return (self.x, self.y - 30)
    
    def draw(self, screen):
        """绘制弹弓"""
        pygame.draw.rect(screen, (139, 90, 43), (self.x - 8, self.y, 16, 100))
        
        pygame.draw.line(screen, (100, 100, 100), 
                        (self.x - 20, self.y), 
                        (self.x, self.y - 30), 4)
        pygame.draw.line(screen, (100, 100, 100), 
                        (self.x + 20, self.y), 
                        (self.x, self.y - 30), 4)
        
        pygame.draw.circle(screen, (50, 50, 50), (self.x, self.y - 30), 8)
        
        if self.is_dragging:
            pygame.draw.lines(screen, (255, 0, 0), False, 
                            [(self.x, self.y - 30), self.drag_end], 2)
            
            for i in range(1, 10):
                px = self.x + (self.drag_end[0] - self.x) * i / 10
                py = self.y - 30 + (self.drag_end[1] - (self.y - 30)) * i / 10
                pygame.draw.circle(screen, (255, 0, 0), (int(px), int(py)), 3)