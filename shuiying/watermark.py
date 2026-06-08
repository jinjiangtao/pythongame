
from PIL import Image, ImageDraw, ImageFont
from utils import calculate_position


def create_text_watermark(text, font_name, font_size, color, opacity, rotation):
    """创建文字水印 - 基于最简单的工作原理"""
    try:
        font = ImageFont.truetype(font_name, font_size)
    except Exception as e:
        print(f"使用默认字体 (无法加载 {font_name})")
        font = ImageFont.load_default()
    
    # 获取文字尺寸
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    padding = 30
    img_width = text_width + padding * 2
    img_height = text_height + padding * 2
    
    # 创建水印图片
    txt_img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_img)
    
    # 计算颜色
    r, g, b = hex_to_rgb(color)
    a = int(opacity * 255)
    rgba = (r, g, b, a)
    
    # 绘制文字
    draw.text((padding, padding), text, font=font, fill=rgba)
    
    if rotation != 0:
        txt_img = txt_img.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)
    
    return txt_img


def hex_to_rgb(hex_color):
    """十六进制颜色转RGB"""
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    return (
        int(hex_color[0:lv//3], 16),
        int(hex_color[lv//3:2*lv//3], 16),
        int(hex_color[2*lv//3:], 16)
    )


def create_image_watermark(image_path, scale, opacity):
    """创建图片水印"""
    try:
        wm_img = Image.open(image_path)
        if wm_img.mode != 'RGBA':
            wm_img = wm_img.convert('RGBA')
        
        original_size = wm_img.size
        new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
        wm_img = wm_img.resize(new_size, Image.Resampling.LANCZOS)
        
        if opacity < 1.0:
            alpha = wm_img.split()[3]
            alpha = alpha.point(lambda p: int(p * opacity))
            wm_img.putalpha(alpha)
        
        return wm_img
    except Exception as e:
        print(f"加载水印图片错误: {e}")
        return None


def apply_watermark(base_img, wm_img, position, margin):
    """应用水印"""
    pos = calculate_position(base_img.size[0], base_img.size[1], wm_img.size[0], wm_img.size[1], position, margin)
    result = base_img.copy()
    result.paste(wm_img, pos, wm_img)
    return result


def process_image(input_path, output_path, settings):
    """处理单张图片 - 这是核心功能，必须确保正常工作"""
    print(f"[水印处理] 开始: {input_path}")
    
    # 1. 打开原图
    base_img = Image.open(input_path)
    base_img_rgba = base_img.convert('RGBA')
    
    # 2. 创建水印
    if settings['mode'] == 'text':
        wm_img = create_text_watermark(
            settings['text'],
            settings['font'],
            settings['font_size'],
            settings['color'],
            settings['opacity'],
            settings['rotation']
        )
    else:
        wm_img = create_image_watermark(
            settings['watermark_image'],
            settings['image_scale'],
            settings['opacity']
        )
    
    if not wm_img:
        print("[水印处理] 错误：无法创建水印")
        return False
    
    # 3. 应用水印
    result_rgba = apply_watermark(base_img_rgba, wm_img, settings['position'], settings['margin'])
    
    # 4. 保存
    ext = input_path.split('.')[-1].lower()
    output_is_jpg = (settings['output_format'] == '统一转成JPG') or (ext in ['jpg', 'jpeg'])
    
    if output_is_jpg:
        background = Image.new('RGB', result_rgba.size, (255, 255, 255))
        background.paste(result_rgba, (0, 0), mask=result_rgba.split()[3])
        background.save(output_path, 'JPEG', quality=settings['jpg_quality'])
    else:
        result_rgba.save(output_path)
    
    print(f"[水印处理] 完成: {output_path}")
    return True
