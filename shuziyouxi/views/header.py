import customtkinter as ctk
from config import Config

class Header(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=15)
        self._create_widgets()
    
    def _create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=0)
        
        self.title_label = ctk.CTkLabel(
            self, 
            text="🧮 小学数学数字游戏", 
            font=Config.FONTS["title"],
            text_color="#FF6B6B"
        )
        self.title_label.grid(row=0, column=0, columnspan=5, pady=10)
        
        self.level_frame = ctk.CTkFrame(self, corner_radius=10)
        self.level_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.level_frame.grid_columnconfigure(0, weight=1)
        
        self.level_label = ctk.CTkLabel(
            self.level_frame, 
            text="第 1 关", 
            font=Config.FONTS["subtitle"],
            text_color="#4ECDC4"
        )
        self.level_label.pack(pady=5)
        
        self.level_name_label = ctk.CTkLabel(
            self.level_frame, 
            text="入门级", 
            font=Config.FONTS["label"],
            text_color="#6C757D"
        )
        self.level_name_label.pack(pady=0)
        
        self.grade_frame = ctk.CTkFrame(self, corner_radius=10)
        self.grade_frame.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.grade_frame.grid_columnconfigure(0, weight=1)
        
        self.grade_label = ctk.CTkLabel(
            self.grade_frame, 
            text="一年级上", 
            font=Config.FONTS["subtitle"],
            text_color="#45B7D1"
        )
        self.grade_label.pack(pady=5)
        
        self.type_label = ctk.CTkLabel(
            self.grade_frame, 
            text="数数", 
            font=Config.FONTS["label"],
            text_color="#6C757D"
        )
        self.type_label.pack(pady=0)
        
        self.score_frame = ctk.CTkFrame(self, corner_radius=10)
        self.score_frame.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        self.score_frame.grid_columnconfigure(0, weight=1)
        
        self.score_label = ctk.CTkLabel(
            self.score_frame, 
            text="得分: 0", 
            font=Config.FONTS["subtitle"],
            text_color="#96CEB4"
        )
        self.score_label.pack(pady=5)
        
        self.accuracy_label = ctk.CTkLabel(
            self.score_frame, 
            text="正确率: 0%", 
            font=Config.FONTS["label"],
            text_color="#6C757D"
        )
        self.accuracy_label.pack(pady=0)
        
        self.progress_frame = ctk.CTkFrame(self, corner_radius=10)
        self.progress_frame.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        self.progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame, 
            text="进度: 0/5", 
            font=Config.FONTS["subtitle"],
            text_color="#F39C12"
        )
        self.progress_label.pack(pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            height=10,
            corner_radius=5,
            progress_color="#F39C12"
        )
        self.progress_bar.pack(padx=10, pady=5, fill="x")
        self.progress_bar.set(0)
        
        self.theme_switch = ctk.CTkSwitch(
            self, 
            text="深色", 
            font=Config.FONTS["label"],
            command=self._on_theme_switch
        )
        self.theme_switch.grid(row=1, column=4, padx=10, pady=5)
        
        self.theme_callback = None
    
    def set_info(self, level: int, level_name: str, grade: str, question_type: str, 
                 score: int, accuracy: float, current_q: int, total_q: int):
        self.level_label.configure(text=f"第 {level} 关")
        self.level_name_label.configure(text=level_name)
        self.grade_label.configure(text=grade)
        self.type_label.configure(text=question_type)
        self.score_label.configure(text=f"得分: {score}")
        self.accuracy_label.configure(text=f"正确率: {accuracy}%")
        self.progress_label.configure(text=f"进度: {current_q}/{total_q}")
        if total_q > 0:
            self.progress_bar.set(current_q / total_q)
        else:
            self.progress_bar.set(0)
    
    def bind_theme_switch(self, callback):
        self.theme_callback = callback
    
    def _on_theme_switch(self):
        if self.theme_callback:
            self.theme_callback()
    
    def set_theme_switch_state(self, is_dark: bool):
        self.theme_switch.select() if is_dark else self.theme_switch.deselect()