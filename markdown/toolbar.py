import customtkinter as ctk

class Toolbar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=8)
        
        self.callbacks = {}
        
        self.create_buttons()
    
    def create_buttons(self):
        buttons = [
            ("新建", "new", "新建文档"),
            ("打开", "open", "打开文件"),
            ("保存", "save", "保存文档"),
            ("导出", "export", "导出HTML"),
            ("清空", "clear", "清空内容"),
            ("主题", "theme", "切换主题")
        ]
        
        for text, key, tooltip in buttons:
            button = ctk.CTkButton(
                self,
                text=text,
                width=60,
                height=30,
                command=lambda k=key: self.on_button_click(k)
            )
            button.pack(side="left", padx=5, pady=5)
            button.bind("<Enter>", lambda e, t=tooltip: self.show_tooltip(e, t))
            button.bind("<Leave>", self.hide_tooltip)
    
    def set_callback(self, key, callback):
        self.callbacks[key] = callback
    
    def on_button_click(self, key):
        if key in self.callbacks:
            self.callbacks[key]()
    
    def show_tooltip(self, event, text):
        self.tooltip = ctk.CTkLabel(self, text=text, fg_color="gray80", text_color="white", corner_radius=4, padx=8, pady=4)
        x = event.widget.winfo_rootx() + event.widget.winfo_width() // 2 - self.tooltip.winfo_reqwidth() // 2
        y = event.widget.winfo_rooty() - self.tooltip.winfo_reqheight() - 10
        self.tooltip.place(x=x, y=y)
    
    def hide_tooltip(self, event):
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()