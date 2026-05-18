"""
测试 Windows 中文字体 - 简化版
"""

import pygame

def test_fonts():
    pygame.init()
    
    print("=" * 60)
    print("Windows 中文字体测试")
    print("=" * 60)
    print()
    
    # 测试不同的中文字体名称
    font_names = [
        'SimSun', 'SimHei', 'Microsoft YaHei',
        'KaiTi', 'FangSong', 'STSong', 'STHeiti'
    ]
    
    print("测试中文字体:")
    print("-" * 40)
    
    for name in font_names:
        try:
            font = pygame.font.SysFont(name, 36)
            if font:
                # 测试渲染中文
                text = font.render("测试中文", True, (255, 255, 255))
                if text:
                    print(f"✓ {name} - 可用，支持中文")
                else:
                    print(f"✗ {name} - 渲染失败")
            else:
                print(f"✗ {name} - 获取失败")
        except Exception as e:
            print(f"✗ {name} - 错误: {str(e)[:50]}")
    
    pygame.quit()

if __name__ == "__main__":
    test_fonts()
