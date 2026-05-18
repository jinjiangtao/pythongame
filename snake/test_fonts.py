"""
测试 Windows 系统中 pygame 可用的中文字体
"""

import pygame

def test_fonts():
    pygame.init()
    
    print("=" * 60)
    print("Windows 中文字体测试")
    print("=" * 60)
    print()
    
    # 获取所有可用字体
    fonts = pygame.font.get_fonts()
    print(f"系统中可用的字体数量: {len(fonts)}")
    print()
    
    # 查找中文字体
    chinese_fonts = []
    font_names_to_test = [
        'simsun', 'SimSun', 'SimHei', 'simhei',
        'Microsoft YaHei', 'MicrosoftYaHei', 'msyh',
        'KaiTi', 'KaiTi_GB2312', '楷体',
        'STSong', 'STKaiti', 'STXihei',
        'FangSong', 'FangSong_GB2312', '仿宋'
    ]
    
    print("测试常见中文字体名称:")
    print("-" * 40)
    
    for font_name in font_names_to_test:
        try:
            font = pygame.font.SysFont(font_name, 36)
            if font:
                print(f"✓ {font_name} - 可用")
                chinese_fonts.append(font_name)
            else:
                print(f"✗ {font_name} - 不可用")
        except Exception as e:
            print(f"✗ {font_name} - 错误: {e}")
    
    print()
    print("=" * 60)
    print("可用的中文字体列表:")
    print("-" * 40)
    for font in chinese_fonts:
        print(f"  • {font}")
    
    pygame.quit()
    return chinese_fonts

if __name__ == "__main__":
    test_fonts()
