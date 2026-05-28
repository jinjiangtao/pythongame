import customtkinter as ctk
from views.game_panel import GamePanel
from views.number_buttons import NumberButtons
from views.status_bar import StatusBar
from views.header import Header

class MainWindow:
    """主窗口视图 - 整合所有UI组件"""
    
    def __init__(self, master):
        self.master = master
        self.master.geometry("600x700")
        
        self._setup_styles()
        self._create_widgets()
    
    def _setup_styles(self):
        """设置全局样式"""
        self.font_large = ("Microsoft YaHei", 24, "bold")
        self.font_medium = ("Microsoft YaHei", 18, "bold")
        self.font_small = ("Microsoft YaHei", 14)
        
        ctk.set_default_color_theme("blue")
    
    def _create_widgets(self):
        """创建所有UI组件"""
        self.header = Header(self.master)
        self.header.pack(fill="x", padx=20, pady=15)
        
        self.game_panel = GamePanel(self.master)
        self.game_panel.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.number_buttons = NumberButtons(self.master)
        self.number_buttons.pack(fill="x", padx=20, pady=10)
        
        self.status_bar = StatusBar(self.master)
        self.status_bar.pack(fill="x", padx=20, pady=15)
    
    def set_header_info(self, level: int, level_name: str, progress: str, accuracy: float):
        """更新头部信息"""
        self.header.set_info(level, level_name, progress, accuracy)
    
    def display_patterns(self, pattern: str, positions: list):
        """在游戏面板显示图案"""
        self.game_panel.display_patterns(pattern, positions)
    
    def clear_panel(self):
        """清空游戏面板"""
        self.game_panel.clear()
    
    def set_number_buttons_range(self, min_num: int, max_num: int):
        """设置数字按钮范围"""
        self.number_buttons.set_range(min_num, max_num)
    
    def select_number(self, number: int):
        """选中数字"""
        self.number_buttons.select(number)
    
    def clear_selection(self):
        """清除数字选择"""
        self.number_buttons.clear_selection()
    
    def set_status_text(self, text: str, is_success: bool = None):
        """设置状态栏文字"""
        self.status_bar.set_text(text, is_success)
    
    def set_feedback(self, text: str, is_success: bool):
        """显示答题反馈"""
        self.status_bar.set_feedback(text, is_success)
    
    def bind_number_click(self, callback):
        """绑定数字按钮点击事件"""
        self.number_buttons.bind_click(callback)
    
    def bind_submit(self, callback):
        """绑定提交按钮点击事件"""
        self.number_buttons.bind_submit(callback)
    
    def bind_next(self, callback):
        """绑定下一题按钮点击事件"""
        self.number_buttons.bind_next(callback)
    
    def bind_restart(self, callback):
        """绑定重新开始按钮点击事件"""
        self.number_buttons.bind_restart(callback)
    
    def bind_theme_switch(self, callback):
        """绑定主题切换事件"""
        self.header.bind_theme_switch(callback)
    
    def enable_submit(self, enable: bool):
        """启用/禁用提交按钮"""
        self.number_buttons.enable_submit(enable)
    
    def enable_next(self, enable: bool):
        """启用/禁用下一题按钮"""
        self.number_buttons.enable_next(enable)