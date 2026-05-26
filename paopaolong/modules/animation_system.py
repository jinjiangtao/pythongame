import pygame
import math

class AnimationType:
    """动画类型枚举"""
    POP = 'pop'
    DROP = 'drop'
    LAUNCH = 'launch'
    COMBO = 'combo'
    DAMAGE = 'damage'

class Animation:
    """单个动画对象"""
    
    def __init__(self, anim_type, x, y, duration=300, **kwargs):
        """
        初始化动画对象
        
        参数:
            anim_type: 动画类型
            x: 起始x坐标
            y: 起始y坐标
            duration: 动画持续时间（毫秒）
            kwargs: 其他参数
        """
        self.type = anim_type
        self.x = x
        self.y = y
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        self.kwargs = kwargs
        self.is_complete = False
        self.scale = 1.0
        self.alpha = 255

    def update(self):
        """更新动画状态"""
        elapsed = pygame.time.get_ticks() - self.start_time
        progress = elapsed / self.duration
        
        if progress >= 1.0:
            self.is_complete = True
            return
        
        if self.type == AnimationType.POP:
            self.scale = 1 + progress * 2
            self.alpha = 255 - int(progress * 255)
        elif self.type == AnimationType.DROP:
            self.y += progress * 10
            self.alpha = 255 - int(progress * 255)
        elif self.type == AnimationType.COMBO:
            self.scale = 1 + math.sin(progress * math.pi * 4) * 0.3
            self.alpha = 255 - int(progress * 150)
        elif self.type == AnimationType.DAMAGE:
            self.scale = 1 + math.sin(progress * math.pi * 6) * 0.2

    def draw(self, screen):
        """绘制动画"""
        if self.is_complete:
            return
        
        if self.type == AnimationType.POP:
            self._draw_pop(screen)
        elif self.type == AnimationType.DROP:
            self._draw_drop(screen)
        elif self.type == AnimationType.COMBO:
            self._draw_combo(screen)
        elif self.type == AnimationType.DAMAGE:
            self._draw_damage(screen)

    def _draw_pop(self, screen):
        """绘制消除动画"""
        color = self.kwargs.get('color', (255, 255, 255))
        for i in range(6):
            angle = i * math.pi * 2 / 6
            dist = self.scale * 15
            px = self.x + math.cos(angle) * dist
            py = self.y + math.sin(angle) * dist
            pygame.draw.circle(screen, color, (int(px), int(py)), int(5 * (1 - self.scale / 3)), 0)

    def _draw_drop(self, screen):
        """绘制掉落动画"""
        color = self.kwargs.get('color', (100, 100, 100))
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(10 * self.scale), 0)

    def _draw_combo(self, screen):
        """绘制连击动画"""
        combo = self.kwargs.get('combo', 2)
        text = f'x{combo}'
        font = pygame.font.Font(None, 48)
        text_surface = font.render(text, True, (255, 200, 0))
        text_surface.set_alpha(self.alpha)
        
        scaled_surface = pygame.transform.scale(text_surface, 
            (int(text_surface.get_width() * self.scale), 
             int(text_surface.get_height() * self.scale)))
        
        rect = scaled_surface.get_rect(center=(self.x, self.y))
        screen.blit(scaled_surface, rect)

    def _draw_damage(self, screen):
        """绘制伤害动画"""
        text = self.kwargs.get('text', '-1')
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (255, 0, 0))
        text_surface.set_alpha(self.alpha)
        
        scaled_surface = pygame.transform.scale(text_surface, 
            (int(text_surface.get_width() * self.scale), 
             int(text_surface.get_height() * self.scale)))
        
        rect = scaled_surface.get_rect(center=(self.x, self.y))
        screen.blit(scaled_surface, rect)

class AnimationSystem:
    """动画系统 - 管理所有游戏动画"""

    def __init__(self):
        """初始化动画系统"""
        self.animations = []

    def add_animation(self, anim_type, x, y, **kwargs):
        """
        添加动画
        
        参数:
            anim_type: 动画类型
            x: x坐标
            y: y坐标
            kwargs: 其他参数
        """
        anim = Animation(anim_type, x, y, **kwargs)
        self.animations.append(anim)

    def add_pop_animation(self, x, y, color):
        """添加消除动画"""
        self.add_animation(AnimationType.POP, x, y, color=color)

    def add_drop_animation(self, x, y, color):
        """添加掉落动画"""
        self.add_animation(AnimationType.DROP, x, y, color=color)

    def add_combo_animation(self, x, y, combo_count):
        """添加连击动画"""
        self.add_animation(AnimationType.COMBO, x, y, combo=combo_count)

    def add_damage_animation(self, x, y, text):
        """添加伤害动画"""
        self.add_animation(AnimationType.DAMAGE, x, y, text=text)

    def update(self):
        """更新所有动画"""
        for anim in self.animations[:]:
            anim.update()
            if anim.is_complete:
                self.animations.remove(anim)

    def draw(self, screen):
        """绘制所有动画"""
        for anim in self.animations:
            anim.draw(screen)

    def clear(self):
        """清除所有动画"""
        self.animations = []