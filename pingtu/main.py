import pygame
import sys
import os
from config import *
from src.modules.game_logic import GameLogic
from src.modules.renderer import Renderer
from src.modules.menu_manager import MenuManager

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class PuzzleGame:
    def __init__(self):
        """
        拼图游戏主类
        """
        pygame.init()
        pygame.display.set_caption("拼图游戏")
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.renderer = Renderer(self.screen)
        self.menu_manager = MenuManager(self.renderer)
        
        self.game_logic = None
        self.current_state = 'menu'
        self.victory = False
        
        self.puzzle_x = 0
        self.puzzle_y = 0
        self.piece_width = 0
        self.piece_height = 0
        
        self.show_preview = False
        self.preview_toggle = True

    def run(self):
        """
        游戏主循环
        """
        running = True
        
        while running:
            self.clock.tick(FPS)
            self.handle_events()
            
            if self.current_state == 'menu':
                self.handle_menu()
            elif self.current_state == 'game':
                self.handle_game()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

    def handle_events(self):
        """
        处理事件
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.current_state == 'menu':
                    self.handle_menu_click(mouse_pos)
                elif self.current_state == 'game':
                    if not self.victory:
                        self.handle_game_click(mouse_pos)
                    else:
                        self.handle_victory_click(mouse_pos)
            
            if event.type == pygame.USEREVENT + 1:
                if self.game_logic:
                    self.game_logic.reset_hint()

    def handle_menu(self):
        """
        处理菜单状态
        """
        menu = self.menu_manager.get_menu()
        
        if menu == 'main':
            self.menu_manager.draw_main_menu()
        elif menu == 'difficulty':
            self.menu_manager.handle_difficulty_menu_click((-1, -1))
        elif menu == 'rules':
            self.menu_manager.handle_rules_menu_click((-1, -1))

    def handle_menu_click(self, mouse_pos):
        """
        处理菜单点击
        :param mouse_pos: 鼠标位置
        """
        menu = self.menu_manager.get_menu()
        
        if menu == 'main':
            action = self.menu_manager.handle_main_menu_click(mouse_pos)
            
            if action == 'start':
                self.start_game()
            elif action == 'difficulty':
                self.menu_manager.set_menu('difficulty')
            elif action == 'rules':
                self.menu_manager.set_menu('rules')
            elif action == 'load_image':
                self.load_custom_image()
            elif action == 'exit':
                pygame.quit()
                sys.exit()
        
        elif menu == 'difficulty':
            result = self.menu_manager.handle_difficulty_menu_click(mouse_pos)
            if result == 'back':
                self.menu_manager.set_menu('main')
            elif result in ['easy', 'medium', 'hard']:
                self.menu_manager.set_menu('main')
        
        elif menu == 'rules':
            result = self.menu_manager.handle_rules_menu_click(mouse_pos)
            if result == 'back':
                self.menu_manager.set_menu('main')

    def load_custom_image(self):
        """
        加载自定义图片
        """
        try:
            import tkinter as tk
            from tkinter import filedialog
            
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            file_path = filedialog.askopenfilename(
                title='选择图片',
                filetypes=[('图片文件', '*.jpg *.jpeg *.png')]
            )
            
            if file_path:
                self.menu_manager.set_image_path(file_path)
                
        except Exception as e:
            print(f"加载图片失败: {e}")

    def start_game(self):
        """
        开始游戏
        """
        difficulty = self.menu_manager.get_difficulty()
        grid_size = DIFFICULTY_LEVELS[difficulty]['grid_size']
        
        self.game_logic = GameLogic(grid_size)
        image_path = self.menu_manager.get_image_path()
        self.game_logic.load_image_and_split(image_path)
        self.game_logic.shuffle_pieces()
        self.game_logic.start_game()
        
        self.calculate_puzzle_position()
        
        self.current_state = 'game'
        self.victory = False

    def calculate_puzzle_position(self):
        """
        计算拼图显示位置
        """
        if self.game_logic and self.game_logic.original_image:
            img_width, img_height = self.game_logic.original_image.get_size()
            self.piece_width = img_width // self.game_logic.grid_size
            self.piece_height = img_height // self.game_logic.grid_size
            
            self.puzzle_x = (WINDOW_WIDTH - img_width) // 2
            self.puzzle_y = 80

    def handle_game(self):
        """
        处理游戏状态
        """
        self.screen.fill(BACKGROUND_COLOR)
        
        self.game_logic.update_timer()
        
        self.renderer.draw_puzzle_grid(
            self.game_logic.pieces,
            self.game_logic.grid_size,
            self.game_logic.empty_index,
            self.puzzle_x,
            self.puzzle_y,
            self.piece_width,
            self.piece_height
        )
        
        difficulty_name = DIFFICULTY_LEVELS[self.menu_manager.get_difficulty()]['name']
        self.renderer.draw_status_bar(
            self.game_logic.steps,
            self.game_logic.elapsed_time,
            difficulty_name,
            50, WINDOW_HEIGHT - 80,
            WINDOW_WIDTH - 100, 50
        )
        
        self.draw_game_buttons()
        
        if self.show_preview and self.game_logic.original_image:
            self.draw_preview_window()
        
        if self.game_logic.hint_piece is not None:
            self.highlight_hint()
        
        if self.victory:
            self.renderer.draw_victory_popup(
                self.game_logic.steps,
                self.game_logic.elapsed_time
            )

    def draw_game_buttons(self):
        """
        绘制游戏界面按钮
        """
        btn_width = 100
        btn_height = 40
        btn_x = 50
        
        restart_btn = self.renderer.draw_button(
            "重新开始", btn_x, WINDOW_HEIGHT - 150, btn_width, btn_height,
            PRIMARY_COLOR, SECONDARY_COLOR, font_size='small'
        )
        
        hint_btn = self.renderer.draw_button(
            "提示", btn_x + btn_width + 10, WINDOW_HEIGHT - 150, btn_width, btn_height,
            ACCENT_COLOR, (211, 84, 0), font_size='small'
        )
        
        preview_btn = self.renderer.draw_button(
            "原图" if self.preview_toggle else "隐藏", 
            btn_x + (btn_width + 10) * 2, WINDOW_HEIGHT - 150, btn_width, btn_height,
            HIGHLIGHT_COLOR, (39, 174, 96), font_size='small'
        )
        
        menu_btn = self.renderer.draw_button(
            "返回菜单", WINDOW_WIDTH - btn_width - 50, WINDOW_HEIGHT - 150, 
            btn_width, btn_height,
            (231, 76, 60), (192, 57, 43), font_size='small'
        )
        
        mouse_pos = pygame.mouse.get_pos()
        
        if restart_btn.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.game_logic.reset_game()
            self.victory = False
        
        elif hint_btn.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.game_logic.get_hint()
        
        elif preview_btn.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.show_preview = not self.show_preview
            self.preview_toggle = not self.preview_toggle
        
        elif menu_btn.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.return_to_menu()

    def draw_preview_window(self):
        """
        绘制原图预览窗口
        """
        preview_width = 150
        preview_height = 150
        
        x = WINDOW_WIDTH - preview_width - 50
        y = 80
        
        self.renderer.draw_panel(x - 5, y - 5, preview_width + 10, preview_height + 10)
        self.renderer.draw_preview_image(self.game_logic.original_image, x, y, preview_width, preview_height)
        self.renderer.draw_text("原图预览", 'small', DARK_TEXT_COLOR, x + preview_width // 2, y + preview_height + 15, centered=True)

    def highlight_hint(self):
        """
        高亮显示提示的碎片
        """
        if 0 <= self.game_logic.hint_piece < len(self.game_logic.pieces):
            piece = self.game_logic.pieces[self.game_logic.hint_piece]
            piece.is_highlighted = True
            
            pygame.time.set_timer(pygame.USEREVENT + 1, 2000)

    def handle_game_click(self, mouse_pos):
        """
        处理游戏界面点击
        :param mouse_pos: 鼠标位置
        """
        for i, piece in enumerate(self.game_logic.pieces):
            if piece.is_clicked(mouse_pos):
                if self.game_logic.is_valid_move(i):
                    self.game_logic.move_piece(i)
                    self.game_logic.reset_hint()
                    
                    if self.game_logic.check_win():
                        self.game_logic.is_running = False
                        self.victory = True
                break

    def handle_victory_click(self, mouse_pos):
        """
        处理胜利弹窗点击
        :param mouse_pos: 鼠标位置
        """
        buttons = self.renderer.draw_victory_popup(
            self.game_logic.steps,
            self.game_logic.elapsed_time
        )
        
        if buttons[0].collidepoint(mouse_pos):
            self.game_logic.reset_game()
            self.victory = False
        elif buttons[1].collidepoint(mouse_pos):
            self.return_to_menu()

    def return_to_menu(self):
        """
        返回主菜单
        """
        self.current_state = 'menu'
        self.menu_manager.set_menu('main')
        self.victory = False
        self.show_preview = False
        self.preview_toggle = True
        self.game_logic = None

if __name__ == '__main__':
    game = PuzzleGame()
    game.run()