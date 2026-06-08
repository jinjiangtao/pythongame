
from PIL import Image, ImageDraw, ImageFont
import os

print("=== 验证测试：明显可见的水印 ===")

# 创建测试图片
img = Image.new('RGB', (800, 600), color='white')
draw = ImageDraw.Draw(img)
draw.rectangle([200, 150, 600, 450], fill='lightgray')
img.save('verify_input.jpg')

# 方法1：直接在图片上绘制大文字 - 这种方法肯定能看到
print("\n方法1：直接绘制文字")
test1 = img.copy()
draw = ImageDraw.Draw(test1)
try:
    font = ImageFont.truetype("arial", 80)
except:
    font = ImageFont.load_default()
draw.text((100, 100), "方法1：直接绘制", fill=(255, 0, 0), font=font)
test1.save('verify_method1.jpg')
print("   ✓ 保存到 verify_method1.jpg")

# 方法2：使用我们的水印函数
print("\n方法2：使用我们的水印模块")
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from watermark import create_text_watermark, apply_watermark
from utils import calculate_position

# 创建非常明显的水印
wm_img = create_text_watermark(
    "方法2：水印模块",
    "arial",
    80,
    "#FF0000",  # 红色
    1.0,  # 完全不透明
    0
)
print(f"   水印尺寸: {wm_img.size}")

# 应用水印
base_img = Image.open('verify_input.jpg').convert('RGBA')
result = apply_watermark(base_img, wm_img, "正中间", 0)

# 保存
background = Image.new('RGB', result.size, (255, 255, 255))
background.paste(result, (0, 0), mask=result.split()[3])
background.save('verify_method2.jpg', 'JPEG', quality=95)
print("   ✓ 保存到 verify_method2.jpg")

print("\n=== 请对比两张图片 ===")
print("1. verify_method1.jpg 应该能看到红色大字")
print("2. verify_method2.jpg 应该也能看到红色大字")
print("如果两者都能看到，说明水印模块正常工作！")
