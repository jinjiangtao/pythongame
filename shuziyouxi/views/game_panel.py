import customtkinter as ctk

class GamePanel(ctk.CTkCanvas):
    """游戏面板组件 - 显示图案的画布区域"""
    
    def __init__(self, master):
        super().__init__(master, bg="transparent", highlightthickness=0)
        self.pattern_size = 50
        self.pattern_labels = []
    
    def display_patterns(self, pattern: str, positions: list):
        """在面板上显示图案"""
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
    
    def clear(self):
        """清空面板上的所有图案"""
        for label in self.pattern_labels:
            label.destroy()
        self.pattern_labels.clear()
    
    def get_size(self):
        """获取面板尺寸"""
        return (self.winfo_width(), self.winfo_height())