import pygame
import os
from config import *

class Renderer:
    def __init__(self, screen):
        """
        界面渲染类
        :param screen: pygame屏幕对象
        """
        self.screen = screen
        self.fonts = {}
        self._init_fonts()

    def _get_chinese_font_path(self):
        """
        获取系统中支持中文的字体路径
        :return: 字体路径，如果找不到则返回None
        """
        font_paths = [
            "C:/Windows/Fonts/simhei.ttf",      
            "C:/Windows/Fonts/msyh.ttc",        
            "C:/Windows/Fonts/msyhbd.ttc",      
            "C:/Windows/Fonts/simsun.ttc",      
            "/Library/Fonts/Songti.ttc",        
            "/Library/Fonts/Heiti.ttc",         
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"  
        ]
        
        for path in font_paths:
            if os.path.exists(path):
                return path
        return None

    def _init_fonts(self):
        """
        初始化字体，优先使用支持中文的字体
        """
        font_path = self._get_chinese_font_path()
        
        if font_path:
            self.fonts = {
                'small': pygame.font.Font(font_path, FONT_SIZE_SMALL),
                'medium': pygame.font.Font(font_path, FONT_SIZE_MEDIUM),
                'large': pygame.font.Font(font_path, FONT_SIZE_LARGE),
                'xlarge': pygame.font.Font(font_path, FONT_SIZE_XLARGE)
            }
        else:
            self.fonts = {
                'small': pygame.font.Font(None, FONT_SIZE_SMALL),
                'medium': pygame.font.Font(None, FONT_SIZE_MEDIUM),
                'large': pygame.font.Font(None, FONT_SIZE_LARGE),
                'xlarge': pygame.font.Font(None, FONT_SIZE_XLARGE)
            }

    def draw_text(self, text, font_size, color, x, y, centered=False):
        """
        绘制文本
        :param text: 文本内容
        :param font_size: 字体大小（'small', 'medium', 'large', 'xlarge'）
        :param color: 文本颜色
        :param x: x坐标
        :param y: y坐标
        :param centered: 是否居中
        """
        font = self.fonts[font_size]
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        
        if centered:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, text, x, y, width, height, color, hover_color, 
                    text_color=TEXT_COLOR, font_size='medium', centered=True):
        """
        绘制按钮
        :param text: 按钮文本
        :param x: x坐标
        :param y: y坐标
        :param width: 宽度
        :param height: 高度
        :param color: 按钮颜色
        :param hover_color: 悬停颜色
        :param text_color: 文本颜色
        :param font_size: 字体大小
        :param centered: 是否居中
        :return: 按钮矩形区域
        """
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(x, y, width, height)
        
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, hover_color, button_rect, border_radius=8)
        else:
            pygame.draw.rect(self.screen, color, button_rect, border_radius=8)
        
        pygame.draw.rect(self.screen, BORDER_COLOR, button_rect, 2, border_radius=8)
        
        if centered:
            self.draw_text(text, font_size, text_color, 
                          button_rect.centerx, button_rect.centery, centered=True)
        else:
            self.draw_text(text, font_size, text_color, x + 10, y + 5)
        
        return button_rect

    def draw_panel(self, x, y, width, height, color=BACKGROUND_COLOR, border_color=BORDER_COLOR):
        """
        绘制面板
        :param x: x坐标
        :param y: y坐标
        :param width: 宽度
        :param height: 高度
        :param color: 面板颜色
        :param border_color: 边框颜色
        :return: 面板矩形区域
        """
        panel_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, border_color, panel_rect, 2, border_radius=10)
        return panel_rect

    def draw_puzzle_grid(self, pieces, grid_size, empty_index, x, y, piece_width, piece_height):
        """
        绘制拼图网格
        :param pieces: 碎片列表
        :param grid_size: 网格大小
        :param empty_index: 空白格位置
        :param x: 起始x坐标
        :param y: 起始y坐标
        :param piece_width: 碎片宽度
        :param piece_height: 碎片高度
        """
        for i in range(grid_size * grid_size):
            row = i // grid_size
            col = i % grid_size
            piece_x = x + col * piece_width
            piece_y = y + row * piece_height
            
            if i == empty_index:
                pygame.draw.rect(self.screen, (200, 200, 200), 
                               (piece_x, piece_y, piece_width, piece_height), 
                               border_radius=5)
                pygame.draw.rect(self.screen, BORDER_COLOR, 
                               (piece_x, piece_y, piece_width, piece_height), 
                               2, border_radius=5)
            else:
                for piece in pieces:
                    if piece.current_index == i:
                        piece.set_position(piece_x, piece_y)
                        piece.draw(self.screen)
                        break

    def draw_preview_image(self, image, x, y, width, height):
        """
        绘制预览图片
        :param image: 原始图片
        :param x: x坐标
        :param y: y坐标
        :param width: 宽度
        :param height: 高度
        """
        scaled_image = pygame.transform.smoothscale(image, (width, height))
        self.screen.blit(scaled_image, (x, y))
        pygame.draw.rect(self.screen, BORDER_COLOR, (x, y, width, height), 2)

    def draw_status_bar(self, steps, time, difficulty, x, y, width, height):
        """
        绘制状态栏
        :param steps: 当前步数
        :param time: 已用时间（秒）
        :param difficulty: 难度名称
        :param x: x坐标
        :param y: y坐标
        :param width: 宽度
        :param height: 高度
        """
        self.draw_panel(x, y, width, height)
        
        time_str = f"{time // 60:02d}:{time % 60:02d}"
        step_text = f"步数: {steps}"
        time_text = f"时间: {time_str}"
        diff_text = f"难度: {difficulty}"
        
        self.draw_text(step_text, 'small', DARK_TEXT_COLOR, x + 15, y + 10)
        self.draw_text(time_text, 'small', DARK_TEXT_COLOR, x + width // 3 + 15, y + 10)
        self.draw_text(diff_text, 'small', DARK_TEXT_COLOR, x + 2 * width // 3 + 15, y + 10)

    def draw_victory_popup(self, steps, time):
        """
        绘制胜利弹窗
        :param steps: 总步数
        :param time: 总时间（秒）
        :return: 按钮矩形区域列表
        """
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        popup_width = 400
        popup_height = 300
        popup_x = (WINDOW_WIDTH - popup_width) // 2
        popup_y = (WINDOW_HEIGHT - popup_height) // 2
        
        self.draw_panel(popup_x, popup_y, popup_width, popup_height, color=(255, 255, 255))
        
        self.draw_text("🎉 恭喜通关！", 'xlarge', PRIMARY_COLOR, 
                      WINDOW_WIDTH // 2, popup_y + 50, centered=True)
        
        time_str = f"{time // 60:02d}:{time % 60:02d}"
        self.draw_text(f"完成步数: {steps}", 'large', DARK_TEXT_COLOR, 
                      WINDOW_WIDTH // 2, popup_y + 120, centered=True)
        self.draw_text(f"用时: {time_str}", 'large', DARK_TEXT_COLOR, 
                      WINDOW_WIDTH // 2, popup_y + 170, centered=True)
        
        btn_width = 150
        btn_height = 45
        btn_x = (WINDOW_WIDTH - btn_width * 2 - 20) // 2
        
        restart_btn = self.draw_button("再来一局", btn_x, popup_y + 220, 
                                      btn_width, btn_height, 
                                      PRIMARY_COLOR, SECONDARY_COLOR)
        
        menu_btn = self.draw_button("返回菜单", btn_x + btn_width + 20, popup_y + 220, 
                                    btn_width, btn_height, 
                                    ACCENT_COLOR, (211, 84, 0))
        
        return [restart_btn, menu_btn]

    def draw_main_menu(self, title, buttons):
        """
        绘制主菜单
        :param title: 标题文本
        :param buttons: 按钮列表
        """
        self.screen.fill(BACKGROUND_COLOR)
        
        self.draw_text(title, 'xlarge', PRIMARY_COLOR, 
                      WINDOW_WIDTH // 2, 80, centered=True)
        
        self.draw_text("一款有趣的图片分割拼图游戏", 'medium', DARK_TEXT_COLOR, 
                      WINDOW_WIDTH // 2, 160, centered=True)
        
        button_y = 250
        for btn in buttons:
            btn_rect = self.draw_button(btn['text'], 
                                       (WINDOW_WIDTH - btn['width']) // 2,
                                       button_y,
                                       btn['width'],
                                       btn['height'],
                                       btn['color'],
                                       btn['hover_color'])
            btn['rect'] = btn_rect
            button_y += btn['height'] + 20
        
        self.draw_text("操作说明：点击与空白格相邻的碎片进行移动", 'small', BORDER_COLOR, 
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50, centered=True)

    def draw_difficulty_menu(self):
        """
        绘制难度选择菜单
        :return: 按钮矩形区域列表
        """
        self.screen.fill(BACKGROUND_COLOR)
        
        self.draw_text("选择难度", 'xlarge', PRIMARY_COLOR, 
                      WINDOW_WIDTH // 2, 80, centered=True)
        
        difficulties = [
            {'name': '初级', 'key': 'easy', 'color': HIGHLIGHT_COLOR},
            {'name': '中级', 'key': 'medium', 'color': ACCENT_COLOR},
            {'name': '高级', 'key': 'hard', 'color': (231, 76, 60)}
        ]
        
        buttons = []
        btn_width = 200
        btn_height = 50
        start_y = 180
        
        for i, diff in enumerate(difficulties):
            y = start_y + i * (btn_height + 30)
            x = (WINDOW_WIDTH - btn_width) // 2
            btn_rect = self.draw_button(diff['name'], x, y, btn_width, btn_height,
                                       diff['color'], (180, 180, 180))
            buttons.append({'rect': btn_rect, 'key': diff['key']})
        
        back_btn = self.draw_button("返回", (WINDOW_WIDTH - 120) // 2, 
                                    WINDOW_HEIGHT - 80, 120, 40, 
                                    SECONDARY_COLOR, PRIMARY_COLOR)
        buttons.append({'rect': back_btn, 'key': 'back'})
        
        return buttons

    def draw_rules_menu(self):
        """
        绘制规则说明菜单
        :return: 返回按钮矩形区域
        """
        self.screen.fill(BACKGROUND_COLOR)
        
        self.draw_text("游戏规则", 'xlarge', PRIMARY_COLOR, 
                      WINDOW_WIDTH // 2, 50, centered=True)
        
        rules = [
            "1. 图片被分割成多个碎片并随机打乱",
            "2. 点击与空白格相邻的碎片进行移动",
            "3. 将所有碎片移动到正确位置即可通关",
            "4. 步数越少、用时越短，成绩越好",
            "5. 可以点击提示按钮获取帮助",
            "6. 可以随时查看原图预览"
        ]
        
        y = 120
        for rule in rules:
            self.draw_text(rule, 'medium', DARK_TEXT_COLOR, 
                          WINDOW_WIDTH // 2, y, centered=True)
            y += 40
        
        back_btn = self.draw_button("返回", (WINDOW_WIDTH - 120) // 2, 
                                    WINDOW_HEIGHT - 80, 120, 40, 
                                    SECONDARY_COLOR, PRIMARY_COLOR)
        
        return back_btn

    def clear_screen(self):
        """
        清除屏幕
        """
        self.screen.fill(BACKGROUND_COLOR)