import math


class CalculatorModel:
    """计算器模型层 - 处理所有数学运算和状态管理"""

    def __init__(self):
        self.reset()

    def reset(self):
        """重置计算器状态"""
        self.current_value = "0"
        self.history = ""
        self.operator = None
        self.last_operation = None
        self.is_new_operation = True

    def append_number(self, num):
        """追加数字到当前输入值"""
        if self.is_new_operation:
            self.current_value = num
            self.is_new_operation = False
        else:
            if len(self.current_value) >= 15:
                return False
            self.current_value += num
        return True

    def append_decimal(self):
        """添加小数点"""
        if self.is_new_operation:
            self.current_value = "0."
            self.is_new_operation = False
        elif "." not in self.current_value:
            if len(self.current_value) >= 14:
                return False
            self.current_value += "."
        return True

    def set_operator(self, op):
        """设置运算符"""
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
        """执行基本算术运算"""
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
                    return (False, "错误：除数不能为零")
                result = num1 / num2
            else:
                return (False, "错误：无效运算符")

            self.history = ""
            self.operator = None
            self.current_value = self._format_result(result)
            self.is_new_operation = True
            self.last_operation = "calculate"
            return (True, "")

        except Exception as e:
            return (False, f"错误：计算异常 - {str(e)}")

    def _format_result(self, result):
        """格式化计算结果"""
        if result == math.floor(result) and result == int(result):
            return str(int(result))
        else:
            result_str = str(result)
            if len(result_str) > 15:
                result_str = "{:.10e}".format(result)
            else:
                result_str = "{:.10f}".format(result).rstrip("0").rstrip(".")
            return result_str

    def toggle_sign(self):
        """切换正负号"""
        if self.current_value != "0":
            if self.current_value.startswith("-"):
                self.current_value = self.current_value[1:]
            else:
                self.current_value = "-" + self.current_value
        return True

    def percentage(self):
        """百分比计算"""
        try:
            value = float(self.current_value)
            value = value / 100
            self.current_value = self._format_result(value)
            return True
        except:
            return False

    def delete_char(self):
        """删除最后一个字符"""
        if self.is_new_operation:
            return False
        if len(self.current_value) > 1:
            self.current_value = self.current_value[:-1]
        else:
            self.current_value = "0"
            self.is_new_operation = True
        return True

    def clear_entry(self):
        """清除当前输入"""
        self.current_value = "0"
        self.is_new_operation = True
        return True

    def apply_scientific_function(self, func_name):
        """应用科学计算函数"""
        try:
            if self.current_value == "":
                return (False, "错误：没有输入值")

            value = float(self.current_value)

            if func_name == "sin":
                result = math.sin(math.radians(value))
            elif func_name == "cos":
                result = math.cos(math.radians(value))
            elif func_name == "tan":
                result = math.tan(math.radians(value))
            elif func_name == "log":
                if value <= 0:
                    return (False, "错误：对数函数需要正数")
                result = math.log10(value)
            elif func_name == "ln":
                if value <= 0:
                    return (False, "错误：自然对数需要正数")
                result = math.log(value)
            elif func_name == "sqrt":
                if value < 0:
                    return (False, "错误：平方根需要非负数")
                result = math.sqrt(value)
            elif func_name == "cbrt":
                result = math.copysign(abs(value) ** (1/3), value)
            elif func_name == "square":
                result = value ** 2
            elif func_name == "cube":
                result = value ** 3
            elif func_name == "power":
                self.history = self.current_value
                self.operator = "^"
                self.is_new_operation = True
                return (True, "")
            elif func_name == "cbrt_root":
                self.history = self.current_value
                self.operator = "∜"
                self.is_new_operation = True
                return (True, "")
            elif func_name == "pi":
                self.current_value = str(math.pi)
                return (True, "")
            elif func_name == "e":
                self.current_value = str(math.e)
                return (True, "")
            elif func_name == "factorial":
                if value < 0 or not float(value).is_integer():
                    return (False, "错误：阶乘需要非负整数")
                result = math.factorial(int(value))
            elif func_name == "abs":
                result = abs(value)
            elif func_name == "inverse":
                if value == 0:
                    return (False, "错误：零没有倒数")
                result = 1 / value
            elif func_name == "percent":
                result = value / 100
            elif func_name == "degrees":
                result = math.degrees(value)
            elif func_name == "radians":
                result = math.radians(value)
            else:
                return (False, f"错误：未知函数 {func_name}")

            self.current_value = self._format_result(result)
            self.is_new_operation = True
            return (True, "")

        except ValueError as ve:
            return (False, f"错误：数值格式错误 - {str(ve)}")
        except Exception as e:
            return (False, f"错误：函数计算异常 - {str(e)}")

    def apply_scientific_operator(self, power_value=None):
        """应用科学运算符（幂运算、根运算）"""
        try:
            if self.history == "" or self.operator is None:
                return (False, "错误：缺少运算数")

            num1 = float(self.history)
            num2 = float(self.current_value) if power_value is None else power_value

            if self.operator == "^":
                result = num1 ** num2
            elif self.operator == "∜":
                if num2 == 0:
                    return (False, "错误：零次方根无意义")
                result = num1 ** (1/num2)
            else:
                return (False, "错误：无效运算符")

            self.history = ""
            self.operator = None
            self.current_value = self._format_result(result)
            self.is_new_operation = True
            return (True, "")

        except OverflowError:
            return (False, "错误：数值超出范围")
        except Exception as e:
            return (False, f"错误：运算异常 - {str(e)}")
