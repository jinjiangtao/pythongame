import pygame
import os

pygame.init()

print("Available system fonts:")
all_fonts = pygame.sysfont.get_fonts()
for font in all_fonts[:20]:
    print(f"  {font}")

print("\nTesting Chinese font rendering...")
test_text = "金币: 100 第 1 天 农场指南"

font_candidates = ['simhei', 'msyh', 'simsun', 'mingliu', 'kaiti', 'songti']

for font_name in font_candidates:
    try:
        font = pygame.sysfont.SysFont(font_name, 24)
        if font:
            text_surface = font.render(test_text, True, (255, 255, 255))
            print(f"  {font_name}: SUCCESS - Can render Chinese")
        else:
            print(f"  {font_name}: FAILED - Font not found")
    except Exception as e:
        print(f"  {font_name}: ERROR - {str(e)}")

print("\nChecking font paths...")
font_paths = [
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simsun.ttc",
]
for path in font_paths:
    exists = os.path.exists(path)
    print(f"  {path}: {'EXISTS' if exists else 'NOT FOUND'}")
    if exists:
        try:
            font = pygame.font.Font(path, 24)
            text_surface = font.render(test_text, True, (255, 255, 255))
            print(f"    -> Can render Chinese: YES")
        except Exception as e:
            print(f"    -> Can render Chinese: NO - {str(e)}")

pygame.quit()
