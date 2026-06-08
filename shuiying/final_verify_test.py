
from PIL import Image, ImageDraw, ImageFont
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("最终验证测试 - 确保水印功能正常")
print("=" * 60)

# 1. 创建测试图片
test_input = "final_test_input.jpg"
img = Image.new('RGB', (800, 600), color='white')
draw = ImageDraw.Draw(img)
draw.rectangle([100, 100, 700, 500], fill='lightyellow')
img.save(test_input)
print(f"\n✓ 测试图片已创建: {test_input}")

# 2. 测试我们修复后的watermark.py
print("\n测试修复后的水印模块...")

from watermark import process_image

settings = {
    'mode': 'text',
    'text': '水印修复成功！',
    'font': 'arial',
    'font_size': 70,
    'color': '#FF0000',
    'opacity': 1.0,
    'rotation': 0,
    'position': '正中间',
    'margin': 20,
    'output_format': '保持原格式',
    'jpg_quality': 95,
    'filename_rule': '原文件名_watermarked',
    'custom_prefix': '',
    'output_mode': '新文件夹'
}

output_path = "final_test_output.jpg"

print("\n调用 process_image...")
success = process_image(test_input, output_path, settings)

if success:
    print(f"\n✓ 处理成功！输出文件: {output_path}")
    
    # 验证文件
    if os.path.exists(output_path):
        output_size = os.path.getsize(output_path)
        print(f"  输出文件大小: {output_size} bytes")
        
        # 打开检查一下
        output_img = Image.open(output_path)
        print(f"  输出尺寸: {output_img.size}")
        print(f"  输出模式: {output_img.mode}")
        
        print("\n" + "=" * 60)
        print("✓✓✓ 修复验证成功！")
        print("请打开 final_test_output.jpg 查看，")
        print("图片正中间应该有红色的'水印修复成功！'文字！")
        print("=" * 60)
    else:
        print("\n✗ 错误：输出文件不存在！")
else:
    print("\n✗ 处理失败！")
