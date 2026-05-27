from model import CalculatorModel


class CalculatorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def handle_number(self, num):
        success = self.model.append_number(num)
        if success:
            self.update_display()

    def handle_decimal(self):
        success = self.model.append_decimal()
        if success:
            self.update_display()

    def handle_operator(self, op):
        success = self.model.set_operator(op)
        if success:
            self.update_display()

    def handle_equals(self):
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
        self.model.reset()
        self.update_display()

    def handle_toggle_sign(self):
        success = self.model.toggle_sign()
        if success:
            self.update_display()

    def handle_percentage(self):
        success = self.model.percentage()
        if success:
            self.update_display()

    def handle_delete(self):
        success = self.model.delete_char()
        if success:
            self.update_display()

    def update_display(self):
        history_text = ""
        if self.model.history != "" and self.model.operator is not None:
            history_text = f"{self.model.history} {self.model.operator}"
        self.view.update_display(history_text, self.model.current_value)