
from PIL import Image, ImageDraw, ImageFont
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from watermark import process_image


def integration_test():
    print("=== 完整集成测试 ===")
    
    # 1. 创建测试图片
    test_input = 'int_test_input.jpg'
    img = Image.new('RGB', (800, 600), color='lightblue')
    draw = ImageDraw.Draw(img)
    draw.rectangle([100, 100, 300, 300], fill='red')
    draw.rectangle([500, 100, 700, 300], fill='green')
    draw.rectangle([300, 400, 500, 550], fill='orange')
    img.save(test_input)
    print(f"1. 创建测试图片: {test_input}")
    
    # 2. 测试文字水印
    print("\n2. 测试文字水印...")
    settings = {
        'mode': 'text',
        'text': '测试水印',
        'font': 'arial',
        'font_size': 60,
        'color': '#000000',
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
    
    output_path = 'int_test_output.jpg'
    process_image(test_input, output_path, settings)
    print(f"   保存结果到: {output_path}")
    
    # 3. 验证水印是否存在
    print("\n3. 验证水印...")
    output_img = Image.open(output_path)
    print(f"   输出图片尺寸: {output_img.size}")
    print(f"   输出图片模式: {output_img.mode}")
    
    # 检查图片右下角是否有内容变化（简单检查）
    # 我们检查右下角区域的像素平均颜色是否变化
    box = (600, 450, 800, 600)
    region = output_img.crop(box)
    colors = region.getcolors()
    print(f"   检查到颜色数量: {len(colors) if colors else 'N/A'}")
    print("   ✓ 请手动打开 int_test_output.jpg 检查水印是否正常显示")
    
    print("\n=== 集成测试完成 ===")


if __name__ == "__main__":
    integration_test()
