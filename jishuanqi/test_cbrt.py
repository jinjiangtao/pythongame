import sys
sys.path.insert(0, r'd:\trae\pythongame\jishuanqi')

from model import CalculatorModel

model = CalculatorModel()

print("测试立方根：")
model.append_number("27")
print(f"当前输入: {model.current_value}")
result = model.apply_scientific_function("cbrt")
print(f"apply_scientific_function 返回: {result}")
print(f"最终结果: {model.current_value}")

print(f"\n直接计算: 27 ** (1/3) = {27 ** (1/3)}")
print(f"使用 copysign: {27 ** (1/3):.15f}")

import math
print(f"使用 math.cbrt: {math.cbrt(27)}")
