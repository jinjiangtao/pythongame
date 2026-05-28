import customtkinter as ctk
from config import Config

class StatusBar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=15)
        self._create_widgets()
    
    def _create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        self.guide_frame = ctk.CTkFrame(self, corner_radius=10)
        self.guide_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.guide_label = ctk.CTkLabel(
            self.guide_frame,
            text="请点击上方数字按钮选择答案",
            font=Config.FONTS["label"],
            text_color="#6C757D"
        )
        self.guide_label.pack(pady=5)
        
        self.feedback_frame = ctk.CTkFrame(self, corner_radius=10)
        self.feedback_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.feedback_label = ctk.CTkLabel(
            self.feedback_frame,
            text="",
            font=Config.FONTS["button"]
        )
        self.feedback_label.pack(pady=5)
        
        self.hint_frame = ctk.CTkFrame(self, corner_radius=10)
        self.hint_frame.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        self.hint_label = ctk.CTkLabel(
            self.hint_frame,
            text="💡 提示：点击数字选择答案",
            font=Config.FONTS["label"],
            text_color="#6C757D"
        )
        self.hint_label.pack(pady=5)
    
    def set_text(self, text: str, is_success: bool = None):
        self.guide_label.configure(text=text)
        if is_success is not None:
            color = "#27AE60" if is_success else "#E74C3C"
            self.guide_label.configure(text_color=color)
        else:
            self.guide_label.configure(text_color="#6C757D")
    
    def set_feedback(self, text: str, is_success: bool):
        color = "#27AE60" if is_success else "#E74C3C"
        self.feedback_label.configure(text=text, text_color=color)
    
    def set_hint(self, text: str):
        self.hint_label.configure(text=f"💡 提示：{text}")