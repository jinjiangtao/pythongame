import pygame
import sys
import os

def test_chinese_rendering():
    """测试中文字体渲染"""
    pygame.init()
    screen = pygame.display.set_mode((600, 300))
    pygame.display.set_caption("中文显示测试")
    
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc"
    ]
    
    selected_font = None
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                selected_font = pygame.font.Font(font_path, 32)
                print(f"成功加载字体: {font_path}")
                break
            except:
                continue
    
    if not selected_font:
        print("未找到中文字体，使用默认字体")
        selected_font = pygame.font.Font(None, 32)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.fill((30, 30, 50))
        
        texts = [
            ("记住卡片位置!", (100, 50)),
            ("按 R 重新开始  |  按 ESC 退出", (100, 100)),
            ("你翻了 20 步", (100, 150)),
            ("总步数: 25", (100, 200))
        ]
        
        for text, pos in texts:
            text_surface = selected_font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, pos)
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    test_chinese_rendering()
