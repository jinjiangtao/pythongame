import customtkinter as ctk

class NumberButtons(ctk.CTkFrame):
    """数字按钮组件 - 包含数字选择按钮、提交、下一题、重新开始按钮"""
    
    def __init__(self, master):
        super().__init__(master, corner_radius=15)
        self.selected_number = None
        self.number_buttons = []
        self._create_widgets()
    
    def _create_widgets(self):
        """创建数字按钮区域"""
        self.number_frame = ctk.CTkFrame(self, corner_radius=10)
        self.number_frame.pack(fill="x", pady=10)
        
        self.action_frame = ctk.CTkFrame(self, corner_radius=10)
        self.action_frame.pack(fill="x", pady=5)
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_columnconfigure(1, weight=1)
        self.action_frame.grid_columnconfigure(2, weight=1)
        
        self.submit_btn = ctk.CTkButton(
            self.action_frame,
            text="确定答案",
            font=("Microsoft YaHei", 16, "bold"),
            fg_color="#4ECDC4",
            hover_color="#44A399",
            corner_radius=10,
            command=self._on_submit
        )
        self.submit_btn.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
        self.submit_btn.configure(state="disabled")
        
        self.next_btn = ctk.CTkButton(
            self.action_frame,
            text="下一题",
            font=("Microsoft YaHei", 16, "bold"),
            fg_color="#45B7D1",
            hover_color="#3A9DBF",
            corner_radius=10,
            command=self._on_next
        )
        self.next_btn.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        self.next_btn.configure(state="disabled")
        
        self.restart_btn = ctk.CTkButton(
            self.action_frame,
            text="重新开始",
            font=("Microsoft YaHei", 16, "bold"),
            fg_color="#FF6B6B",
            hover_color="#E55555",
            corner_radius=10,
            command=self._on_restart
        )
        self.restart_btn.grid(row=0, column=2, padx=8, pady=8, sticky="ew")
        
        self.click_callback = None
        self.submit_callback = None
        self.next_callback = None
        self.restart_callback = None
    
    def set_range(self, min_num: int, max_num: int):
        """设置数字按钮范围"""
        # 清除现有按钮
        for btn in self.number_buttons:
            btn.destroy()
        self.number_buttons.clear()
        
        total = max_num - min_num + 1
        cols = min(total, 5)
        
        for i in range(total):
            num = min_num + i
            btn = ctk.CTkButton(
                self.number_frame,
                text=str(num),
                font=("Microsoft YaHei", 24, "bold"),
                width=80,
                height=60,
                corner_radius=15,
                fg_color="#96CEB4",
                hover_color="#85BB9E",
                command=lambda n=num: self._on_number_click(n)
            )
            row = i // cols
            col = i % cols
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.number_buttons.append(btn)
    
    def _on_number_click(self, number: int):
        """数字按钮点击事件"""
        self.selected_number = number
        
        for btn in self.number_buttons:
            if int(btn.cget("text")) == number:
                btn.configure(fg_color="#FFEAA7", hover_color="#F0D878")
            else:
                btn.configure(fg_color="#96CEB4", hover_color="#85BB9E")
        
        if self.click_callback:
            self.click_callback(number)
        
        self.submit_btn.configure(state="normal")
    
    def _on_submit(self):
        """提交按钮点击事件"""
        if self.submit_callback and self.selected_number is not None:
            self.submit_callback(self.selected_number)
    
    def _on_next(self):
        """下一题按钮点击事件"""
        if self.next_callback:
            self.next_callback()
    
    def _on_restart(self):
        """重新开始按钮点击事件"""
        if self.restart_callback:
            self.restart_callback()
    
    def bind_click(self, callback):
        """绑定数字按钮点击回调"""
        self.click_callback = callback
    
    def bind_submit(self, callback):
        """绑定提交按钮回调"""
        self.submit_callback = callback
    
    def bind_next(self, callback):
        """绑定下一题按钮回调"""
        self.next_callback = callback
    
    def bind_restart(self, callback):
        """绑定重新开始按钮回调"""
        self.restart_callback = callback
    
    def select(self, number: int):
        """选中指定数字"""
        for btn in self.number_buttons:
            if int(btn.cget("text")) == number:
                btn.invoke()
                break
    
    def clear_selection(self):
        """清除数字选择状态"""
        self.selected_number = None
        for btn in self.number_buttons:
            btn.configure(fg_color="#96CEB4", hover_color="#85BB9E")
        self.submit_btn.configure(state="disabled")
    
    def enable_submit(self, enable: bool):
        """启用/禁用提交按钮"""
        self.submit_btn.configure(state="normal" if enable else "disabled")
    
    def enable_next(self, enable: bool):
        """启用/禁用下一题按钮"""
        self.next_btn.configure(state="normal" if enable else "disabled")