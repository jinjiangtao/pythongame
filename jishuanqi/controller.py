from model import CalculatorModel


class CalculatorController:
    """计算器控制器层 - 协调视图和模型，处理用户输入"""

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def handle_number(self, num):
        """处理数字输入"""
        success = self.model.append_number(num)
        if success:
            self.update_display()

    def handle_decimal(self):
        """处理小数点输入"""
        success = self.model.append_decimal()
        if success:
            self.update_display()

    def handle_operator(self, op):
        """处理运算符输入"""
        if self.model.operator in ["^", "∜"]:
            result = self.model.apply_scientific_operator()
            if result is None:
                return
            success, message = result
            if success:
                self.update_display()
            else:
                self.view.show_error(message)
                self.model.reset()
                self.update_display()
                return

        success = self.model.set_operator(op)
        if success:
            self.update_display()

    def handle_equals(self):
        """处理等号输入"""
        if self.model.operator in ["^", "∜"]:
            result = self.model.apply_scientific_operator()
            if result is None:
                return
            success, message = result
            if success:
                self.update_display()
            else:
                self.view.show_error(message)
                self.model.reset()
                self.update_display()
            return

        result = self.model.calculate()
        if result is None:
            return
        success, message = result
        if success:
            self.update_display()
        else:
            self.view.show_error(message)
            self.model.reset()
            self.update_display()

    def handle_clear(self):
        """处理清空全部"""
        self.model.reset()
        self.update_display()

    def handle_clear_entry(self):
        """处理清除当前输入"""
        self.model.clear_entry()
        self.update_display()

    def handle_toggle_sign(self):
        """处理正负号切换"""
        success = self.model.toggle_sign()
        if success:
            self.update_display()

    def handle_percentage(self):
        """处理百分比计算"""
        success = self.model.percentage()
        if success:
            self.update_display()

    def handle_delete(self):
        """处理删除最后一个字符"""
        success = self.model.delete_char()
        if success:
            self.update_display()

    def handle_scientific_function(self, func_name):
        """处理科学计算函数"""
        result = self.model.apply_scientific_function(func_name)
        if result is None:
            return

        success, message = result
        if success:
            self.update_display()
        else:
            self.view.show_error(message)
            self.model.reset()
            self.update_display()

    def update_display(self):
        """更新显示内容"""
        history_text = ""
        if self.model.history != "":
            history_text = self.model.history
            if self.model.operator:
                history_text = f"{history_text} {self.model.operator}"

        self.view.update_display(history_text, self.model.current_value)
