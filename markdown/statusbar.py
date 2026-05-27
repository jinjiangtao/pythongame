import customtkinter as ctk

class StatusBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=8, height=30)
        
        self.create_widgets()
    
    def create_widgets(self):
        self.line_label = ctk.CTkLabel(self, text="行: 1", font=("Arial", 12))
        self.line_label.pack(side="left", padx=15, pady=5)
        
        self.col_label = ctk.CTkLabel(self, text="列: 0", font=("Arial", 12))
        self.col_label.pack(side="left", padx=15, pady=5)
        
        self.char_label = ctk.CTkLabel(self, text="字符: 0", font=("Arial", 12))
        self.char_label.pack(side="left", padx=15, pady=5)
        
        self.word_label = ctk.CTkLabel(self, text="字数: 0", font=("Arial", 12))
        self.word_label.pack(side="left", padx=15, pady=5)
        
        self.file_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.file_label.pack(side="left", padx=15, pady=5)
        
        self.modified_label = ctk.CTkLabel(self, text="", font=("Arial", 12), text_color="red")
        self.modified_label.pack(side="right", padx=15, pady=5)
    
    def update_status(self, line, col, char_count, word_count, file_path, modified):
        self.line_label.configure(text=f"行: {line}")
        self.col_label.configure(text=f"列: {col}")
        self.char_label.configure(text=f"字符: {char_count}")
        self.word_label.configure(text=f"字数: {word_count}")
        
        if file_path:
            display_path = file_path[-50:] if len(file_path) > 50 else file_path
            self.file_label.configure(text=f"文件: {display_path}")
        else:
            self.file_label.configure(text="文件: 未保存")
        
        self.update_modified(modified)
    
    def update_modified(self, modified):
        if modified:
            self.modified_label.configure(text="*已修改")
        else:
            self.modified_label.configure(text="")