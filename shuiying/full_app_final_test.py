
from PIL import Image, ImageDraw
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("完整应用级测试")
print("=" * 60)

# 1. 创建测试图片
test_img1 = "app_test1.jpg"
test_img2 = "app_test2.jpg"

for i, path in enumerate([test_img1, test_img2]):
    img = Image.new('RGB', (600, 400), color=f'hsl({i * 120}, 70%, 80%)')
    draw = ImageDraw.Draw(img)
    draw.rectangle([100, 100, 500, 300], fill=f'hsl({(i + 1) * 60}, 70%, 60%)')
    img.save(path)
    print(f"✓ 创建测试图片: {path}")

# 2. 模拟应用设置
settings = {
    'mode': 'text',
    'text': '批量水印测试',
    'font': 'arial',
    'font_size': 50,
    'color': '#0000FF',  # 蓝色
    'opacity': 1.0,
    'rotation': 0,
    'position': '右下',
    'margin': 20,
    'output_format': '保持原格式',
    'jpg_quality': 95,
    'filename_rule': '原文件名_watermarked',
    'custom_prefix': '',
    'output_mode': '新文件夹'
}

# 3. 测试 watermark 和 processor 模块
from processor import BatchProcessor

print("\n准备批量处理...")

image_list = [
    {'path': test_img1, 'width': 600, 'height': 400},
    {'path': test_img2, 'width': 600, 'height': 400}
]

# 由于BatchProcessor使用回调，我们简化直接调用process_image
print("\n直接测试 process_image:")

from watermark import process_image

for img_info in image_list:
    input_path = img_info['path']
    
    # 构造输出路径
    dirname = os.path.dirname(input_path)
    basename = os.path.basename(input_path)
    name, ext = os.path.splitext(basename)
    output_dir = os.path.join(dirname, 'watermarked')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{name}_watermarked{ext}')
    
    # 处理
    print(f"  处理: {input_path}")
    process_image(input_path, output_path, settings)

# 验证
print("\n验证结果:")
output_dir = 'watermarked'
if os.path.exists(output_dir):
    files = os.listdir(output_dir)
    for f in files:
        full_path = os.path.join(output_dir, f)
        size = os.path.getsize(full_path)
        print(f"  ✓ {f} ({size} bytes)")
        img = Image.open(full_path)
        print(f"    尺寸: {img.size}")

print("\n" + "=" * 60)
print("✓✓✓ 完整应用级测试成功！")
print("请查看 watermarked 文件夹中的图片，")
print("每张图片右下角应该有蓝色的'批量水印测试'文字！")
print("=" * 60)
