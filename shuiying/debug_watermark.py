
from PIL import Image, ImageDraw, ImageFont
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入我们的模块
from watermark import create_text_watermark, apply_watermark
from utils import hex_to_rgba, calculate_position
from settings import POSITION_MAP


def debug_test():
    print("=== 水印调试测试 ===")
    
    # 1. 打开测试图片
    test_img = 'simple_test_input.jpg'
    if not os.path.exists(test_img):
        print("创建测试图片")
        img = Image.new('RGB', (800, 600), color='lightblue')
        draw = ImageDraw.Draw(img)
        draw.rectangle([100, 100, 300, 300], fill='red')
        img.save(test_img)
    
    base_img = Image.open(test_img).convert('RGBA')
    print(f"基础图片: 尺寸 {base_img.size}, 模式 {base_img.mode}")
    
    # 2. 创建文字水印
    print("\n--- 创建文字水印 ---")
    text = "测试水印文字"
    font_size = 60
    color = "#000000"
    opacity = 1.0
    
    # 直接测试创建文字水印
    try:
        font = ImageFont.truetype("arial", font_size)
    except:
        font = ImageFont.load_default()
    
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    print(f"文字尺寸: width={text_width}, height={text_height}")
    
    padding = 20
    txt_img = Image.new('RGBA', (text_width + padding*2, text_height + padding*2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_img)
    
    rgba_color = hex_to_rgba(color, int(opacity * 255))
    print(f"颜色: {rgba_color}")
    
    draw.text((padding, padding), text, font=font, fill=rgba_color)
    
    txt_img.save('debug_watermark.png')
    print("保存了调试水印图片: debug_watermark.png")
    
    # 3. 测试位置计算
    position = "右下"
    margin = 20
    pos = calculate_position(base_img.size[0], base_img.size[1], txt_img.size[0], txt_img.size[1], position, margin)
    print(f"计算出的位置: {pos}")
    
    # 4. 应用水印
    print("\n--- 应用水印 ---")
    result = base_img.copy()
    result.paste(txt_img, pos, txt_img)
    
    # 5. 保存
    background = Image.new('RGB', result.size, (255, 255, 255))
    background.paste(result, mask=result.split()[3])
    output_path = 'debug_result.jpg'
    background.save(output_path, 'JPEG', quality=95)
    print(f"保存结果到: {output_path}")
    
    print("\n=== 调试完成 ===")
    print("请检查以下文件:")
    print("1. debug_watermark.png - 看水印是否正确生成")
    print("2. debug_result.jpg - 看最终结果是否有水印")


if __name__ == "__main__":
    debug_test()
