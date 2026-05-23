import pygame
import os

def get_chinese_font(size):
    font_paths = [
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/kaiu.ttf",
        "C:/Windows/Fonts/STKaiti.ttf",
        "C:/Windows/Fonts/STSong.ttf",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, size)
            except:
                continue
    
    return pygame.font.Font(None, size)
