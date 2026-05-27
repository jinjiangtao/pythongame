import customtkinter as ctk


class CalculatorDisplay(ctk.CTkFrame):
    """显示屏组件 - 显示历史记录和当前结果"""

    def __init__(self, parent):
        super().__init__(parent, corner_radius=12)
        self.configure(fg_color="transparent")

        self.history_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=16, weight="normal"),
            anchor="e",
            height=30
        )
        self.history_label.pack(side="top", fill="x", padx=20, pady=(10, 0), anchor="e")

        self.result_label = ctk.CTkLabel(
            self,
            text="0",
            font=ctk.CTkFont(size=48, weight="bold"),
            anchor="e",
            height=60
        )
        self.result_label.pack(side="bottom", fill="x", padx=20, pady=(5, 15), anchor="e")

    def update_history(self, text):
        """更新历史记录显示"""
        self.history_label.configure(text=text)

    def update_result(self, text):
        """更新当前结果显示"""
        if len(text) > 12:
            font_size = 36
        elif len(text) > 9:
            font_size = 42
        else:
            font_size = 48
        self.result_label.configure(text=text, font=ctk.CTkFont(size=font_size, weight="bold"))

    def update_colors(self, is_dark):
        """更新颜色主题"""
        if is_dark:
            self.history_label.configure(text_color="#8b8b8b")
            self.result_label.configure(text_color="#ffffff")
        else:
            self.history_label.configure(text_color="#6b6b6b")
            self.result_label.configure(text_color="#1a1a1a")


class CalculatorButton(ctk.CTkButton):
    """计算器按钮组件 - 支持多种按钮类型"""

    def __init__(self, parent, text, command, button_type="number", width=70, height=50):
        super().__init__(parent, text=text, command=command)
        self.button_type = button_type

        self.configure(
            corner_radius=8,
            font=ctk.CTkFont(size=16, weight="bold"),
            border_width=0,
            height=height,
            width=width
        )
        self.update_colors(is_dark=True)

    def update_colors(self, is_dark):
        """更新按钮颜色"""
        fg_color = self._get_fg_color(is_dark)
        hover_color = self._get_hover_color(is_dark)
        text_color = self._get_text_color(is_dark)

        self.configure(
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=text_color
        )

    def _get_fg_color(self, is_dark):
        """获取前景色"""
        colors = {
            "number": "#3a3a3a" if is_dark else "#e0e0e0",
            "operator": "#ff9500",
            "function": "#6b6b6b" if is_dark else "#d0d0d0",
            "scientific": "#505050" if is_dark else "#c8c8c8",
            "equals": "#ff6b35"
        }
        return colors.get(self.button_type, colors["number"])

    def _get_hover_color(self, is_dark):
        """获取悬停颜色"""
        colors = {
            "number": "#4a4a4a" if is_dark else "#c0c0c0",
            "operator": "#ffad40",
            "function": "#7b7b7b" if is_dark else "#b8b8b8",
            "scientific": "#606060" if is_dark else "#d8d8d8",
            "equals": "#ff8a5c"
        }
        return colors.get(self.button_type, colors["number"])

    def _get_text_color(self, is_dark):
        """获取文本颜色"""
        if self.button_type in ["equals", "operator"]:
            return "#ffffff"
        return "#ffffff" if is_dark else "#333333"


class ScientificButtons(ctk.CTkFrame):
    """科学计算按键区域 - 包含三角函数、对数、指数等按钮"""

    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=8)
        self.configure(fg_color="transparent")
        self.controller = controller
        self.button_list = []

        self.create_scientific_buttons()

    def create_scientific_buttons(self):
        """创建科学计算按钮"""
        buttons = [
            ("sin", "scientific"), ("cos", "scientific"), ("tan", "scientific"), ("log", "scientific"),
            ("ln", "scientific"), ("√", "scientific"), ("x²", "scientific"), ("x³", "scientific"),
            ("xʸ", "scientific"), ("∜", "scientific"), ("π", "scientific"), ("e", "scientific"),
            ("n!", "scientific"), ("1/x", "scientific"), ("|x|", "scientific"), ("CE", "function")
        ]

        for i, (text, button_type) in enumerate(buttons):
            row = i // 4
            col = i % 4

            btn = CalculatorButton(
                self, text,
                self.make_command(text),
                button_type,
                width=55,
                height=40
            )
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
            self.button_list.append(btn)

        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        for i in range(4):
            self.grid_rowconfigure(i, weight=1)

    def update_colors(self, is_dark):
        """更新所有按钮颜色"""
        for btn in self.button_list:
            btn.update_colors(is_dark)

    def make_command(self, text):
        """创建按钮命令"""
        func_map = {
            "sin": lambda: self.controller.handle_scientific_function("sin"),
            "cos": lambda: self.controller.handle_scientific_function("cos"),
            "tan": lambda: self.controller.handle_scientific_function("tan"),
            "log": lambda: self.controller.handle_scientific_function("log"),
            "ln": lambda: self.controller.handle_scientific_function("ln"),
            "√": lambda: self.controller.handle_scientific_function("sqrt"),
            "x²": lambda: self.controller.handle_scientific_function("square"),
            "x³": lambda: self.controller.handle_scientific_function("cube"),
            "xʸ": lambda: self.controller.handle_scientific_function("power"),
            "∜": lambda: self.controller.handle_scientific_function("cbrt_root"),
            "π": lambda: self.controller.handle_scientific_function("pi"),
            "e": lambda: self.controller.handle_scientific_function("e"),
            "n!": lambda: self.controller.handle_scientific_function("factorial"),
            "1/x": lambda: self.controller.handle_scientific_function("inverse"),
            "|x|": lambda: self.controller.handle_scientific_function("abs"),
            "CE": lambda: self.controller.handle_clear_entry()
        }
        return func_map.get(text, lambda: None)


class StandardButtons(ctk.CTkFrame):
    """标准计算按键区域 - 包含数字和基本运算符"""

    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=8)
        self.configure(fg_color="transparent")
        self.controller = controller
        self.button_list = []

        self.create_standard_buttons()

    def create_standard_buttons(self):
        """创建标准计算按钮"""
        buttons = [
            ("C", "function"), ("±", "function"), ("⌫", "function"), ("÷", "operator"),
            ("7", "number"), ("8", "number"), ("9", "number"), ("×", "operator"),
            ("4", "number"), ("5", "number"), ("6", "number"), ("-", "operator"),
            ("1", "number"), ("2", "number"), ("3", "number"), ("+", "operator"),
            ("0", "number"), (".", "number"), ("=", "equals")
        ]

        for i, (text, button_type) in enumerate(buttons):
            row = i // 4
            col = i % 4

            if text == "0":
                btn = CalculatorButton(
                    self, text,
                    self.make_command(text),
                    button_type,
                    width=115,
                    height=50
                )
                btn.grid(row=row, column=col, columnspan=2, padx=3, pady=3, sticky="nsew")
                self.button_list.append(btn)
            elif text == "=":
                btn = CalculatorButton(
                    self, text,
                    self.make_command(text),
                    button_type,
                    width=70,
                    height=105
                )
                btn.grid(row=row, column=col, rowspan=2, padx=3, pady=3, sticky="nsew")
                self.button_list.append(btn)
            else:
                btn = CalculatorButton(
                    self, text,
                    self.make_command(text),
                    button_type,
                    width=70,
                    height=50
                )
                btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
                self.button_list.append(btn)

        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)

    def update_colors(self, is_dark):
        """更新所有按钮颜色"""
        for btn in self.button_list:
            btn.update_colors(is_dark)

    def make_command(self, text):
        """创建按钮命令"""
        if text == "C":
            return lambda: self.controller.handle_clear()
        elif text == "⌫":
            return lambda: self.controller.handle_delete()
        elif text == "±":
            return lambda: self.controller.handle_toggle_sign()
        elif text == "=":
            return lambda: self.controller.handle_equals()
        elif text in ["+", "-", "×", "÷"]:
            return lambda: self.controller.handle_operator(text)
        elif text == ".":
            return lambda: self.controller.handle_decimal()
        else:
            return lambda: self.controller.handle_number(text)


class CalculatorView(ctk.CTk):
    """计算器主窗口视图"""

    def __init__(self):
        super().__init__()
        self.title("科学计算器 V2.0")
        self.geometry("420x680")
        self.resizable(False, False)

        self.center_window()

        self.title_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.title_frame.pack(fill="x", padx=20, pady=(15, 5))

        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="科学计算器 V2.0",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(side="left")

        self.theme_switch = ctk.CTkSwitch(
            self.title_frame,
            text="深色模式",
            font=ctk.CTkFont(size=12),
            command=self.toggle_theme
        )
        self.theme_switch.pack(side="right")
        self.theme_switch.select()

        self.display = CalculatorDisplay(self)
        self.display.pack(fill="x", padx=15, pady=5)

        self.scientific_frame = ctk.CTkFrame(self)
        self.scientific_frame.pack(fill="x", padx=15, pady=5)

        self.scientific_buttons = None

        self.standard_frame = ctk.CTkFrame(self)
        self.standard_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        self.standard_buttons = None

        self.bind('<Key>', self.handle_key_press)

        self.update_ui_colors(is_dark=True)

    def center_window(self):
        """窗口居中显示"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def set_controller(self, controller):
        """设置控制器"""
        self.controller = controller
        self.scientific_buttons = ScientificButtons(self.scientific_frame, controller)
        self.scientific_buttons.pack(fill="both", expand=True, padx=5, pady=5)

        self.standard_buttons = StandardButtons(self.standard_frame, controller)
        self.standard_buttons.pack(fill="both", expand=True, padx=5, pady=5)

    def toggle_theme(self):
        """切换主题"""
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
            self.theme_switch.configure(text="深色模式")
            self.update_ui_colors(is_dark=True)
        else:
            ctk.set_appearance_mode("light")
            self.theme_switch.configure(text="浅色模式")
            self.update_ui_colors(is_dark=False)

    def update_ui_colors(self, is_dark):
        """更新界面颜色"""
        if is_dark:
            self.configure(fg_color="#1a1a1a")
            self.title_label.configure(text_color="#ffffff")
            self.theme_switch.configure(text_color="#ffffff")
            self.scientific_frame.configure(fg_color="#1a1a1a")
            self.standard_frame.configure(fg_color="#1a1a1a")
        else:
            self.configure(fg_color="#f0f0f0")
            self.title_label.configure(text_color="#1a1a1a")
            self.theme_switch.configure(text_color="#1a1a1a")
            self.scientific_frame.configure(fg_color="#f0f0f0")
            self.standard_frame.configure(fg_color="#f0f0f0")

        self.display.update_colors(is_dark)
        if self.scientific_buttons:
            self.scientific_buttons.update_colors(is_dark)
        if self.standard_buttons:
            self.standard_buttons.update_colors(is_dark)

    def update_display(self, history_text, result_text):
        """更新显示内容"""
        self.display.update_history(history_text)
        self.display.update_result(result_text)

    def show_error(self, message):
        """显示错误对话框"""
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("错误")
        error_dialog.geometry("300x150")
        error_dialog.resizable(False, False)
        error_dialog.transient(self)
        error_dialog.grab_set()

        label = ctk.CTkLabel(
            error_dialog,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=280
        )
        label.pack(pady=20, padx=10)

        ok_button = ctk.CTkButton(error_dialog, text="确定", command=error_dialog.destroy)
        ok_button.pack(pady=10)

    def handle_key_press(self, event):
        """处理键盘输入"""
        key = event.char
        if key in "0123456789":
            self.controller.handle_number(key)
        elif key == ".":
            self.controller.handle_decimal()
        elif key in "+-*/":
            op_map = {"+": "+", "-": "-", "*": "×", "/": "÷"}
            self.controller.handle_operator(op_map.get(key, key))
        elif key == "=" or key == "\r":
            self.controller.handle_equals()
        elif key == "c" or key == "C":
            self.controller.handle_clear()
        elif key == "\b":
            self.controller.handle_delete()
        elif key == "%":
            self.controller.handle_scientific_function("percent")
