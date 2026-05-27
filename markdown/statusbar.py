import customtkinter as ctk

class StatusBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10, height=40)
        
        self.create_widgets()
    
    def create_widgets(self):
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.pack(side="left", fill="y", padx=15)
        
        self.line_label = ctk.CTkLabel(self.left_frame, text="行: 1", font=("Microsoft YaHei", 13))
        self.line_label.pack(side="left", padx=15, pady=8)
        
        self.col_label = ctk.CTkLabel(self.left_frame, text="列: 0", font=("Microsoft YaHei", 13))
        self.col_label.pack(side="left", padx=15, pady=8)
        
        self.char_label = ctk.CTkLabel(self.left_frame, text="字符: 0", font=("Microsoft YaHei", 13))
        self.char_label.pack(side="left", padx=15, pady=8)
        
        self.word_label = ctk.CTkLabel(self.left_frame, text="字数: 0", font=("Microsoft YaHei", 13))
        self.word_label.pack(side="left", padx=15, pady=8)
        
        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.pack(side="left", fill="y", expand=True)
        
        self.file_label = ctk.CTkLabel(self.center_frame, text="文件: 未保存", font=("Microsoft YaHei", 13))
        self.file_label.pack(side="left", padx=15, pady=8)
        
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.pack(side="right", fill="y", padx=15)
        
        self.theme_label = ctk.CTkLabel(self.right_frame, text="主题: 浅色", font=("Microsoft YaHei", 13))
        self.theme_label.pack(side="right", padx=15, pady=8)
        
        self.mode_label = ctk.CTkLabel(self.right_frame, text="模式: Markdown", font=("Microsoft YaHei", 13))
        self.mode_label.pack(side="right", padx=15, pady=8)
        
        self.modified_label = ctk.CTkLabel(self.right_frame, text="", font=("Microsoft YaHei", 13), text_color="#ff6b6b")
        self.modified_label.pack(side="right", padx=15, pady=8)
    
    def update_status(self, line, col, char_count, word_count, file_path, modified, theme):
        self.line_label.configure(text=f"行: {line}")
        self.col_label.configure(text=f"列: {col}")
        self.char_label.configure(text=f"字符: {char_count}")
        self.word_label.configure(text=f"字数: {word_count}")
        
        if file_path:
            display_path = file_path[-60:] if len(file_path) > 60 else file_path
            self.file_label.configure(text=f"文件: {display_path}")
        else:
            self.file_label.configure(text="文件: 未保存")
        
        theme_text = "深色" if theme == "dark" else "浅色"
        self.theme_label.configure(text=f"主题: {theme_text}")
        
        self.update_modified(modified)
    
    def update_modified(self, modified):
        if modified:
            self.modified_label.configure(text="*已修改")
        else:
            self.modified_label.configure(text="")
    
    def refresh_theme(self):
        theme = "dark" if ctk.get_appearance_mode() == "dark" else "light"
        theme_text = "深色" if theme == "dark" else "浅色"
        self.theme_label.configure(text=f"主题: {theme_text}")