import customtkinter as ctk

class Header(ctk.CTkFrame):
    """头部组件 - 显示游戏标题、关卡信息、正确率、主题切换"""
    
    def __init__(self, master):
        super().__init__(master, corner_radius=15)
        self._create_widgets()
    
    def _create_widgets(self):
        """创建头部组件"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0)
        
        self.title_label = ctk.CTkLabel(
            self, 
            text="🔢 数字数数游戏", 
            font=("Microsoft YaHei", 20, "bold"),
            text_color="#FF6B6B"
        )
        self.title_label.grid(row=0, column=0, columnspan=4, pady=10)
        
        self.level_label = ctk.CTkLabel(
            self, 
            text="第 1 关", 
            font=("Microsoft YaHei", 16, "bold"),
            text_color="#4ECDC4"
        )
        self.level_label.grid(row=1, column=0, padx=10, pady=5)
        
        self.level_name_label = ctk.CTkLabel(
            self, 
            text="入门级", 
            font=("Microsoft YaHei", 14),
            text_color="#6C757D"
        )
        self.level_name_label.grid(row=2, column=0, padx=10, pady=0)
        
        self.progress_label = ctk.CTkLabel(
            self, 
            text="进度: 0/5", 
            font=("Microsoft YaHei", 16, "bold"),
            text_color="#45B7D1"
        )
        self.progress_label.grid(row=1, column=1, padx=10, pady=5)
        
        self.hint_label = ctk.CTkLabel(
            self, 
            text="数一数有几个图案", 
            font=("Microsoft YaHei", 12),
            text_color="#6C757D"
        )
        self.hint_label.grid(row=2, column=1, padx=10, pady=0)
        
        self.accuracy_label = ctk.CTkLabel(
            self, 
            text="正确率: 0%", 
            font=("Microsoft YaHei", 16, "bold"),
            text_color="#96CEB4"
        )
        self.accuracy_label.grid(row=1, column=2, padx=10, pady=5)
        
        self.theme_switch = ctk.CTkSwitch(
            self, 
            text="深色", 
            font=("Microsoft YaHei", 12),
            command=self._on_theme_switch
        )
        self.theme_switch.grid(row=1, column=3, rowspan=2, padx=10, pady=5)
        
        self.theme_callback = None
    
    def set_info(self, level: int, level_name: str, progress: str, accuracy: float):
        """更新头部信息"""
        self.level_label.configure(text=f"第 {level} 关")
        self.level_name_label.configure(text=level_name)
        self.progress_label.configure(text=f"进度: {progress}")
        self.accuracy_label.configure(text=f"正确率: {accuracy}%")
    
    def bind_theme_switch(self, callback):
        """绑定主题切换回调"""
        self.theme_callback = callback
    
    def _on_theme_switch(self):
        """主题切换事件处理"""
        if self.theme_callback:
            self.theme_callback()
    
    def set_theme_switch_state(self, is_dark: bool):
        """设置主题开关状态"""
        self.theme_switch.select() if is_dark else self.theme_switch.deselect()