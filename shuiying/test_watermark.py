
from PIL import Image, ImageDraw, ImageFont
import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from watermark import create_text_watermark, create_image_watermark, apply_watermark, process_image
from utils import hex_to_rgba, calculate_position


def test_basic_watermark():
    print("=== 测试水印功能 ===")
    
    # 创建测试图片
    test_img_path = "test_image.jpg"
    create_test_image(test_img_path)
    print(f"1. 创建了测试图片: {test_img_path}")
    
    # 测试文字水印
    print("\n2. 测试文字水印...")
    test_text_watermark(test_img_path)
    
    print("\n=== 测试完成 ===")


def create_test_image(path):
    img = Image.new('RGB', (800, 600), color='lightblue')
    draw = ImageDraw.Draw(img)
    draw.rectangle([100, 100, 300, 300], fill='red')
    draw.rectangle([500, 100, 700, 300], fill='green')
    draw.rectangle([300, 400, 500, 550], fill='orange')
    img.save(path)


def test_text_watermark(input_path):
    settings = {
        'mode': 'text',
        'text': '测试水印',
        'font': 'arial',
        'font_size': 60,
        'color': '#000000',  # 黑色
        'opacity': 1.0,  # 完全不透明
        'rotation': 0,
        'position': '右下',
        'margin': 20,
        'output_format': '保持原格式',
        'jpg_quality': 95,
        'filename_rule': '原文件名_watermarked',
        'custom_prefix': '',
        'output_mode': '新文件夹'
    }
    
    output_path = "test_output.jpg"
    
    # 直接测试各个函数
    print("- 测试 create_text_watermark...")
    wm_img = create_text_watermark(
        settings['text'],
        settings['font'],
        settings['font_size'],
        settings['color'],
        settings['opacity'],
        settings['rotation']
    )
    print(f"  水印尺寸: {wm_img.size}")
    
    print("- 测试 apply_watermark...")
    base_img = Image.open(input_path).convert('RGBA')
    result = apply_watermark(base_img, wm_img, settings['position'], settings['margin'])
    
    print("- 保存结果...")
    background = Image.new('RGB', result.size, (255, 255, 255))
    background.paste(result, mask=result.split()[3])
    background.save(output_path, 'JPEG', quality=95)
    
    print(f"✓ 文字水印测试完成，输出到: {output_path}")
    print("  请检查此图片是否有水印")


if __name__ == "__main__":
    test_basic_watermark()
