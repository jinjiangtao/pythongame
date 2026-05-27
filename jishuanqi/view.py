import customtkinter as ctk


class CalculatorDisplay(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=12)
        self.configure(fg_color="transparent")

        self.history_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=16, weight="normal"),
            anchor="e"
        )
        self.history_label.pack(side="top", fill="x", padx=20, pady=(10, 0), anchor="e")

        self.result_label = ctk.CTkLabel(
            self,
            text="0",
            font=ctk.CTkFont(size=42, weight="bold"),
            anchor="e"
        )
        self.result_label.pack(side="bottom", fill="x", padx=20, pady=(5, 15), anchor="e")

    def update_history(self, text):
        self.history_label.configure(text=text)

    def update_result(self, text):
        self.result_label.configure(text=text)

    def update_colors(self, is_dark):
        if is_dark:
            self.history_label.configure(text_color="#8b8b8b")
            self.result_label.configure(text_color="#ffffff")
        else:
            self.history_label.configure(text_color="#6b6b6b")
            self.result_label.configure(text_color="#1a1a1a")


class CalculatorButton(ctk.CTkButton):
    def __init__(self, parent, text, command, button_type="number"):
        super().__init__(parent, text=text, command=command)
        self.button_type = button_type
        
        self.configure(
            corner_radius=12,
            font=ctk.CTkFont(size=20, weight="bold"),
            border_width=0,
            height=60,
            width=70
        )
        self.update_colors(is_dark=True)

    def update_colors(self, is_dark):
        fg_color = self._get_fg_color(is_dark)
        hover_color = self._get_hover_color(is_dark)
        text_color = self._get_text_color(is_dark)
        
        self.configure(
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=text_color
        )

    def _get_fg_color(self, is_dark):
        if is_dark:
            colors = {
                "number": "#3a3a3a",
                "operator": "#ff9500",
                "function": "#6b6b6b",
                "equals": "#ff6b35"
            }
        else:
            colors = {
                "number": "#e0e0e0",
                "operator": "#ffb347",
                "function": "#d0d0d0",
                "equals": "#ff8a5c"
            }
        return colors.get(self.button_type, colors["number"])

    def _get_hover_color(self, is_dark):
        if is_dark:
            colors = {
                "number": "#4a4a4a",
                "operator": "#ffad40",
                "function": "#7b7b7b",
                "equals": "#ff8a5c"
            }
        else:
            colors = {
                "number": "#c0c0c0",
                "operator": "#ffc069",
                "function": "#b8b8b8",
                "equals": "#ffa07a"
            }
        return colors.get(self.button_type, colors["number"])

    def _get_text_color(self, is_dark):
        if self.button_type == "equals":
            return "#ffffff"
        return "#ffffff" if is_dark else "#333333"


class CalculatorButtons(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=12)
        self.configure(fg_color="transparent")
        self.controller = controller
        self.button_list = []

        self.create_buttons()

    def create_buttons(self):
        buttons = [
            ("C", "function"), ("±", "function"), ("%", "function"), ("÷", "operator"),
            ("7", "number"),   ("8", "number"),   ("9", "number"),   ("×", "operator"),
            ("4", "number"),   ("5", "number"),   ("6", "number"),   ("-", "operator"),
            ("1", "number"),   ("2", "number"),   ("3", "number"),   ("+", "operator"),
            ("0", "number"),   (".", "number"),   ("=", "equals")
        ]

        for i, (text, button_type) in enumerate(buttons):
            row = i // 4
            col = i % 4

            if text == "0":
                btn = CalculatorButton(self, text, self.make_command(text), button_type)
                btn.grid(row=row, column=col, columnspan=2, padx=5, pady=5, sticky="nsew")
                btn.configure(width=150)
                self.button_list.append(btn)
            elif text == "=":
                btn = CalculatorButton(self, text, self.make_command(text), button_type)
                btn.grid(row=row, column=col, rowspan=2, padx=5, pady=5, sticky="nsew")
                btn.configure(height=130)
                self.button_list.append(btn)
            else:
                btn = CalculatorButton(self, text, self.make_command(text), button_type)
                btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                self.button_list.append(btn)

        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)

    def update_colors(self, is_dark):
        for btn in self.button_list:
            btn.update_colors(is_dark)

    def make_command(self, text):
        if text == "C":
            return lambda: self.controller.handle_clear()
        elif text == "±":
            return lambda: self.controller.handle_toggle_sign()
        elif text == "%":
            return lambda: self.controller.handle_percentage()
        elif text == "=":
            return lambda: self.controller.handle_equals()
        elif text in ["+", "-", "×", "÷"]:
            return lambda: self.controller.handle_operator(text)
        elif text == ".":
            return lambda: self.controller.handle_decimal()
        else:
            return lambda: self.controller.handle_number(text)


class CalculatorView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("计算器")
        self.geometry("320x480")
        self.resizable(False, False)

        self.center_window()

        self.display = CalculatorDisplay(self)
        self.display.pack(fill="x", padx=15, pady=10)

        self.title_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.title_frame.pack(fill="x", padx=20, pady=15)

        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="计算器",
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

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.buttons = None

        self.bind('<Key>', self.handle_key_press)

        self.update_ui_colors(is_dark=True)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def set_controller(self, controller):
        self.controller = controller
        self.buttons = CalculatorButtons(self.buttons_frame, controller)
        self.buttons.pack(fill="both", expand=True, padx=5, pady=5)

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
            self.theme_switch.configure(text="深色模式")
            self.update_ui_colors(is_dark=True)
        else:
            ctk.set_appearance_mode("light")
            self.theme_switch.configure(text="浅色模式")
            self.update_ui_colors(is_dark=False)

    def update_ui_colors(self, is_dark):
        if is_dark:
            self.configure(fg_color="#1a1a1a")
            self.title_label.configure(text_color="#ffffff")
            self.theme_switch.configure(text_color="#ffffff")
            self.buttons_frame.configure(fg_color="#1a1a1a")
        else:
            self.configure(fg_color="#f5f5f5")
            self.title_label.configure(text_color="#1a1a1a")
            self.theme_switch.configure(text_color="#1a1a1a")
            self.buttons_frame.configure(fg_color="#f5f5f5")
        
        self.display.update_colors(is_dark)
        if self.buttons:
            self.buttons.update_colors(is_dark)

    def update_display(self, history_text, result_text):
        self.display.update_history(history_text)
        self.display.update_result(result_text)

    def show_error(self, message):
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("错误")
        error_dialog.geometry("250x120")
        error_dialog.resizable(False, False)
        error_dialog.transient(self)
        error_dialog.grab_set()

        label = ctk.CTkLabel(error_dialog, text=message, font=ctk.CTkFont(size=14))
        label.pack(pady=20)

        ok_button = ctk.CTkButton(error_dialog, text="确定", command=error_dialog.destroy)
        ok_button.pack(pady=10)

    def handle_key_press(self, event):
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
            self.controller.handle_percentage()