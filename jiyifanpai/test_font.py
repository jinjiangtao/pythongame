import pygame
import os
import sys

def test_chinese_font():
    """测试中文字体是否可用"""
    pygame.init()
    
    screen = pygame.display.set_mode((400, 200))
    pygame.display.set_caption("Chinese Font Test")
    
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc"
    ]
    
    font = None
    font_name = None
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font = pygame.font.Font(font_path, 36)
                font_name = font_path.split('/')[-1]
                print(f"✓ 成功加载字体: {font_name}")
                break
            except Exception as e:
                print(f"✗ 加载字体失败 {font_path}: {e}")
    
    if not font:
        print("✗ 未能找到任何中文字体")
        font = pygame.font.Font(None, 36)
    
    test_text = "记住卡片位置!"
    text_surface = font.render(test_text, True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(text_surface, (50, 80))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        pygame.display.flip()
        pygame.time.wait(100)
    
    pygame.quit()
    print("测试完成")

if __name__ == "__main__":
    test_chinese_font()
