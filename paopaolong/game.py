import pygame
import math
from bubble import Bubble
from cannon import Cannon

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
        game_state: 游戏状态 ('start', 'playing', 'paused', 'win', 'gameover')
        grid: 六边形网格系统
        drop_speed: 泡泡下移速度
        drop_timer: 下移计时器
        left_panel_width: 左侧面板宽度
        right_panel_width: 右侧面板宽度
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
        
        # 设置中文字体 - 使用Windows系统字体路径
        import os
        font_path = None
        
        # Windows系统字体路径
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
                # 加载失败使用默认字体
                self.font = pygame.font.Font(None, 20)
                self.font_large = pygame.font.Font(None, 36)
                self.font_small = pygame.font.Font(None, 16)
        else:
            # 尝试使用系统字体名称
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
        
        # 游戏区域边界
        self.game_area_left = self.left_panel_width
        self.game_area_right = self.width - self.right_panel_width
        self.game_area_width = self.game_area_right - self.game_area_left
        
        # 创建显示窗口
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('泡泡龙')
        
        # 初始化游戏组件
        self.cannon = Cannon(self.width // 2, self.height - 50)
        self.bubbles = []
        self.flying_bubble = None
        self.score = 0
        self.level = 1
        self.game_state = 'start'
        
        # 游戏配置
        self.drop_speed = 0.5
        self.drop_timer = 0
        self.drop_interval = 3000  # 毫秒
        
        # 六边形网格配置
        self.grid_cell_size = 30
        self.grid_cols = 12
        self.grid_rows = 10
        
        # 颜色定义
        self.bg_color = (30, 30, 30)
        self.panel_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        self.border_color = (80, 80, 80)
        
        # 游戏说明
        self.game_instructions = [
            "游戏玩法说明:",
            "",
            "1. 鼠标移动控制炮台角度",
            "2. 点击左键发射泡泡",
            "3. 三个或更多同色泡泡",
            "   相邻时自动消除",
            "4. 消除相连的悬空泡泡",
            "   可获得额外分数",
            "5. 泡泡触达底部则游戏结束",
            "6. 消除所有泡泡通关",
            "",
            "操作提示:",
            "- 空格键: 重新开始",
            "- ESC键: 退出游戏"
        ]
    
    def reset_game(self):
        """重置游戏状态"""
        self.bubbles = []
        self.flying_bubble = None
        self.score = 0
        self.level = 1
        self.game_state = 'playing'
        self.drop_speed = 0.5
        self.cannon = Cannon(self.width // 2, self.height - 50)
        self.create_initial_bubbles()
    
    def create_initial_bubbles(self):
        """创建初始泡泡阵列"""
        # 根据关卡调整初始泡泡数量
        rows_to_create = min(4 + self.level, 7)
        
        for row in range(rows_to_create):
            for col in range(self.grid_cols):
                # 交错排列六边形网格
                offset_x = 0
                if row % 2 == 1:
                    offset_x = self.grid_cell_size / 2
                
                x = self.game_area_left + self.grid_cell_size / 2 + col * self.grid_cell_size + offset_x
                y = 50 + row * (self.grid_cell_size * math.sqrt(3) / 2)
                
                # 随机决定是否放置泡泡
                if pygame.time.get_ticks() % (row + col + 2) != 0:
                    bubble = Bubble(x, y)
                    bubble.grid_pos = (row, col)
                    self.bubbles.append(bubble)
    
    def update(self):
        """更新游戏状态"""
        if self.game_state == 'playing':
            self._update_flying_bubble()
            self._update_drop_timer()
            self._check_game_over()
            self._check_level_complete()
    
    def _update_flying_bubble(self):
        """更新飞行泡泡的状态"""
        if self.flying_bubble:
            self.flying_bubble.update()
            
            # 检测墙壁碰撞
            wall = self.flying_bubble.check_wall_collision(self.game_area_right, self.height)
            if wall:
                self.flying_bubble.reflect(wall)
                # 限制泡泡在游戏区域内
                if wall == 'left':
                    self.flying_bubble.x = self.flying_bubble.radius + 1
                elif wall == 'right':
                    self.flying_bubble.x = self.game_area_right - self.flying_bubble.radius - 1
                elif wall == 'top':
                    self.flying_bubble.y = self.flying_bubble.radius + 1
            
            # 检测与已放置泡泡的碰撞
            for bubble in self.bubbles:
                if self.flying_bubble.check_collision(bubble):
                    self._place_bubble()
                    return
            
            # 检测是否飞出底部
            if self.flying_bubble.y > self.height:
                self.flying_bubble = None
                self.cannon.set_ready()
    
    def _place_bubble(self):
        """放置泡泡并检测消除"""
        self.flying_bubble.stop_flying()
        self.bubbles.append(self.flying_bubble)
        self.flying_bubble = None
        self.cannon.set_ready()
        
        # 检测消除
        self._check_and_clear_matches()
    
    def _check_and_clear_matches(self):
        """检测并消除匹配的泡泡"""
        if not self.bubbles:
            return
        
        # 找到最后添加的泡泡
        last_bubble = self.bubbles[-1]
        
        # 查找相连的同色泡泡
        matched = self._find_connected_bubbles(last_bubble)
        
        if len(matched) >= 3:
            # 移除匹配的泡泡
            for bubble in matched:
                if bubble in self.bubbles:
                    self.bubbles.remove(bubble)
                    self.score += 10  # 每个泡泡10分
            
            # 检测悬空泡泡
            self._check_hanging_bubbles()
    
    def _find_connected_bubbles(self, start_bubble):
        """
        查找相连的同色泡泡
        
        参数:
            start_bubble: 起始泡泡
        
        返回:
            list: 相连的同色泡泡列表
        """
        matched = []
        visited = set()
        stack = [start_bubble]
        
        while stack:
            bubble = stack.pop()
            if bubble in visited:
                continue
            visited.add(bubble)
            
            if bubble.color == start_bubble.color:
                matched.append(bubble)
                
                # 检查相邻泡泡
                for other in self.bubbles:
                    if other not in visited and bubble.check_collision(other):
                        stack.append(other)
        
        return matched
    
    def _check_hanging_bubbles(self):
        """检测并移除悬空的泡泡"""
        if not self.bubbles:
            return
        
        # 找到所有连接到顶部的泡泡
        connected_to_top = set()
        stack = []
        
        # 初始化：找到所有顶部的泡泡
        for bubble in self.bubbles:
            if bubble.y <= bubble.radius + 20:
                stack.append(bubble)
                connected_to_top.add(bubble)
        
        # BFS查找所有连接到顶部的泡泡
        while stack:
            bubble = stack.pop()
            for other in self.bubbles:
                if other not in connected_to_top and bubble.check_collision(other):
                    connected_to_top.add(other)
                    stack.append(other)
        
        # 移除悬空的泡泡
        hanging_bubbles = []
        for bubble in self.bubbles:
            if bubble not in connected_to_top:
                hanging_bubbles.append(bubble)
        
        for bubble in hanging_bubbles:
            self.bubbles.remove(bubble)
            self.score += 20  # 悬空泡泡额外20分
    
    def _update_drop_timer(self):
        """更新泡泡下移计时器"""
        self.drop_timer += 16  # 约60fps
        
        if self.drop_timer >= self.drop_interval:
            self.drop_timer = 0
            self._drop_all_bubbles()
    
    def _drop_all_bubbles(self):
        """将所有泡泡下移"""
        for bubble in self.bubbles:
            bubble.y += self.drop_speed * self.level
    
    def _check_game_over(self):
        """检查游戏是否结束"""
        for bubble in self.bubbles:
            if bubble.y + bubble.radius > self.height - 80:
                self.game_state = 'gameover'
                return
    
    def _check_level_complete(self):
        """检查是否通关"""
        if not self.bubbles and self.game_state == 'playing':
            self.level += 1
            self.drop_speed += 0.1  # 增加难度
            self.create_initial_bubbles()
    
    def draw(self):
        """绘制游戏界面"""
        # 清空屏幕
        self.screen.fill(self.bg_color)
        
        # 绘制左侧面板
        self._draw_left_panel()
        
        # 绘制右侧面板
        self._draw_right_panel()
        
        # 绘制游戏区域边框
        pygame.draw.rect(self.screen, self.border_color, 
                        (self.game_area_left, 0, self.game_area_width, self.height), 2)
        
        # 绘制已放置的泡泡
        for bubble in self.bubbles:
            bubble.draw(self.screen)
        
        # 绘制飞行中的泡泡
        if self.flying_bubble:
            self.flying_bubble.draw(self.screen)
        
        # 绘制炮台
        if self.game_state == 'playing':
            self.cannon.draw(self.screen)
        
        # 绘制游戏开始界面
        if self.game_state == 'start':
            self._draw_start_screen()
        
        # 绘制游戏结束界面
        if self.game_state == 'gameover':
            self._draw_gameover_screen()
        
        # 刷新显示
        pygame.display.flip()
    
    def _draw_left_panel(self):
        """绘制左侧信息面板"""
        # 面板背景
        pygame.draw.rect(self.screen, self.panel_color, (0, 0, self.left_panel_width, self.height))
        
        # 面板边框
        pygame.draw.rect(self.screen, self.border_color, (0, 0, self.left_panel_width, self.height), 2)
        
        # 标题
        title_text = self.font_large.render('泡泡龙', True, self.text_color)
        title_rect = title_text.get_rect(center=(self.left_panel_width // 2, 40))
        self.screen.blit(title_text, title_rect)
        
        # 分隔线
        pygame.draw.line(self.screen, self.border_color, (10, 80), (self.left_panel_width - 10, 80), 2)
        
        # 得分
        score_text = self.font.render(f'得分: {self.score}', True, self.text_color)
        score_rect = score_text.get_rect(center=(self.left_panel_width // 2, 120))
        self.screen.blit(score_text, score_rect)
        
        # 关卡
        level_text = self.font.render(f'关卡: {self.level}', True, self.text_color)
        level_rect = level_text.get_rect(center=(self.left_panel_width // 2, 160))
        self.screen.blit(level_text, level_rect)
        
        # 游戏状态
        state_text = self.font.render(f'状态: {self._get_state_text()}', True, self.text_color)
        state_rect = state_text.get_rect(center=(self.left_panel_width // 2, 200))
        self.screen.blit(state_text, state_rect)
        
        # 泡泡数量
        count_text = self.font.render(f'泡泡数: {len(self.bubbles)}', True, self.text_color)
        count_rect = count_text.get_rect(center=(self.left_panel_width // 2, 240))
        self.screen.blit(count_text, count_rect)
    
    def _draw_right_panel(self):
        """绘制右侧预览面板"""
        # 面板背景
        pygame.draw.rect(self.screen, self.panel_color, 
                        (self.game_area_right, 0, self.right_panel_width, self.height))
        
        # 面板边框
        pygame.draw.rect(self.screen, self.border_color, 
                        (self.game_area_right, 0, self.right_panel_width, self.height), 2)
        
        # 标题
        title_text = self.font.render('泡泡预览', True, self.text_color)
        title_rect = title_text.get_rect(center=(self.game_area_right + self.right_panel_width // 2, 40))
        self.screen.blit(title_text, title_rect)
        
        # 分隔线
        pygame.draw.line(self.screen, self.border_color, 
                        (self.game_area_right + 10, 70), 
                        (self.width - 10, 70), 2)
        
        # 当前泡泡预览
        current_label = self.font_small.render('当前:', True, self.text_color)
        current_label_rect = current_label.get_rect(center=(self.game_area_right + self.right_panel_width // 2, 100))
        self.screen.blit(current_label, current_label_rect)
        
        if self.cannon.current_bubble:
            current_bubble_x = self.game_area_right + self.right_panel_width // 2
            current_bubble_y = 140
            pygame.draw.circle(self.screen, self.cannon.current_bubble.color, 
                            (current_bubble_x, current_bubble_y), 20)
            pygame.draw.circle(self.screen, (255, 255, 255), 
                            (current_bubble_x - 6, current_bubble_y - 6), 6)
            pygame.draw.circle(self.screen, (0, 0, 0), 
                            (current_bubble_x, current_bubble_y), 20, 1)
        
        # 下一个泡泡预览
        next_label = self.font_small.render('下一个:', True, self.text_color)
        next_label_rect = next_label.get_rect(center=(self.game_area_right + self.right_panel_width // 2, 180))
        self.screen.blit(next_label, next_label_rect)
        
        if self.cannon.next_bubble:
            next_bubble_x = self.game_area_right + self.right_panel_width // 2
            next_bubble_y = 220
            pygame.draw.circle(self.screen, self.cannon.next_bubble.color, 
                            (next_bubble_x, next_bubble_y), 20)
            pygame.draw.circle(self.screen, (255, 255, 255), 
                            (next_bubble_x - 6, next_bubble_y - 6), 6)
            pygame.draw.circle(self.screen, (0, 0, 0), 
                            (next_bubble_x, next_bubble_y), 20, 1)
    
    def _draw_start_screen(self):
        """绘制游戏开始界面"""
        # 半透明遮罩
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # 标题
        title_text = self.font_large.render('泡泡龙', True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # 绘制说明文字
        y_offset = 150
        for line in self.game_instructions:
            if line == "":
                y_offset += 15
                continue
            text = self.font_small.render(line, True, (200, 200, 200))
            text_rect = text.get_rect(center=(self.width // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 25
        
        # 开始提示
        start_text = self.font.render('点击鼠标或按空格键开始游戏', True, (0, 255, 0))
        start_rect = start_text.get_rect(center=(self.width // 2, y_offset + 40))
        self.screen.blit(start_text, start_rect)
    
    def _draw_gameover_screen(self):
        """绘制游戏结束界面"""
        # 半透明遮罩
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # 游戏结束文字
        gameover_text = self.font_large.render('游戏结束', True, (255, 0, 0))
        gameover_rect = gameover_text.get_rect(center=(self.width // 2, 150))
        self.screen.blit(gameover_text, gameover_rect)
        
        # 得分显示
        score_text = self.font.render(f'最终得分: {self.score}', True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.width // 2, 220))
        self.screen.blit(score_text, score_rect)
        
        # 关卡显示
        level_text = self.font.render(f'到达关卡: {self.level}', True, (255, 255, 255))
        level_rect = level_text.get_rect(center=(self.width // 2, 260))
        self.screen.blit(level_text, level_rect)
        
        # 重新开始提示
        restart_text = self.font.render('按空格键重新开始', True, (0, 255, 0))
        restart_rect = restart_text.get_rect(center=(self.width // 2, 320))
        self.screen.blit(restart_text, restart_rect)
        
        # 退出提示
        exit_text = self.font.render('按ESC键退出游戏', True, (200, 200, 200))
        exit_rect = exit_text.get_rect(center=(self.width // 2, 360))
        self.screen.blit(exit_text, exit_rect)
    
    def _get_state_text(self):
        """获取游戏状态文字"""
        if self.game_state == 'start':
            return '准备开始'
        elif self.game_state == 'playing':
            return '游戏中'
        elif self.game_state == 'gameover':
            return '游戏结束'
        else:
            return self.game_state
    
    def handle_event(self, event):
        """
        处理游戏事件
        
        参数:
            event: pygame事件对象
        """
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_SPACE:
                if self.game_state == 'start' or self.game_state == 'gameover':
                    self.reset_game()
        
        if event.type == pygame.MOUSEMOTION:
            if self.game_state == 'playing':
                mouse_x, mouse_y = event.pos
                self.cannon.update_angle(mouse_x, mouse_y)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.game_state == 'start':
                    self.reset_game()
                elif self.game_state == 'playing' and self.cannon.is_ready:
                    self.flying_bubble = self.cannon.launch_bubble()
        
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
            
            clock.tick(60)  # 固定60fps
        
        pygame.quit()