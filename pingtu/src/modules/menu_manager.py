import pygame
from config import PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR

class MenuManager:
    def __init__(self, renderer):
        """
        菜单管理类
        :param renderer: 渲染器对象
        """
        self.renderer = renderer
        self.current_menu = 'main'
        self.selected_difficulty = 'easy'
        self.selected_image_path = None

    def handle_main_menu_click(self, mouse_pos):
        """
        处理主菜单点击事件
        :param mouse_pos: 鼠标位置
        :return: 操作类型（'start', 'difficulty', 'rules', 'exit', 'load_image'）
        """
        buttons = self._get_main_menu_buttons()
        self.renderer.draw_main_menu("拼图游戏", buttons)
        
        for btn in buttons:
            if btn['rect'].collidepoint(mouse_pos):
                return btn['action']
        
        return None

    def _get_main_menu_buttons(self):
        """
        获取主菜单按钮配置
        :return: 按钮配置列表
        """
        return [
            {
                'text': '开始游戏',
                'width': 200,
                'height': 50,
                'color': PRIMARY_COLOR,
                'hover_color': SECONDARY_COLOR,
                'action': 'start'
            },
            {
                'text': '难度选择',
                'width': 200,
                'height': 50,
                'color': SECONDARY_COLOR,
                'hover_color': PRIMARY_COLOR,
                'action': 'difficulty'
            },
            {
                'text': '加载图片',
                'width': 200,
                'height': 50,
                'color': ACCENT_COLOR,
                'hover_color': (211, 84, 0),
                'action': 'load_image'
            },
            {
                'text': '游戏规则',
                'width': 200,
                'height': 50,
                'color': (46, 204, 113),
                'hover_color': (39, 174, 96),
                'action': 'rules'
            },
            {
                'text': '退出游戏',
                'width': 200,
                'height': 50,
                'color': (231, 76, 60),
                'hover_color': (192, 57, 43),
                'action': 'exit'
            }
        ]

    def handle_difficulty_menu_click(self, mouse_pos):
        """
        处理难度选择菜单点击事件
        :param mouse_pos: 鼠标位置
        :return: 选择的难度或'back'
        """
        buttons = self.renderer.draw_difficulty_menu()
        
        for btn in buttons:
            if btn['rect'].collidepoint(mouse_pos):
                if btn['key'] != 'back':
                    self.selected_difficulty = btn['key']
                return btn['key']
        
        return None

    def handle_rules_menu_click(self, mouse_pos):
        """
        处理规则说明菜单点击事件
        :param mouse_pos: 鼠标位置
        :return: 'back'或None
        """
        back_btn = self.renderer.draw_rules_menu()
        
        if back_btn.collidepoint(mouse_pos):
            return 'back'
        
        return None

    def draw_main_menu(self):
        """
        绘制主菜单
        """
        buttons = self._get_main_menu_buttons()
        self.renderer.draw_main_menu("拼图游戏", buttons)

    def set_difficulty(self, difficulty):
        """
        设置难度
        :param difficulty: 难度级别（'easy', 'medium', 'hard'）
        """
        if difficulty in ['easy', 'medium', 'hard']:
            self.selected_difficulty = difficulty

    def set_image_path(self, path):
        """
        设置图片路径
        :param path: 图片文件路径
        """
        self.selected_image_path = path

    def get_difficulty(self):
        """
        获取当前选择的难度
        :return: 难度级别
        """
        return self.selected_difficulty

    def get_image_path(self):
        """
        获取当前选择的图片路径
        :return: 图片路径
        """
        return self.selected_image_path

    def set_menu(self, menu_name):
        """
        设置当前菜单
        :param menu_name: 菜单名称
        """
        self.current_menu = menu_name

    def get_menu(self):
        """
        获取当前菜单名称
        :return: 当前菜单名称
        """
        return self.current_menu