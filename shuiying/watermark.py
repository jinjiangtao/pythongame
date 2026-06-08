
from PIL import Image, ImageDraw, ImageFont, ImageOps
import math
from utils import hex_to_rgba, calculate_position


def create_text_watermark(text, font_name, font_size, color, opacity, rotation):
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
    wm_img = Image.open(image_path)
    if wm_img.mode != 'RGBA':
        wm_img = wm_img.convert('RGBA')
    
    original_size = wm_img.size
    new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
    wm_img = wm_img.resize(new_size, Image.Resampling.LANCZOS)
    
    if opacity < 1.0:
        alpha = wm_img.split()[3]
        alpha = alpha.point(lambda p: p * opacity)
        wm_img.putalpha(alpha)
    
    return wm_img


def apply_watermark(base_img, wm_img, position, margin):
    base_w, base_h = base_img.size
    wm_w, wm_h = wm_img.size
    
    pos = calculate_position(base_w, base_h, wm_w, wm_h, position, margin)
    
    result = base_img.copy()
    result.paste(wm_img, pos, wm_img)
    
    return result


def process_image(input_path, output_path, settings):
    base_img = Image.open(input_path)
    original_mode = base_img.mode
    if base_img.mode != 'RGBA':
        base_img = base_img.convert('RGBA')
    
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
    
    result = apply_watermark(base_img, wm_img, settings['position'], settings['margin'])
    
    if original_mode != 'RGBA':
        result = result.convert(original_mode)
    
    output_format = settings['output_format']
    if output_format == '统一转成JPG':
        if result.mode in ('RGBA', 'P'):
            background = Image.new('RGB', result.size, (255, 255, 255))
            background.paste(result, mask=result.split()[3] if result.mode == 'RGBA' else None)
            result = background
        result.save(output_path, 'JPEG', quality=settings['jpg_quality'])
    else:
        ext = input_path.split('.')[-1].lower()
        if ext in ['jpg', 'jpeg']:
            if result.mode == 'RGBA':
                background = Image.new('RGB', result.size, (255, 255, 255))
                background.paste(result, mask=result.split()[3])
                result = background
            result.save(output_path, 'JPEG', quality=settings['jpg_quality'])
        else:
            result.save(output_path)
