import pygame
import os

def get_chinese_font(font_size=24, font_name="SimHei"):
    """
    获取支持中文的字体
    按优先级尝试：
    1. 使用系统中匹配的字体
    2. 直接指定Windows字体路径
    3. 返回默认字体（可能不支持中文）
    """
    # 尝试1：使用 pygame.font.match_font
    try:
        font_path = pygame.font.match_font(font_name)
        if font_path:
            return pygame.font.Font(font_path, font_size)
    except:
        pass
    
    # 尝试2：直接指定Windows字体路径
    windows_font_paths = [
        f"C:/Windows/Fonts/{font_name}.ttf",
        f"C:/Windows/Fonts/{font_name}.otf",
        f"C:/Windows/Fonts/{font_name.lower()}.ttf",
        f"C:/Windows/Fonts/{font_name.lower()}.otf",
        f"C:/Windows/Fonts/simhei.ttf",
        f"C:/Windows/Fonts/simsun.ttc",
    ]
    
    for font_path in windows_font_paths:
        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, font_size)
            except:
                continue
    
    # 尝试3：使用其他常见中文字体
    common_fonts = ["simhei", "simsun", "mingliu", "msyh", "kaiu"]
    for font in common_fonts:
        try:
            font_path = pygame.font.match_font(font)
            if font_path:
                return pygame.font.Font(font_path, font_size)
        except:
            continue
    
    # 最后返回默认字体
    return pygame.font.Font(None, font_size)