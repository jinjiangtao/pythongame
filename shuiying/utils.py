
import os
from PIL import Image, ImageTk
from settings import SUPPORTED_FORMATS


def get_image_files(path):
    image_files = []
    if os.path.isfile(path):
        if os.path.splitext(path)[1].lower() in SUPPORTED_FORMATS:
            image_files.append(path)
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.path.splitext(file)[1].lower() in SUPPORTED_FORMATS:
                    image_files.append(os.path.join(root, file))
    return image_files


def load_image(file_path, max_size=None):
    try:
        img = Image.open(file_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        if max_size:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        return img
    except Exception as e:
        print(f'加载图片失败 {file_path}: {e}')
        return None


def image_to_tk(img):
    return ImageTk.PhotoImage(img)


def hex_to_rgba(hex_color, alpha=255):
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    return tuple(int(hex_color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)) + (alpha,)


def calculate_position(img_width, img_height, wm_width, wm_height, position, margin):
    from settings import POSITION_MAP
    x_ratio, y_ratio = POSITION_MAP[position]
    x = int((img_width - wm_width) * x_ratio)
    y = int((img_height - wm_height) * y_ratio)
    
    if x_ratio == 0:
        x += margin
    elif x_ratio == 1:
        x -= margin
    
    if y_ratio == 0:
        y += margin
    elif y_ratio == 1:
        y -= margin
    
    return (x, y)


def get_available_fonts():
    import sys
    if sys.platform == 'win32':
        fonts = ['Arial', 'Microsoft YaHei', 'SimHei', 'SimSun', 'KaiTi']
    elif sys.platform == 'darwin':
        fonts = ['Arial', 'Helvetica', 'PingFang SC', 'STHeiti']
    else:
        fonts = ['Arial', 'DejaVu Sans']
    return fonts
