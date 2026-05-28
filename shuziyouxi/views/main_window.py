import customtkinter as ctk
from views.game_panel import GamePanel
from views.number_buttons import NumberButtons
from views.status_bar import StatusBar
from views.header import Header
from config import Config

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.geometry(Config.WINDOW_SIZE)
        self.master.title(Config.WINDOW_TITLE)
        self.master.resizable(False, False)
        
        self._setup_styles()
        self._create_widgets()
    
    def _setup_styles(self):
        ctk.set_default_color_theme("blue")
    
    def _create_widgets(self):
        self.header = Header(self.master)
        self.header.pack(fill="x", padx=20, pady=15)
        
        self.game_panel = GamePanel(self.master)
        self.game_panel.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.number_buttons = NumberButtons(self.master)
        self.number_buttons.pack(fill="x", padx=20, pady=10)
        
        self.status_bar = StatusBar(self.master)
        self.status_bar.pack(fill="x", padx=20, pady=15)
    
    def set_header_info(self, level: int, level_name: str, grade: str, question_type: str,
                        score: int, accuracy: float, current_q: int, total_q: int):
        self.header.set_info(level, level_name, grade, question_type, score, accuracy, current_q, total_q)
    
    def display_patterns(self, pattern: str, positions: list):
        self.game_panel.display_patterns(pattern, positions)
    
    def display_question(self, content: str):
        self.game_panel.display_question(content)
    
    def clear_panel(self):
        self.game_panel.clear()
    
    def set_options(self, options: list):
        self.number_buttons.set_options(options)
    
    def set_time(self, seconds: int):
        self.number_buttons.set_time(seconds)
    
    def select_number(self, number: int):
        self.number_buttons.select(number)
    
    def clear_selection(self):
        self.number_buttons.clear_selection()
    
    def set_status_text(self, text: str, is_success: bool = None):
        self.status_bar.set_text(text, is_success)
    
    def set_feedback(self, text: str, is_success: bool):
        self.status_bar.set_feedback(text, is_success)
    
    def set_hint(self, text: str):
        self.status_bar.set_hint(text)
    
    def bind_number_click(self, callback):
        self.number_buttons.bind_click(callback)
    
    def bind_submit(self, callback):
        self.number_buttons.bind_submit(callback)
    
    def bind_next(self, callback):
        self.number_buttons.bind_next(callback)
    
    def bind_restart(self, callback):
        self.number_buttons.bind_restart(callback)
    
    def bind_theme_switch(self, callback):
        self.header.bind_theme_switch(callback)
    
    def enable_submit(self, enable: bool):
        self.number_buttons.enable_submit(enable)
    
    def enable_next(self, enable: bool):
        self.number_buttons.enable_next(enable)