
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw
from watermark import process_image
from processor import BatchProcessor


def test_full_workflow():
    print("=== 完整应用工作流测试 ===")
    
    # 1. 创建测试图片
    test_img1 = "app_test1.jpg"
    test_img2 = "app_test2.jpg"
    
    for i, path in enumerate([test_img1, test_img2]):
        img = Image.new('RGB', (600, 400), color=f'hsl({i*120}, 70%, 70%)')
        draw = ImageDraw.Draw(img)
        draw.rectangle([100, 100, 500, 300], fill=f'hsl({(i+1)*60}, 70%, 50%)')
        img.save(path)
        print(f"创建测试图片: {path}")
    
    # 2. 设置参数
    settings = {
        'mode': 'text',
        'text': '应用测试水印',
        'font': 'arial',
        'font_size': 48,
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
    
    # 3. 创建图片列表
    image_list = [
        {'path': test_img1, 'width': 600, 'height': 400},
        {'path': test_img2, 'width': 600, 'height': 400}
    ]
    
    # 4. 处理图片
    print("\n开始处理图片...")
    for img_info in image_list:
        input_path = img_info['path']
        dirname = os.path.dirname(input_path)
        basename = os.path.basename(input_path)
        name, ext = os.path.splitext(basename)
        output_dir = os.path.join(dirname, 'watermarked')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'{name}_watermarked{ext}')
        
        print(f"处理 {input_path} -> {output_path}")
        process_image(input_path, output_path, settings)
    
    # 5. 验证结果
    print("\n验证结果:")
    output_dir = 'watermarked'
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        print(f"找到 {len(files)} 个输出文件:")
        for f in files:
            print(f"  - {f}")
            file_path = os.path.join(output_dir, f)
            img = Image.open(file_path)
            print(f"    尺寸: {img.size}, 模式: {img.mode}")
    
    print("\n=== 完整应用测试完成 ===")
    print("请检查 watermarked/ 文件夹中的图片，应该有明显可见的水印")


if __name__ == "__main__":
    test_full_workflow()
