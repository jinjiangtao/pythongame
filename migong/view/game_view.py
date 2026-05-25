import pygame
import os
from model.items import ItemType

class Colors:
    BACKGROUND = (245, 245, 245)
    WALL = (60, 60, 60)
    PATH = (255, 255, 255)
    START = (0, 255, 0)
    END = (255, 0, 0)
    PLAYER = (0, 100, 200)
    PLAYER_OUTLINE = (0, 50, 100)
    HEALTH_ITEM = (0, 200, 0)
    TRAP_ITEM = (200, 0, 0)
    UI_TEXT = (30, 30, 30)
    UI_BG = (200, 200, 200)
    MESSAGE_BG = (200, 200, 200)
    MESSAGE_TEXT = (30, 30, 30)
    HELP_BG = (230, 230, 230)
    HELP_TEXT = (50, 50, 50)

class GameView:
    def __init__(self, screen):
        self.screen = screen
        self.cell_size = 30
        self.ui_height = 60
        self.font = self.get_chinese_font(20)
        self.large_font = self.get_chinese_font(36)
        self.message_timer = 0
        self.current_message = ""
    
    def get_chinese_font(self, size):
        font_paths = [
            'simhei.ttf',
            'msyh.ttc',
            'simsun.ttc',
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'simhei.ttf'),
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'msyh.ttc'),
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'simsun.ttc'),
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'kaiu.ttf'),
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'msyh.ttf'),
        ]
        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    return pygame.font.Font(font_path, size)
            except:
                continue
        
        try:
            font = pygame.font.Font(None, size)
            font.set_bold(True)
            return font
        except:
            return pygame.font.Font(None, size)

    def render(self, maze, player, item_manager, level):
        self.draw_background()
        self.draw_help_panel()
        self.draw_maze(maze)
        self.draw_items(item_manager, maze)
        self.draw_player(player)
        self.draw_ui(player, level)
        self.draw_message()

    def draw_background(self):
        self.screen.fill(Colors.BACKGROUND)

    def draw_maze(self, maze):
        cell_size = maze.cell_size
        offset_x = 180
        for y in range(maze.height):
            for x in range(maze.width):
                rect = pygame.Rect(
                    x * cell_size + offset_x,
                    y * cell_size,
                    cell_size - 1,
                    cell_size - 1
                )
                if maze.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, Colors.WALL, rect)
                else:
                    pygame.draw.rect(self.screen, Colors.PATH, rect)
        
        start_x, start_y = maze.get_screen_coords(maze.start[0], maze.start[1])
        end_x, end_y = maze.get_screen_coords(maze.end[0], maze.end[1])
        
        pygame.draw.circle(self.screen, Colors.START, 
                          (start_x + cell_size // 2 + offset_x, start_y + cell_size // 2), 
                          cell_size // 3)
        pygame.draw.circle(self.screen, Colors.END, 
                          (end_x + cell_size // 2 + offset_x, end_y + cell_size // 2), 
                          cell_size // 3)

    def draw_player(self, player):
        cell_size = player.maze.cell_size
        offset_x = 180
        center_x = player.screen_x + cell_size // 2 + offset_x
        center_y = player.screen_y + cell_size // 2
        
        pygame.draw.circle(self.screen, Colors.PLAYER_OUTLINE, (center_x, center_y), cell_size // 2 + 2)
        pygame.draw.circle(self.screen, Colors.PLAYER, (center_x, center_y), cell_size // 2)
        
        pygame.draw.circle(self.screen, (255, 255, 255), (center_x - 4, center_y - 3), 3)
        pygame.draw.circle(self.screen, (255, 255, 255), (center_x + 4, center_y - 3), 3)
        pygame.draw.circle(self.screen, (0, 0, 0), (center_x - 4, center_y - 3), 1)
        pygame.draw.circle(self.screen, (0, 0, 0), (center_x + 4, center_y - 3), 1)
        
        pygame.draw.arc(self.screen, (255, 150, 150), 
                       (center_x - 5, center_y + 2, 10, 6), 0, 3.14, 2)

    def draw_items(self, item_manager, maze):
        cell_size = maze.cell_size
        offset_x = 180
        for item in item_manager.items:
            if not item.collected:
                x, y = item.get_screen_coords(maze)
                center_x = x + cell_size // 2 + offset_x
                center_y = y + cell_size // 2
                
                if item.type == ItemType.HEALTH:
                    pygame.draw.polygon(self.screen, Colors.HEALTH_ITEM, [
                        (center_x, center_y - 8),
                        (center_x - 6, center_y - 2),
                        (center_x - 6, center_y + 4),
                        (center_x, center_y + 10),
                        (center_x + 6, center_y + 4),
                        (center_x + 6, center_y - 2)
                    ])
                elif item.type == ItemType.TRAP:
                    pygame.draw.polygon(self.screen, Colors.TRAP_ITEM, [
                        (center_x, center_y - 8),
                        (center_x + 6, center_y - 2),
                        (center_x + 6, center_y + 4),
                        (center_x, center_y + 10),
                        (center_x - 6, center_y + 4),
                        (center_x - 6, center_y - 2)
                    ])

    def draw_ui(self, player, level):
        ui_y = self.screen.get_height() - self.ui_height
        pygame.draw.rect(self.screen, Colors.UI_BG, (0, ui_y, self.screen.get_width(), self.ui_height))
        
        level_text = self.font.render(f"关卡: {level}", True, Colors.UI_TEXT)
        health_text = self.font.render(f"生命: {player.health}/{player.max_health}", True, (255, 0, 0))
        steps_text = self.font.render(f"步数: {player.steps}", True, Colors.UI_TEXT)
        
        self.screen.blit(level_text, (20, ui_y + 15))
        self.screen.blit(health_text, (150, ui_y + 15))
        self.screen.blit(steps_text, (300, ui_y + 15))
        
        pause_text = self.font.render("P: 暂停 | R: 重新开始 | ESC: 退出", True, Colors.UI_TEXT)
        self.screen.blit(pause_text, (self.screen.get_width() - 400, ui_y + 15))
    
    def draw_help_panel(self):
        panel_width = 180
        panel_height = self.screen.get_height() - self.ui_height
        
        pygame.draw.rect(self.screen, Colors.HELP_BG, (0, 0, panel_width, panel_height))
        pygame.draw.rect(self.screen, (150, 150, 150), (panel_width - 1, 0, 1, panel_height))
        
        help_lines = [
            "游戏说明",
            "",
            "操作方式:",
            "↑↓←→ / WASD",
            "移动角色",
            "",
            "游戏目标:",
            "从绿色起点",
            "到达红色终点",
            "",
            "道具说明:",
            "❤ 绿色心形",
            "恢复1点生命",
            "✱ 红色陷阱",
            "减少1点生命",
            "",
            "游戏规则:",
            "步数超限或",
            "生命耗尽则",
            "游戏结束",
            "",
            "快捷键:",
            "P - 暂停",
            "R - 重新开始",
            "ESC - 退出",
        ]
        
        start_y = 20
        line_height = 22
        
        for i, line in enumerate(help_lines):
            if line == "":
                start_y += line_height
                continue
            
            if i == 0:
                text = self.font.render(line, True, (0, 80, 150))
            elif line in ["操作方式:", "游戏目标:", "道具说明:", "游戏规则:", "快捷键:"]:
                text = self.font.render(line, True, (80, 80, 80))
            else:
                text = self.font.render(line, True, Colors.HELP_TEXT)
            
            self.screen.blit(text, (15, start_y))
            start_y += line_height

    def show_message(self, message, duration=1500):
        self.current_message = message
        self.message_timer = pygame.time.get_ticks() + duration

    def draw_message(self):
        if self.current_message and pygame.time.get_ticks() < self.message_timer:
            text = self.large_font.render(self.current_message, True, Colors.MESSAGE_TEXT)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            
            padding = 20
            bg_rect = pygame.Rect(
                text_rect.left - padding,
                text_rect.top - padding,
                text_rect.width + padding * 2,
                text_rect.height + padding * 2
            )
            
            pygame.draw.rect(self.screen, Colors.MESSAGE_BG, bg_rect)
            pygame.draw.rect(self.screen, Colors.UI_TEXT, bg_rect, 2)
            self.screen.blit(text, text_rect)
        else:
            self.current_message = ""

    def draw_pause_screen(self):
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((50, 50, 50))
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.large_font.render("游戏暂停", True, (255, 255, 255))
        hint_text = self.font.render("按 P 继续游戏", True, (200, 200, 200))
        
        pause_rect = pause_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 30))
        hint_rect = hint_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 20))
        
        self.screen.blit(pause_text, pause_rect)
        self.screen.blit(hint_text, hint_rect)

    def draw_game_over(self, level, steps):
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(200)
        overlay.fill((30, 30, 30))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.large_font.render("游戏结束", True, (255, 100, 100))
        level_text = self.font.render(f"到达关卡: {level}", True, (255, 255, 255))
        steps_text = self.font.render(f"总步数: {steps}", True, (255, 255, 255))
        restart_text = self.font.render("按 R 重新开始 | 按 ESC 退出", True, (200, 200, 200))
        
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 60))
        level_rect = level_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 10))
        steps_rect = steps_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 30))
        restart_rect = restart_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 80))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(level_text, level_rect)
        self.screen.blit(steps_text, steps_rect)
        self.screen.blit(restart_text, restart_rect)