
from PIL import Image, ImageDraw, ImageFont
import os
import sys

# 添加当前目录
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("水印功能终极测试")
print("=" * 60)

# 1. 创建一张测试图片
test_input = "ultimate_test_input.jpg"
img = Image.new('RGB', (800, 600), color='skyblue')
draw = ImageDraw.Draw(img)
draw.rectangle([100, 100, 700, 500], fill='lightgreen')
draw.text((200, 200), "测试图片", fill='black', font=ImageFont.load_default())
img.save(test_input)
print(f"\n✓ 创建测试图片: {test_input}")

# 2. 测试直接绘制文字（不使用水印模块）
print("\n--- 测试1: 直接绘制文字 ---")
test1 = img.copy()
draw1 = ImageDraw.Draw(test1)
try:
    font1 = ImageFont.truetype("arial", 60)
except:
    font1 = ImageFont.load_default()
draw1.text((200, 250), "直接绘制的文字", fill=(255, 0, 0), font=font1)
test1.save("ultimate_test1.jpg")
print("✓ 保存 ultimate_test1.jpg (应该能看到红色文字)")

# 3. 测试我们的水印模块
print("\n--- 测试2: 使用水印模块 ---")
from watermark import process_image

settings = {
    'mode': 'text',
    'text': '水印模块测试',
    'font': 'arial',
    'font_size': 60,
    'color': '#FF0000',  # 红色
    'opacity': 1.0,     # 完全不透明
    'rotation': 0,
    'position': '正中间',
    'margin': 20,
    'output_format': '保持原格式',
    'jpg_quality': 95,
    'filename_rule': '原文件名_watermarked',
    'custom_prefix': '',
    'output_mode': '新文件夹'
}

output_path = "ultimate_test2.jpg"
success = process_image(test_input, output_path, settings)

if success:
    print(f"✓ 保存 ultimate_test2.jpg (应该能看到红色水印文字)")
else:
    print("✗ 水印处理失败!")

# 4. 检查生成的文件
print("\n--- 验证文件 ---")
for f in ["ultimate_test1.jpg", "ultimate_test2.jpg"]:
    if os.path.exists(f):
        size = os.path.getsize(f)
        print(f"✓ {f} 存在, 大小: {size} bytes")
    else:
        print(f"✗ {f} 不存在!")

print("\n" + "=" * 60)
print("请检查以下文件:")
print("1. ultimate_test1.jpg - 直接绘制的文字，应该能看到")
print("2. ultimate_test2.jpg - 使用水印模块的文字，也应该能看到")
print("=" * 60)
