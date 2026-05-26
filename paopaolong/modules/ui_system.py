import pygame

class UISystem:
    """UI系统 - 管理游戏界面元素"""

    def __init__(self, game):
        """
        初始化UI系统
        
        参数:
            game: 游戏主对象
        """
        self.game = game
        self.hover_button = None

    def draw_icon(self, screen, icon_type, x, y, size=32):
        """
        绘制图标
        
        参数:
            screen: pygame显示表面
            icon_type: 图标类型
            x: x坐标
            y: y坐标
            size: 图标大小
        """
        if icon_type == 'heart':
            self._draw_heart(screen, x, y, size)
        elif icon_type == 'star':
            self._draw_star(screen, x, y, size)
        elif icon_type == 'target':
            self._draw_target(screen, x, y, size)
        elif icon_type == 'bomb':
            self._draw_bomb(screen, x, y, size)
        elif icon_type == 'rainbow':
            self._draw_rainbow(screen, x, y, size)
        elif icon_type == 'arrow':
            self._draw_arrow(screen, x, y, size)
        elif icon_type == 'shield':
            self._draw_shield(screen, x, y, size)

    def _draw_heart(self, screen, x, y, size):
        """绘制心形图标"""
        pygame.draw.polygon(screen, (255, 100, 100), [
            (x, y + size * 0.3),
            (x - size * 0.4, y),
            (x - size * 0.4, y + size * 0.25),
            (x, y + size * 0.5),
            (x + size * 0.4, y + size * 0.25),
            (x + size * 0.4, y),
        ])

    def _draw_star(self, screen, x, y, size):
        """绘制星形图标"""
        points = []
        for i in range(5):
            angle = i * math.pi * 2 / 5 - math.pi / 2
            px = x + math.cos(angle) * size / 2
            py = y + math.sin(angle) * size / 2
            points.append((px, py))
        pygame.draw.polygon(screen, (255, 200, 0), points)

    def _draw_target(self, screen, x, y, size):
        """绘制目标图标"""
        pygame.draw.circle(screen, (255, 100, 0), (x, y), size // 2, 2)
        pygame.draw.circle(screen, (255, 100, 0), (x, y), size // 4, 2)
        pygame.draw.circle(screen, (255, 100, 0), (x, y), 3, 0)

    def _draw_bomb(self, screen, x, y, size):
        """绘制炸弹图标"""
        pygame.draw.circle(screen, (200, 50, 50), (x, y), size // 2)
        pygame.draw.rect(screen, (80, 80, 80), 
                        (x - 3, y - size // 2 - 5, 6, 8))

    def _draw_rainbow(self, screen, x, y, size):
        """绘制彩虹图标"""
        colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0),
                  (0, 255, 0), (0, 0, 255), (75, 0, 130)]
        for i, color in enumerate(colors):
            radius = size // 2 - i * 3
            pygame.draw.arc(screen, color, 
                          (x - radius, y - radius, radius * 2, radius * 2),
                          math.pi, 0, 2)

    def _draw_arrow(self, screen, x, y, size):
        """绘制箭头图标"""
        pygame.draw.line(screen, (100, 200, 255), 
                       (x - size // 2, y), (x + size // 2, y), 3)
        pygame.draw.polygon(screen, (100, 200, 255), [
            (x + size // 2, y),
            (x + size // 4, y - size // 4),
            (x + size // 4, y + size // 4)
        ])

    def _draw_shield(self, screen, x, y, size):
        """绘制盾牌图标"""
        pygame.draw.polygon(screen, (100, 150, 255), [
            (x, y - size // 2),
            (x + size // 2, y - size // 4),
            (x + size // 2, y + size // 3),
            (x, y + size // 2),
            (x - size // 2, y + size // 3),
            (x - size // 2, y - size // 4)
        ])

    def draw_button(self, screen, x, y, width, height, text, 
                   hover=False, disabled=False):
        """
        绘制按钮
        
        参数:
            screen: pygame显示表面
            x: x坐标
            y: y坐标
            width: 宽度
            height: 高度
            text: 按钮文字
            hover: 是否悬停
            disabled: 是否禁用
        """
        if disabled:
            color = (80, 80, 80)
            text_color = (120, 120, 120)
        elif hover:
            color = (80, 120, 180)
            text_color = (255, 255, 255)
        else:
            color = (60, 100, 160)
            text_color = (200, 200, 200)
        
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius=5)
        pygame.draw.rect(screen, (100, 150, 200), (x, y, width, height), 2, border_radius=5)
        
        text_surface = self.game.font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)

    def draw_panel(self, screen, x, y, width, height, title=""):
        """
        绘制面板
        
        参数:
            screen: pygame显示表面
            x: x坐标
            y: y坐标
            width: 宽度
            height: 高度
            title: 面板标题
        """
        pygame.draw.rect(screen, (40, 40, 45), (x, y, width, height), border_radius=8)
        pygame.draw.rect(screen, (70, 70, 80), (x, y, width, height), 2, border_radius=8)
        
        if title:
            title_surface = self.game.font.render(title, True, (200, 200, 200))
            title_rect = title_surface.get_rect(center=(x + width // 2, y + 25))
            screen.blit(title_surface, title_rect)
            pygame.draw.line(screen, (70, 70, 80), (x + 10, y + 45), (x + width - 10, y + 45), 1)

    def draw_centered_text(self, screen, text, y, font_size=36, color=(255, 255, 255)):
        """
        绘制居中文字
        
        参数:
            screen: pygame显示表面
            text: 文字内容
            y: y坐标
            font_size: 字体大小
            color: 文字颜色
        """
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.game.width // 2, y))
        screen.blit(text_surface, text_rect)

    def draw_progress_bar(self, screen, x, y, width, height, current, max_val, color=(0, 255, 0)):
        """
        绘制进度条
        
        参数:
            screen: pygame显示表面
            x: x坐标
            y: y坐标
            width: 宽度
            height: 高度
            current: 当前值
            max_val: 最大值
            color: 进度条颜色
        """
        pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height), border_radius=3)
        
        ratio = min(current / max_val, 1)
        fill_width = int(width * ratio)
        pygame.draw.rect(screen, color, (x, y, fill_width, height), border_radius=3)

    def draw_start_menu(self, screen, mouse_pos):
        """绘制开始菜单"""
        overlay = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        title_surface = self.game.font_large.render('泡泡龙', True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.game.width // 2, 80))
        screen.blit(title_surface, title_rect)

        pygame.draw.rect(screen, (60, 100, 160), 
                        (self.game.width // 2 - 100, 100, 200, 3), border_radius=2)

        button_y = 200
        buttons = [
            ('开始游戏', 1.0),
            ('游戏设置', 0.5),
            ('游戏说明', 0.5),
            ('退出游戏', 0.5)
        ]
        
        for text, scale in buttons:
            button_x = self.game.width // 2 - 100
            button_width = 200
            button_height = 45
            
            hover = (button_x <= mouse_pos[0] <= button_x + button_width and
                     button_y <= mouse_pos[1] <= button_y + button_height)
            
            if hover:
                self.hover_button = text
            
            self.draw_button(screen, button_x, button_y, button_width, button_height, text, hover)
            button_y += 60

    def draw_pause_menu(self, screen, mouse_pos):
        """绘制暂停菜单"""
        overlay = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title_surface = self.game.font_large.render('游戏暂停', True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.game.width // 2, 120))
        screen.blit(title_surface, title_rect)

        button_y = 200
        buttons = [
            ('继续游戏', 1.0),
            ('重新开始', 0.5),
            ('返回主菜单', 0.5)
        ]
        
        for text, scale in buttons:
            button_x = self.game.width // 2 - 100
            button_width = 200
            button_height = 45
            
            hover = (button_x <= mouse_pos[0] <= button_x + button_width and
                     button_y <= mouse_pos[1] <= button_y + button_height)
            
            if hover:
                self.hover_button = text
            
            self.draw_button(screen, button_x, button_y, button_width, button_height, text, hover)
            button_y += 60

    def draw_victory_screen(self, screen, mouse_pos):
        """绘制胜利界面"""
        overlay = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        title_surface = self.game.font_large.render('🎉 关卡胜利!', True, (0, 255, 100))
        title_rect = title_surface.get_rect(center=(self.game.width // 2, 100))
        screen.blit(title_surface, title_rect)

        stats_y = 180
        
        score_text = self.game.font.render(f'本局得分: {self.game.score}', True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.game.width // 2, stats_y))
        screen.blit(score_text, score_rect)
        stats_y += 40

        level_text = self.game.font.render(f'到达关卡: {self.game.level}', True, (255, 255, 255))
        level_rect = level_text.get_rect(center=(self.game.width // 2, stats_y))
        screen.blit(level_text, level_rect)
        stats_y += 40

        time_text = self.game.font.render(f'用时: {self.game.get_elapsed_time()}', True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(self.game.width // 2, stats_y))
        screen.blit(time_text, time_rect)

        button_y = 300
        buttons = [
            ('下一关', 1.0),
            ('重新开始', 0.5),
            ('返回主菜单', 0.5)
        ]
        
        for text, scale in buttons:
            button_x = self.game.width // 2 - 100
            button_width = 200
            button_height = 45
            
            hover = (button_x <= mouse_pos[0] <= button_x + button_width and
                     button_y <= mouse_pos[1] <= button_y + button_height)
            
            if hover:
                self.hover_button = text
            
            self.draw_button(screen, button_x, button_y, button_width, button_height, text, hover)
            button_y += 60

    def draw_gameover_screen(self, screen, mouse_pos):
        """绘制游戏结束界面"""
        overlay = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        title_surface = self.game.font_large.render('游戏结束', True, (255, 50, 50))
        title_rect = title_surface.get_rect(center=(self.game.width // 2, 100))
        screen.blit(title_surface, title_rect)

        stats_y = 180
        
        score_text = self.game.font.render(f'最终得分: {self.game.score}', True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.game.width // 2, stats_y))
        screen.blit(score_text, score_rect)
        stats_y += 40

        level_text = self.game.font.render(f'到达关卡: {self.game.level}', True, (255, 255, 255))
        level_rect = level_text.get_rect(center=(self.game.width // 2, stats_y))
        screen.blit(level_text, level_rect)
        stats_y += 40

        time_text = self.game.font.render(f'用时: {self.game.get_elapsed_time()}', True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(self.game.width // 2, stats_y))
        screen.blit(time_text, time_rect)
        stats_y += 40

        max_combo_text = self.game.font.render(f'最大连击: x{self.game.max_combo}', True, (255, 200, 0))
        max_combo_rect = max_combo_text.get_rect(center=(self.game.width // 2, stats_y))
        screen.blit(max_combo_text, max_combo_rect)

        button_y = 320
        buttons = [
            ('重新开始', 1.0),
            ('返回主菜单', 0.5)
        ]
        
        for text, scale in buttons:
            button_x = self.game.width // 2 - 100
            button_width = 200
            button_height = 45
            
            hover = (button_x <= mouse_pos[0] <= button_x + button_width and
                     button_y <= mouse_pos[1] <= button_y + button_height)
            
            if hover:
                self.hover_button = text
            
            self.draw_button(screen, button_x, button_y, button_width, button_height, text, hover)
            button_y += 60

    def draw_settings_screen(self, screen, mouse_pos):
        """绘制设置界面"""
        overlay = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        title_surface = self.game.font_large.render('游戏设置', True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.game.width // 2, 80))
        screen.blit(title_surface, title_rect)

        back_button_x = self.game.width // 2 - 100
        back_button_y = 400
        hover = (back_button_x <= mouse_pos[0] <= back_button_x + 200 and
                 back_button_y <= mouse_pos[1] <= back_button_y + 45)
        
        if hover:
            self.hover_button = '返回主菜单'
        
        self.draw_button(screen, back_button_x, back_button_y, 200, 45, '返回主菜单', hover)

    def draw_instructions_screen(self, screen, mouse_pos):
        """绘制游戏说明界面"""
        overlay = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        title_surface = self.game.font_large.render('游戏说明', True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.game.width // 2, 60))
        screen.blit(title_surface, title_rect)

        instructions = [
            '操作方式:',
            '  - 鼠标移动控制炮台角度',
            '  - 点击左键发射泡泡',
            '  - 空格键暂停/继续游戏',
            '  - ESC键返回主菜单',
            '',
            '游戏规则:',
            '  - 三个或更多同色泡泡相邻时自动消除',
            '  - 消除相连的悬空泡泡可获得额外分数',
            '  - 泡泡触达底部扣除生命值',
            '  - 生命归零游戏结束',
            '  - 消除所有泡泡通关',
            '',
            '道具说明:',
            '  - 💣 炸弹泡泡: 消除周围一圈泡泡',
            '  - 🌈 彩虹泡泡: 可替代任意颜色',
            '  - ➡️ 穿透泡泡: 可穿过一个异色泡泡',
            '  - ⛏️ 障碍物: 不可消除，增加难度'
        ]

        y = 120
        for line in instructions:
            color = (200, 200, 200)
            if line.startswith('操作方式:') or line.startswith('游戏规则:') or line.startswith('道具说明:'):
                color = (100, 200, 255)
            
            text_surface = self.game.font_small.render(line, True, color)
            text_rect = text_surface.get_rect(center=(self.game.width // 2, y))
            screen.blit(text_surface, text_rect)
            y += 25

        back_button_x = self.game.width // 2 - 100
        back_button_y = y + 40
        hover = (back_button_x <= mouse_pos[0] <= back_button_x + 200 and
                 back_button_y <= mouse_pos[1] <= back_button_y + 45)
        
        if hover:
            self.hover_button = '返回主菜单'
        
        self.draw_button(screen, back_button_x, back_button_y, 200, 45, '返回主菜单', hover)

import math