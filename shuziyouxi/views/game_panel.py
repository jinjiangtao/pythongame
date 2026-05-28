import customtkinter as ctk
from config import Config

class GamePanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=15)
        self.pattern_size = 50
        self.pattern_labels = []
        self._create_widgets()
    
    def _create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.question_label = ctk.CTkLabel(
            self,
            text="",
            font=Config.FONTS["large_number"],
            text_color="#333",
            wraplength=700,
            justify="center"
        )
        self.question_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    
    def display_patterns(self, pattern: str, positions: list):
        self.clear()
        
        for (x, y) in positions:
            label = ctk.CTkLabel(
                self,
                text=pattern,
                font=("Arial", 40),
                bg_color="transparent"
            )
            label.place(x=x - self.pattern_size // 2, y=y - self.pattern_size // 2)
            self.pattern_labels.append(label)
    
    def display_question(self, content: str):
        self.clear()
        self.question_label.configure(text=content)
        self.question_label.lift()
    
    def clear(self):
        for label in self.pattern_labels:
            label.destroy()
        self.pattern_labels.clear()
        self.question_label.configure(text="")
    
    def get_size(self):
        self.update_idletasks()
        return (self.winfo_width(), self.winfo_height())