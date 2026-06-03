# main.py - 游戏主循环和入口

import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, LIGHT_GREEN, WHITE, RED, GREEN, INITIAL_BIRDS, GROUND_HEIGHT, PIG_SCORE, BLOCK_SCORE
from bird import Bird
from pig import Pig
from block import Block
from slingshot import Slingshot
from game_state import GameState
from utils import circle_circle_collision, circle_rect_collision, create_particles

def reset_game(bird, pigs, blocks, game_state):
    """重置游戏"""
    bird.reset()
    for pig in pigs:
        pig.alive = True
    for block in blocks:
        block.alive = True
        block.hp = 1
    game_state.reset()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("愤怒的小鸟 - 简化版")
    
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)
    small_font = pygame.font.Font(None, 24)
    
    bird = Bird()
    slingshot = Slingshot()
    game_state = GameState()
    
    pigs = [Pig(600, 520)]
    blocks = [Block(570, 550), Block(650, 550)]
    
    particles = []
    
    running = True
    while running:
        screen.fill(LIGHT_GREEN)
        
        pygame.draw.rect(screen, (34, 139, 34), (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_state.is_game_over():
                    reset_game(bird, pigs, blocks, game_state)
                    particles = []
            
            slingshot.handle_event(event, bird, game_state)
        
        if bird.is_flying:
            bird.update()
            bird.check_bounds()
            
            for pig in pigs:
                if pig.alive and circle_circle_collision(bird.x, bird.y, bird.radius, pig.x, pig.y, pig.radius):
                    pig.alive = False
                    bird.is_flying = False
                    game_state.add_score(PIG_SCORE)
                    particles.extend(create_particles(pig.x, pig.y, (0, 200, 0)))
            
            for block in blocks:
                if block.alive and circle_rect_collision(bird.x, bird.y, bird.radius, block.x, block.y, block.width, block.height):
                    block.hit()
                    bird.is_flying = False
                    game_state.add_score(BLOCK_SCORE)
                    particles.extend(create_particles(bird.x, bird.y, (139, 69, 19)))
            
            if not bird.is_flying and game_state.birds_left > 0:
                game_state.check_lose()
        
        if not bird.is_flying and not game_state.is_game_over() and game_state.birds_left > 0:
            bird.reset()
        
        game_state.check_win(pigs)
        
        for p in particles[:]:
            p.update()
            if p.life <= 0:
                particles.remove(p)
        
        slingshot.draw(screen)
        
        if not bird.is_flying:
            bird.draw(screen)
        
        for block in blocks:
            block.draw(screen)
        
        for pig in pigs:
            pig.draw(screen)
        
        for p in particles:
            p.draw(screen)
        
        score_text = font.render(f"得分: {game_state.score}", True, WHITE)
        screen.blit(score_text, (20, 20))
        
        for i in range(INITIAL_BIRDS):
            x = SCREEN_WIDTH - 30 - i * 30
            y = 20
            if i < game_state.birds_left:
                pygame.draw.circle(screen, RED, (x, y), 10)
            else:
                pygame.draw.circle(screen, (100, 100, 100), (x, y), 10)
        
        instructions = [
            "游戏说明:",
            "1. 点击并拖拽弹弓发射小鸟",
            "2. 击打猪头获得 100 分",
            "3. 击打方块获得 20 分",
            "4. 消灭所有猪头获胜",
            "5. 用完小鸟则失败",
            "6. 按 R 键重新开始"
        ]
        
        for i, text in enumerate(instructions):
            text_surface = small_font.render(text, True, WHITE)
            screen.blit(text_surface, (20, SCREEN_HEIGHT - 150 + i * 22))
        
        if game_state.win:
            win_text = big_font.render("胜利!", True, GREEN)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(win_text, text_rect)
            hint_text = font.render("按 R 键重新开始", True, WHITE)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(hint_text, hint_rect)
        
        if game_state.lose:
            lose_text = big_font.render("失败!", True, RED)
            text_rect = lose_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(lose_text, text_rect)
            hint_text = font.render("按 R 键重新开始", True, WHITE)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(hint_text, hint_rect)
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()