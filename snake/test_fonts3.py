"""
测试直接加载 Windows 字体文件
"""

import pygame
import os

def test_font_files():
    pygame.init()
    
    print("=" * 60)
    print("Windows 字体文件测试")
    print("=" * 60)
    print()
    
    # Windows 字体目录
    font_dirs = [
        r'C:\Windows\Fonts',
        r'C:\WINNT\Fonts',
        os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
    ]
    
    font_files = {
        'SimSun': ['simsun.ttc', 'simsun.ttf'],
        'SimHei': ['simhei.ttf', 'simhei.ttc'],
        'Microsoft YaHei': ['msyh.ttc', 'msyh.ttf'],
        'KaiTi': ['kaiu.ttf', 'kaiti.ttf'],
        'FangSong': ['simfang.ttf']
    }
    
    found_fonts = []
    
    for font_name, files in font_files.items():
        found = False
        for font_dir in font_dirs:
            for filename in files:
                font_path = os.path.join(font_dir, filename)
                if os.path.exists(font_path):
                    try:
                        font = pygame.font.Font(font_path, 36)
                        if font:
                            text = font.render("测试中文", True, (255, 255, 255))
                            if text:
                                print(f"✓ {font_name} - {filename}")
                                found_fonts.append((font_name, font_path))
                                found = True
                                break
                    except Exception as e:
                        print(f"✗ {font_name} ({filename}) - 错误: {str(e)[:50]}")
            if found:
                break
        if not found:
            print(f"✗ {font_name} - 未找到字体文件")
    
    pygame.quit()
    return found_fonts

if __name__ == "__main__":
    test_font_files()
