
from PIL import Image, ImageDraw
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("中文字体测试")
print("=" * 60)

# 创建测试图片
test_input = "chinese_test.jpg"
img = Image.new('RGB', (800, 600), color='white')
draw = ImageDraw.Draw(img)
draw.rectangle([100, 100, 700, 500], fill='lightyellow')
img.save(test_input)
print(f"✓ 测试图片已创建")

# 测试水印
settings = {
    'mode': 'text',
    'text': '中文水印测试成功！',
    'font': 'Microsoft YaHei',
    'font_size': 60,
    'color': '#0000FF',  # 蓝色
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

from watermark import process_image

output_path = "chinese_test_result.jpg"
print("\n开始水印处理...")
success = process_image(test_input, output_path, settings)

if success:
    print("\n" + "=" * 60)
    print("✓✓✓ 中文字体测试成功！")
    print(f"请查看文件: {output_path}")
    print("图片中间应该有蓝色的'中文水印测试成功！'")
    print("=" * 60)
else:
    print("\n✗ 测试失败！")
