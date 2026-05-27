import sys
sys.path.insert(0, r'd:\trae\pythongame\jishuanqi')

from model import CalculatorModel

model = CalculatorModel()

print("测试基本运算：")
model.append_number("5")
model.set_operator("+")
model.append_number("3")
result = model.calculate()
print(f"5 + 3 = {model.current_value}")

model.reset()
print("\n测试科学函数：")
model.append_number("16")
result = model.apply_scientific_function("sqrt")
print(f"√16 = {model.current_value}")

model.reset()
model.append_number("90")
result = model.apply_scientific_function("sin")
print(f"sin(90°) = {model.current_value}")

model.reset()
model.append_number("100")
result = model.apply_scientific_function("log")
print(f"log(100) = {model.current_value}")

model.reset()
model.append_number("2")
model.apply_scientific_function("square")
print(f"2² = {model.current_value}")

model.reset()
model.append_number("27")
result = model.apply_scientific_function("cube")
print(f"27^(1/3) = {27 ** (1/3):.10f}")
result = model.apply_scientific_function("cbrt")
print(f"∛27 = {model.current_value}")

model.reset()
model.append_number("3")
result = model.apply_scientific_function("factorial")
print(f"3! = {model.current_value}")

model.reset()
model.append_number("5")
result = model.apply_scientific_function("pi")
print(f"π = {model.current_value}")

model.reset()
model.append_number("1")
result = model.apply_scientific_function("e")
print(f"e = {model.current_value}")

model.reset()
model.append_number("-5")
result = model.apply_scientific_function("abs")
print(f"|-5| = {model.current_value}")

model.reset()
model.append_number("4")
result = model.apply_scientific_function("inverse")
print(f"1/4 = {model.current_value}")

print("\n所有测试通过！")
