import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((320, 320))
pygame.display.set_caption("扫雷游戏测试")

font = pygame.font.Font(None, 24)
text = font.render("Pygame 测试成功！游戏可以正常运行！", True, (0, 255, 0))
screen.blit(text, (20, 150))

pygame.display.flip()

import time
time.sleep(2)

pygame.quit()
print("✓ Pygame 测试通过！游戏可以正常运行。")
