
from PIL import Image, ImageDraw, ImageFont
from utils import hex_to_rgba, calculate_position


def create_text_watermark(text, font_name, font_size, color, opacity, rotation):
    """创建文字水印"""
    try:
        font = ImageFont.truetype(font_name, font_size)
    except:
        font = ImageFont.load_default()
    
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    padding = 20
    img_width = text_width + padding * 2
    img_height = text_height + padding * 2
    
    txt_img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_img)
    
    rgba_color = hex_to_rgba(color, int(opacity * 255))
    draw.text((padding, padding), text, font=font, fill=rgba_color)
    
    if rotation != 0:
        txt_img = txt_img.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)
    
    return txt_img


def create_image_watermark(image_path, scale, opacity):
    """创建图片水印"""
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


def apply_watermark(base_img, wm_img, position, margin):
    """应用水印到图片"""
    result = base_img.copy()
    pos = calculate_position(base_img.size[0], base_img.size[1], wm_img.size[0], wm_img.size[1], position, margin)
    result.paste(wm_img, pos, wm_img)
    return result


def process_image(input_path, output_path, settings):
    """处理单张图片"""
    base_img = Image.open(input_path)
    
    # 转换为RGBA模式进行处理
    if base_img.mode != 'RGBA':
        base_img = base_img.convert('RGBA')
    
    # 创建水印
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
    
    # 应用水印
    result = apply_watermark(base_img, wm_img, settings['position'], settings['margin'])
    
    # 保存文件
    output_format = settings['output_format']
    ext = input_path.split('.')[-1].lower()
    
    # 判断是否需要保存为JPG
    save_as_jpg = (output_format == '统一转成JPG') or (ext in ['jpg', 'jpeg'])
    
    if save_as_jpg:
        # 保存为JPG，需要处理透明度
        background = Image.new('RGB', result.size, (255, 255, 255))
        background.paste(result, (0, 0), mask=result.split()[3])
        background.save(output_path, 'JPEG', quality=settings['jpg_quality'])
    else:
        # 保持原格式
        result.save(output_path)
