import customtkinter as ctk

class StatusBar(ctk.CTkFrame):
    """状态栏组件 - 显示操作引导和答题反馈"""
    
    def __init__(self, master):
        super().__init__(master, corner_radius=15)
        self._create_widgets()
    
    def _create_widgets(self):
        """创建状态栏组件"""
        self.guide_label = ctk.CTkLabel(
            self,
            text="请点击上方数字按钮选择答案",
            font=("Microsoft YaHei", 14),
            text_color="#6C757D"
        )
        self.guide_label.pack(pady=5)
        
        self.feedback_label = ctk.CTkLabel(
            self,
            text="",
            font=("Microsoft YaHei", 16, "bold")
        )
        self.feedback_label.pack(pady=5)
    
    def set_text(self, text: str, is_success: bool = None):
        """设置引导文字"""
        self.guide_label.configure(text=text)
        if is_success is not None:
            color = "#27AE60" if is_success else "#E74C3C"
            self.guide_label.configure(text_color=color)
        else:
            self.guide_label.configure(text_color="#6C757D")
    
    def set_feedback(self, text: str, is_success: bool):
        """设置答题反馈"""
        color = "#27AE60" if is_success else "#E74C3C"
        self.feedback_label.configure(text=text, text_color=color)