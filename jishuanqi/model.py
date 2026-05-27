import math


class CalculatorModel:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current_value = "0"
        self.history = ""
        self.operator = None
        self.last_operation = None
        self.is_new_operation = True

    def append_number(self, num):
        if self.is_new_operation:
            self.current_value = num
            self.is_new_operation = False
        else:
            if len(self.current_value) >= 15:
                return False
            self.current_value += num
        return True

    def append_decimal(self):
        if self.is_new_operation:
            self.current_value = "0."
            self.is_new_operation = False
        elif "." not in self.current_value:
            if len(self.current_value) >= 14:
                return False
            self.current_value += "."
        return True

    def set_operator(self, op):
        if self.operator is None and self.history == "":
            self.history = self.current_value
        elif not self.is_new_operation:
            result = self.calculate()
            if result and result[0]:
                self.history = self.current_value
            else:
                self.history = self.current_value

        self.operator = op
        self.is_new_operation = True
        self.last_operation = "operator"
        return True

    def calculate(self):
        if self.operator is None or self.history == "":
            return (True, "")

        try:
            num1 = float(self.history)
            num2 = float(self.current_value)

            if self.operator == "+":
                result = num1 + num2
            elif self.operator == "-":
                result = num1 - num2
            elif self.operator == "×":
                result = num1 * num2
            elif self.operator == "÷":
                if num2 == 0:
                    return (False, "除数不能为零")
                result = num1 / num2
            else:
                return (False, "无效运算符")

            self.history = ""
            self.operator = None

            if result == math.floor(result) and result == int(result):
                self.current_value = str(int(result))
            else:
                result_str = str(result)
                if len(result_str) > 15:
                    result_str = "{:.10e}".format(result)
                else:
                    result_str = "{:.10f}".format(result).rstrip("0").rstrip(".")
                self.current_value = result_str

            self.is_new_operation = True
            self.last_operation = "calculate"
            return (True, "")

        except Exception as e:
            return (False, str(e))

    def toggle_sign(self):
        if self.current_value != "0":
            if self.current_value.startswith("-"):
                self.current_value = self.current_value[1:]
            else:
                self.current_value = "-" + self.current_value
        return True

    def percentage(self):
        try:
            value = float(self.current_value)
            value = value / 100
            self.current_value = str(value)
            return True
        except:
            return False

    def delete_char(self):
        if self.is_new_operation:
            return False
        if len(self.current_value) > 1:
            self.current_value = self.current_value[:-1]
        else:
            self.current_value = "0"
            self.is_new_operation = True
        return True