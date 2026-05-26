import pygame
import math
from bubble import Bubble, BubbleType
from cannon import Cannon
from modules.powerup_system import PowerupSystem
from modules.animation_system import AnimationSystem
from modules.ui_system import UISystem
from modules.life_system import LifeSystem

class Game:
    """
    游戏主逻辑类 - 控制整个游戏的流程和状态
    
    属性:
        screen: pygame显示表面
        width: 游戏窗口宽度
        height: 游戏窗口高度
        cannon: 炮台对象
        bubbles: 已放置的泡泡列表
        flying_bubble: 当前飞行中的泡泡
        score: 当前得分
        level: 当前关卡
        game_state: 游戏状态 ('start', 'playing', 'paused', 'win', 'gameover', 'settings', 'instructions')
        grid: 六边形网格系统
        drop_speed: 泡泡下移速度
        drop_timer: 下移计时器
        left_panel_width: 左侧面板宽度
        right_panel_width: 右侧面板宽度
        powerup_system: 道具系统
        animation_system: 动画系统
        ui_system: UI系统
        life_system: 生命系统
        combo_count: 当前连击数
        max_combo: 最大连击数
        combo_timer: 连击计时器
        game_start_time: 游戏开始时间
        show_settings: 是否显示设置界面
        show_instructions: 是否显示说明界面
    """

    def __init__(self, width=800, height=600):
        """
        初始化游戏对象
        
        参数:
            width: 游戏窗口宽度
            height: 游戏窗口高度
        """
        pygame.init()
        pygame.font.init()
        
        import os
        font_path = None
        
        system_font_paths = [
            'C:/Windows/Fonts/simhei.ttf',
            'C:/Windows/Fonts/simsun.ttc',
            'C:/Windows/Fonts/msyh.ttc',
            'C:/Windows/Fonts/kaiti.ttf',
            'C:/Windows/Fonts/STHeiti Light.ttc',
        ]
        
        for path in system_font_paths:
            if os.path.exists(path):
                font_path = path
                break
        
        if font_path:
            try:
                self.font = pygame.font.Font(font_path, 20)
                self.font_large = pygame.font.Font(font_path, 36)
                self.font_small = pygame.font.Font(font_path, 16)
            except:
                self.font = pygame.font.Font(None, 20)
                self.font_large = pygame.font.Font(None, 36)
                self.font_small = pygame.font.Font(None, 16)
        else:
            chinese_fonts = ['SimHei', 'SimSun', 'Microsoft YaHei', 'KaiTi']
            font_found = False
            for font_name in chinese_fonts:
                try:
                    self.font = pygame.font.SysFont(font_name, 20)
                    self.font_large = pygame.font.SysFont(font_name, 36)
                    self.font_small = pygame.font.SysFont(font_name, 16)
                    font_found = True
                    break
                except:
                    continue
            
            if not font_found:
                self.font = pygame.font.Font(None, 20)
                self.font_large = pygame.font.Font(None, 36)
                self.font_small = pygame.font.Font(None, 16)
        
        self.width = width
        self.height = height
        self.left_panel_width = 150
        self.right_panel_width = 150
        
        self.game_area_left = self.left_panel_width
        self.game_area_right = self.width - self.right_panel_width
        self.game_area_width = self.game_area_right - self.game_area_left
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('泡泡龙')
        
        self.cannon = Cannon(self.width // 2, self.height - 50)
        self.bubbles = []
        self.flying_bubble = None
        self.score = 0
        self.level = 1
        self.game_state = 'start'
        
        self.drop_speed = 0.5
        self.drop_timer = 0
        self.drop_interval = 3000
        
        self.grid_cell_size = 30
        self.grid_cols = 12
        self.grid_rows = 10
        
        self.bg_color = (30, 30, 30)
        self.panel_color = (40, 40, 45)
        self.text_color = (255, 255, 255)
        self.border_color = (70, 70, 80)
        
        self.powerup_system = PowerupSystem(self)
        self.animation_system = AnimationSystem()
        self.ui_system = UISystem(self)
        self.life_system = LifeSystem(self, max_lives=3)
        
        self.combo_count = 0
        self.max_combo = 0
        self.combo_timer = 0
        self.max_combo_timer = 2000
        
        self.game_start_time = 0
        self.show_settings = False
        self.show_instructions = False
        
        self.mouse_pos = (0, 0)

    def reset_game(self):
        """重置游戏状态"""
        self.bubbles = []
        self.flying_bubble = None
        self.score = 0
        self.level = 1
        self.game_state = 'playing'
        self.drop_speed = 0.5
        self.cannon = Cannon(self.width // 2, self.height - 50)
        self.life_system.reset_lives()
        self.combo_count = 0
        self.max_combo = 0
        self.game_start_time = pygame.time.get_ticks()
        self.animation_system.clear()
        self.create_initial_bubbles()

    def next_level(self):
        """进入下一关"""
        self.level += 1
        self.drop_speed = 0.5 + (self.level - 1) * 0.15
        self.drop_interval = max(1000, 3000 - (self.level - 1) * 200)
        self.bubbles = []
        self.flying_bubble = None
        self.cannon = Cannon(self.width // 2, self.height - 50)
        self.create_initial_bubbles()

    def create_initial_bubbles(self):
        """创建初始泡泡阵列"""
        rows_to_create = min(4 + self.level, 7)
        
        for row in range(rows_to_create):
            for col in range(self.grid_cols):
                offset_x = 0
                if row % 2 == 1:
                    offset_x = self.grid_cell_size / 2
                
                x = self.game_area_left + self.grid_cell_size / 2 + col * self.grid_cell_size + offset_x
                y = 50 + row * (self.grid_cell_size * math.sqrt(3) / 2)
                
                if pygame.time.get_ticks() % (row + col + 2) != 0:
                    if self.level >= 5 and pygame.time.get_ticks() % 15 == 0:
                        bubble = Bubble.create_obstacle_bubble(x, y)
                    else:
                        bubble = self.powerup_system.get_random_powerup_bubble(x, y)
                    bubble.grid_pos = (row, col)
                    self.bubbles.append(bubble)

    def update(self):
        """更新游戏状态"""
        if self.game_state == 'playing':
            self.life_system.update()
            self._update_combo_timer()
            self._update_flying_bubble()
            self._update_drop_timer()
            self._check_game_over()
            self._check_level_complete()
        
        self.animation_system.update()

    def _update_combo_timer(self):
        """更新连击计时器"""
        if self.combo_count > 0:
            self.combo_timer += 16
            if self.combo_timer >= self.max_combo_timer:
                self.combo_count = 0
                self.combo_timer = 0

    def _update_flying_bubble(self):
        """更新飞行泡泡的状态"""
        if self.flying_bubble:
            bottom_bound = self.height - 80
            
            self.flying_bubble.update()
            
            max_reflections = 3
            reflection_count = 0
            
            while reflection_count < max_reflections:
                wall = self.flying_bubble.check_wall_collision(self.game_area_left, self.game_area_right, 0, bottom_bound)
                if not wall:
                    break
                
                if wall == 'bottom':
                    self.flying_bubble = None
                    self.cannon.set_ready()
                    self.life_system.lose_life()
                    self.animation_system.add_damage_animation(self.width // 2, self.height // 2, '-1生命')
                    return
                
                self.flying_bubble.reflect(wall)
                
                if wall == 'left':
                    self.flying_bubble.x = self.game_area_left + self.flying_bubble.radius + 3
                elif wall == 'right':
                    self.flying_bubble.x = self.game_area_right - self.flying_bubble.radius - 3
                elif wall == 'top':
                    self.flying_bubble.y = self.flying_bubble.radius + 3
                
                reflection_count += 1
            
            for bubble in self.bubbles:
                if self.flying_bubble.check_collision(bubble):
                    if self.powerup_system.should_ignore_collision(self.flying_bubble, bubble):
                        self.flying_bubble.mark_pierced()
                        continue
                    self._place_bubble()
                    return
            
            if self.flying_bubble.y > self.height:
                self.flying_bubble = None
                self.cannon.set_ready()
                self.life_system.lose_life()
                self.animation_system.add_damage_animation(self.width // 2, self.height // 2, '-1生命')

    def _place_bubble(self):
        """放置泡泡并检测消除"""
        flying_bubble = self.flying_bubble
        
        if flying_bubble.bubble_type == BubbleType.RAINBOW:
            target_color = self.powerup_system.activate_rainbow_bubble(flying_bubble)
            flying_bubble.color = target_color
            flying_bubble.bubble_type = BubbleType.NORMAL
        
        flying_bubble.stop_flying()
        self.bubbles.append(flying_bubble)
        self.flying_bubble = None
        self.cannon.set_ready()
        
        self._check_and_clear_matches()

    def _check_and_clear_matches(self):
        """检测并消除匹配的泡泡"""
        if not self.bubbles:
            return
        
        last_bubble = self.bubbles[-1]
        
        if last_bubble.bubble_type == BubbleType.BOMB:
            affected = self.powerup_system.activate_bomb_bubble(last_bubble)
            for bubble in affected:
                self.animation_system.add_pop_animation(bubble.x, bubble.y, bubble.color)
                self.bubbles.remove(bubble)
                self.score += 15 * (self.combo_count + 1)
            
            if self.bubbles and last_bubble in self.bubbles:
                self.bubbles.remove(last_bubble)
            self._increment_combo(len(affected))
            self._check_hanging_bubbles()
            return
        
        matched = self._find_connected_bubbles(last_bubble)
        
        if len(matched) >= 3:
            for bubble in matched:
                if bubble in self.bubbles:
                    self.animation_system.add_pop_animation(bubble.x, bubble.y, bubble.color)
                    self.bubbles.remove(bubble)
                    self.score += 10 * (self.combo_count + 1)
            
            self._increment_combo(len(matched))
            self._check_hanging_bubbles()

    def _increment_combo(self, count):
        """增加连击数"""
        if count > 0:
            self.combo_count += 1
            self.combo_timer = 0
            if self.combo_count > self.max_combo:
                self.max_combo = self.combo_count
            
            if self.combo_count >= 2:
                self.animation_system.add_combo_animation(self.width // 2, self.height // 2, self.combo_count)

    def _find_connected_bubbles(self, start_bubble):
        """查找相连的同色泡泡"""
        if start_bubble.bubble_type == BubbleType.OBSTACLE:
            return []
        
        matched = []
        visited = set()
        stack = [start_bubble]
        
        while stack:
            bubble = stack.pop()
            if bubble in visited:
                continue
            visited.add(bubble)
            
            if bubble.bubble_type == BubbleType.OBSTACLE:
                continue
            
            if bubble.color == start_bubble.color:
                matched.append(bubble)
                
                for other in self.bubbles:
                    if other not in visited and bubble.check_collision(other):
                        stack.append(other)
        
        return matched

    def _check_hanging_bubbles(self):
        """检测并移除悬空的泡泡"""
        if not self.bubbles:
            return
        
        connected_to_top = set()
        stack = []
        
        for bubble in self.bubbles:
            if bubble.bubble_type == BubbleType.OBSTACLE:
                stack.append(bubble)
                connected_to_top.add(bubble)
            elif bubble.y <= bubble.radius + 20:
                stack.append(bubble)
                connected_to_top.add(bubble)
        
        while stack:
            bubble = stack.pop()
            for other in self.bubbles:
                if other not in connected_to_top and bubble.check_collision(other):
                    connected_to_top.add(other)
                    stack.append(other)
        
        hanging_bubbles = []
        for bubble in self.bubbles:
            if bubble not in connected_to_top and bubble.bubble_type != BubbleType.OBSTACLE:
                hanging_bubbles.append(bubble)
        
        for bubble in hanging_bubbles:
            self.animation_system.add_drop_animation(bubble.x, bubble.y, bubble.color)
            self.bubbles.remove(bubble)
            self.score += 20 * (self.combo_count + 1)

    def _update_drop_timer(self):
        """更新泡泡下移计时器"""
        self.drop_timer += 16
        
        if self.drop_timer >= self.drop_interval:
            self.drop_timer = 0
            self._drop_all_bubbles()

    def _drop_all_bubbles(self):
        """将所有泡泡下移"""
        for bubble in self.bubbles:
            bubble.y += self.drop_speed

    def _check_game_over(self):
        """检查游戏是否结束"""
        if self.life_system.is_game_over():
            self.game_state = 'gameover'
            return
        
        for bubble in self.bubbles:
            if bubble.y + bubble.radius > self.height - 80:
                self.life_system.lose_life()
                self.animation_system.add_damage_animation(self.width // 2, self.height // 2, '-1生命')
                if self.life_system.is_game_over():
                    self.game_state = 'gameover'
                else:
                    self._drop_all_bubbles_to_bottom()
                return

    def _drop_all_bubbles_to_bottom(self):
        """将泡泡下移一行，给玩家更多空间"""
        for bubble in self.bubbles:
            bubble.y -= self.grid_cell_size * math.sqrt(3) / 2
        
        self.bubbles = [b for b in self.bubbles if b.y > -b.radius]

    def _check_level_complete(self):
        """检查是否通关"""
        normal_bubbles = [b for b in self.bubbles if b.bubble_type != BubbleType.OBSTACLE]
        if not normal_bubbles and self.game_state == 'playing':
            self.game_state = 'win'

    def draw(self):
        """绘制游戏界面"""
        self.screen.fill(self.bg_color)
        
        self._draw_left_panel()
        self._draw_right_panel()
        
        pygame.draw.rect(self.screen, self.border_color, 
                        (self.game_area_left, 0, self.game_area_width, self.height), 2)
        
        for bubble in self.bubbles:
            bubble.draw(self.screen)
        
        if self.flying_bubble:
            self.flying_bubble.draw(self.screen)
        
        if self.game_state == 'playing':
            self.cannon.draw(self.screen, self.game_area_left, self.game_area_right, self.height)
            self.life_system.draw(self.screen)
        
        self.animation_system.draw(self.screen)
        
        if self.game_state == 'start':
            self.ui_system.draw_start_menu(self.screen, self.mouse_pos)
        elif self.game_state == 'paused':
            self.ui_system.draw_pause_menu(self.screen, self.mouse_pos)
        elif self.game_state == 'win':
            self.ui_system.draw_victory_screen(self.screen, self.mouse_pos)
        elif self.game_state == 'gameover':
            self.ui_system.draw_gameover_screen(self.screen, self.mouse_pos)
        elif self.game_state == 'settings':
            self.ui_system.draw_settings_screen(self.screen, self.mouse_pos)
        elif self.game_state == 'instructions':
            self.ui_system.draw_instructions_screen(self.screen, self.mouse_pos)
        
        pygame.display.flip()

    def _draw_left_panel(self):
        """绘制左侧信息面板"""
        pygame.draw.rect(self.screen, self.panel_color, (0, 0, self.left_panel_width, self.height), border_radius=8)
        pygame.draw.rect(self.screen, self.border_color, (0, 0, self.left_panel_width, self.height), 2, border_radius=8)
        
        pygame.draw.circle(self.screen, (255, 200, 0), (self.left_panel_width // 2, 40), 20)
        pygame.draw.polygon(self.screen, (255, 255, 255), [
            (self.left_panel_width // 2, 25),
            (self.left_panel_width // 2 + 6, 35),
            (self.left_panel_width // 2 - 6, 35)
        ])
        
        pygame.draw.line(self.screen, self.border_color, (10, 80), (self.left_panel_width - 10, 80), 2)
        
        score_text = self.font.render(f'得分', True, (200, 200, 200))
        score_rect = score_text.get_rect(center=(self.left_panel_width // 2, 110))
        self.screen.blit(score_text, score_rect)
        
        score_value = self.font_large.render(f'{self.score}', True, (255, 255, 255))
        score_value_rect = score_value.get_rect(center=(self.left_panel_width // 2, 145))
        self.screen.blit(score_value, score_value_rect)
        
        pygame.draw.line(self.screen, self.border_color, (20, 170), (self.left_panel_width - 20, 170), 1)
        
        level_text = self.font.render(f'关卡', True, (200, 200, 200))
        level_rect = level_text.get_rect(center=(self.left_panel_width // 2, 200))
        self.screen.blit(level_text, level_rect)
        
        level_value = self.font_large.render(f'{self.level}', True, (100, 200, 255))
        level_value_rect = level_value.get_rect(center=(self.left_panel_width // 2, 235))
        self.screen.blit(level_value, level_value_rect)
        
        pygame.draw.line(self.screen, self.border_color, (20, 260), (self.left_panel_width - 20, 260), 1)
        
        combo_text = self.font.render(f'连击', True, (200, 200, 200))
        combo_rect = combo_text.get_rect(center=(self.left_panel_width // 2, 290))
        self.screen.blit(combo_text, combo_rect)
        
        if self.combo_count > 0:
            combo_value = self.font_large.render(f'x{self.combo_count}', True, (255, 200, 0))
        else:
            combo_value = self.font_large.render(f'-', True, (100, 100, 100))
        combo_value_rect = combo_value.get_rect(center=(self.left_panel_width // 2, 325))
        self.screen.blit(combo_value, combo_value_rect)
        
        pygame.draw.line(self.screen, self.border_color, (20, 350), (self.left_panel_width - 20, 350), 1)
        
        max_combo_text = self.font.render(f'最大连击', True, (200, 200, 200))
        max_combo_rect = max_combo_text.get_rect(center=(self.left_panel_width // 2, 380))
        self.screen.blit(max_combo_text, max_combo_rect)
        
        max_combo_value = self.font.render(f'x{self.max_combo}', True, (255, 150, 0))
        max_combo_value_rect = max_combo_value.get_rect(center=(self.left_panel_width // 2, 405))
        self.screen.blit(max_combo_value, max_combo_value_rect)
        
        pygame.draw.line(self.screen, self.border_color, (20, 430), (self.left_panel_width - 20, 430), 1)
        
        time_text = self.font.render(f'用时', True, (200, 200, 200))
        time_rect = time_text.get_rect(center=(self.left_panel_width // 2, 460))
        self.screen.blit(time_text, time_rect)
        
        time_value = self.font.render(f'{self.get_elapsed_time()}', True, (150, 200, 150))
        time_value_rect = time_value.get_rect(center=(self.left_panel_width // 2, 485))
        self.screen.blit(time_value, time_value_rect)

    def _draw_right_panel(self):
        """绘制右侧预览面板"""
        pygame.draw.rect(self.screen, self.panel_color, 
                        (self.game_area_right, 0, self.right_panel_width, self.height), border_radius=8)
        pygame.draw.rect(self.screen, self.border_color, 
                        (self.game_area_right, 0, self.right_panel_width, self.height), 2, border_radius=8)
        
        title_text = self.font.render('泡泡预览', True, (200, 200, 200))
        title_rect = title_text.get_rect(center=(self.game_area_right + self.right_panel_width // 2, 40))
        self.screen.blit(title_text, title_rect)
        
        pygame.draw.line(self.screen, self.border_color, 
                        (self.game_area_right + 10, 70), 
                        (self.width - 10, 70), 2)
        
        current_label = self.font_small.render('当前', True, (200, 200, 200))
        current_label_rect = current_label.get_rect(center=(self.game_area_right + self.right_panel_width // 2, 100))
        self.screen.blit(current_label, current_label_rect)
        
        if self.cannon.current_bubble:
            current_bubble_x = self.game_area_right + self.right_panel_width // 2
            current_bubble_y = 140
            
            if self.cannon.current_bubble.bubble_type == BubbleType.BOMB:
                pygame.draw.circle(self.screen, (255, 100, 100), (current_bubble_x, current_bubble_y), 20)
                pygame.draw.circle(self.screen, (0, 0, 0), (current_bubble_x, current_bubble_y), 20, 2)
                pygame.draw.circle(self.screen, (255, 255, 0), (current_bubble_x, current_bubble_y), 10)
                pygame.draw.polygon(self.screen, (0, 0, 0), [
                    (current_bubble_x, current_bubble_y - 3),
                    (current_bubble_x + 2, current_bubble_y),
                    (current_bubble_x, current_bubble_y + 3),
                    (current_bubble_x - 2, current_bubble_y)
                ])
            elif self.cannon.current_bubble.bubble_type == BubbleType.RAINBOW:
                rainbow_colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130)]
                for i, color in enumerate(rainbow_colors):
                    radius = 20 - i * 3
                    pygame.draw.arc(self.screen, color, 
                                  (current_bubble_x - radius, current_bubble_y - radius, radius * 2, radius * 2),
                                  math.pi, 0, 2)
                pygame.draw.circle(self.screen, (255, 255, 255), (current_bubble_x, current_bubble_y), 20, 2)
            elif self.cannon.current_bubble.bubble_type == BubbleType.PIERCE:
                pygame.draw.circle(self.screen, (100, 200, 255), (current_bubble_x, current_bubble_y), 20)
                pygame.draw.circle(self.screen, (0, 0, 255), (current_bubble_x, current_bubble_y), 20, 2)
                for i in range(4):
                    angle = i * math.pi / 2
                    arrow_x = current_bubble_x + math.cos(angle) * 12
                    arrow_y = current_bubble_y + math.sin(angle) * 12
                    pygame.draw.polygon(self.screen, (255, 255, 255), [
                        (arrow_x, arrow_y),
                        (arrow_x + math.cos(angle) * 3, arrow_y + math.sin(angle) * 3),
                        (arrow_x + math.cos(angle + 0.3) * 2, arrow_y + math.sin(angle + 0.3) * 2),
                        (arrow_x + math.cos(angle - 0.3) * 2, arrow_y + math.sin(angle - 0.3) * 2)
                    ])
            else:
                pygame.draw.circle(self.screen, self.cannon.current_bubble.color, (current_bubble_x, current_bubble_y), 20)
                pygame.draw.circle(self.screen, (255, 255, 255), (current_bubble_x - 6, current_bubble_y - 6), 6)
                pygame.draw.circle(self.screen, (0, 0, 0), (current_bubble_x, current_bubble_y), 20, 1)
        
        next_label = self.font_small.render('下一个', True, (200, 200, 200))
        next_label_rect = next_label.get_rect(center=(self.game_area_right + self.right_panel_width // 2, 180))
        self.screen.blit(next_label, next_label_rect)
        
        if self.cannon.next_bubble:
            next_bubble_x = self.game_area_right + self.right_panel_width // 2
            next_bubble_y = 220
            
            if self.cannon.next_bubble.bubble_type == BubbleType.BOMB:
                pygame.draw.circle(self.screen, (255, 100, 100), (next_bubble_x, next_bubble_y), 20)
                pygame.draw.circle(self.screen, (0, 0, 0), (next_bubble_x, next_bubble_y), 20, 2)
                pygame.draw.circle(self.screen, (255, 255, 0), (next_bubble_x, next_bubble_y), 10)
            elif self.cannon.next_bubble.bubble_type == BubbleType.RAINBOW:
                pygame.draw.circle(self.screen, (255, 255, 255), (next_bubble_x, next_bubble_y), 20)
                pygame.draw.circle(self.screen, (200, 200, 200), (next_bubble_x, next_bubble_y), 20, 2)
            elif self.cannon.next_bubble.bubble_type == BubbleType.PIERCE:
                pygame.draw.circle(self.screen, (100, 200, 255), (next_bubble_x, next_bubble_y), 20)
                pygame.draw.circle(self.screen, (0, 0, 255), (next_bubble_x, next_bubble_y), 20, 2)
            else:
                pygame.draw.circle(self.screen, self.cannon.next_bubble.color, (next_bubble_x, next_bubble_y), 20)
                pygame.draw.circle(self.screen, (255, 255, 255), (next_bubble_x - 6, next_bubble_y - 6), 6)
                pygame.draw.circle(self.screen, (0, 0, 0), (next_bubble_x, next_bubble_y), 20, 1)
        
        pygame.draw.line(self.screen, self.border_color, 
                        (self.game_area_right + 10, 260), 
                        (self.width - 10, 260), 1)
        
        powerup_title = self.font.render('道具说明', True, (200, 200, 200))
        powerup_title_rect = powerup_title.get_rect(center=(self.game_area_right + self.right_panel_width // 2, 285))
        self.screen.blit(powerup_title, powerup_title_rect)
        
        powerup_items = [
            ('💣', '炸弹'),
            ('🌈', '彩虹'),
            ('➡️', '穿透'),
            ('⛏️', '障碍')
        ]
        
        for i, (icon, name) in enumerate(powerup_items):
            item_x = self.game_area_right + 25 + (i % 2) * 55
            item_y = 320 + (i // 2) * 40
            
            icon_text = self.font_small.render(icon, True, (255, 255, 255))
            icon_rect = icon_text.get_rect(center=(item_x, item_y))
            self.screen.blit(icon_text, icon_rect)
            
            name_text = self.font_small.render(name, True, (180, 180, 180))
            name_rect = name_text.get_rect(center=(item_x, item_y + 18))
            self.screen.blit(name_text, name_rect)

    def get_elapsed_time(self):
        """获取游戏用时"""
        if self.game_start_time == 0:
            return '00:00'
        
        elapsed = pygame.time.get_ticks() - self.game_start_time
        minutes = elapsed // 60000
        seconds = (elapsed // 1000) % 60
        return f'{minutes:02d}:{seconds:02d}'

    def handle_event(self, event):
        """处理游戏事件"""
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            if self.game_state == 'playing':
                mouse_x, mouse_y = event.pos
                self.cannon.update_angle(mouse_x, mouse_y)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.game_state == 'start':
                    if self.ui_system.hover_button == '开始游戏':
                        self.reset_game()
                    elif self.ui_system.hover_button == '游戏设置':
                        self.game_state = 'settings'
                    elif self.ui_system.hover_button == '游戏说明':
                        self.game_state = 'instructions'
                    elif self.ui_system.hover_button == '退出游戏':
                        return False
                elif self.game_state == 'paused':
                    if self.ui_system.hover_button == '继续游戏':
                        self.game_state = 'playing'
                    elif self.ui_system.hover_button == '重新开始':
                        self.reset_game()
                    elif self.ui_system.hover_button == '返回主菜单':
                        self.game_state = 'start'
                elif self.game_state == 'win':
                    if self.ui_system.hover_button == '下一关':
                        self.next_level()
                        self.game_state = 'playing'
                    elif self.ui_system.hover_button == '重新开始':
                        self.reset_game()
                    elif self.ui_system.hover_button == '返回主菜单':
                        self.game_state = 'start'
                elif self.game_state == 'gameover':
                    if self.ui_system.hover_button == '重新开始':
                        self.reset_game()
                    elif self.ui_system.hover_button == '返回主菜单':
                        self.game_state = 'start'
                elif self.game_state == 'settings':
                    if self.ui_system.hover_button == '返回主菜单':
                        self.game_state = 'start'
                elif self.game_state == 'instructions':
                    if self.ui_system.hover_button == '返回主菜单':
                        self.game_state = 'start'
                elif self.game_state == 'playing' and self.cannon.is_ready:
                    self.flying_bubble = self.cannon.launch_bubble(self.game_area_left, self.game_area_right, self.height)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.game_state == 'playing':
                    self.game_state = 'paused'
                elif self.game_state == 'paused':
                    self.game_state = 'playing'
                else:
                    self.game_state = 'start'
            
            if event.key == pygame.K_SPACE:
                if self.game_state == 'start':
                    self.reset_game()
                elif self.game_state == 'playing':
                    self.game_state = 'paused'
                elif self.game_state == 'paused':
                    self.game_state = 'playing'
                elif self.game_state == 'gameover':
                    self.reset_game()
        
        return True

    def run(self):
        """运行游戏主循环"""
        clock = pygame.time.Clock()
        
        running = True
        while running:
            for event in pygame.event.get():
                running = self.handle_event(event)
            
            self.update()
            self.draw()
            
            clock.tick(60)
        
        pygame.quit()