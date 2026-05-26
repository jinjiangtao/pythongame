import pygame
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("简单测试")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 24)

current_screen = "menu"

def draw_menu():
    screen.fill((30, 30, 40))
    
    title = font.render("灯光迷阵", True, (255, 255, 0))
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
    screen.blit(title, title_rect)
    
    button_rect = pygame.Rect((SCREEN_WIDTH - 200) // 2, 200, 200, 50)
    pygame.draw.rect(screen, (50, 150, 255), button_rect, border_radius=8)
    
    button_text = small_font.render("开始游戏", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)
    
    return button_rect

def draw_game():
    screen.fill((30, 30, 40))
    
    game_text = font.render("游戏界面", True, (255, 255, 255))
    game_rect = game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(game_text, game_rect)
    
    for i in range(3):
        for j in range(3):
            cell_rect = pygame.Rect(250 + j * 80, 200 + i * 80, 70, 70)
            color = (255, 255, 0) if (i + j) % 2 == 0 else (128, 128, 128)
            pygame.draw.rect(screen, color, cell_rect, border_radius=8)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if current_screen == "menu":
                button_rect = draw_menu()
                if button_rect.collidepoint(mouse_pos):
                    print("点击开始游戏")
                    current_screen = "game"
            
            elif current_screen == "game":
                print(f"游戏中点击: {mouse_pos}")
    
    if current_screen == "menu":
        draw_menu()
    elif current_screen == "game":
        draw_game()
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()