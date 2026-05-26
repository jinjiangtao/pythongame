import pygame
from config import FONT_MEDIUM, BLACK, WHITE, SCREEN_WIDTH, FONT_LARGE

class GameStats:
    def __init__(self):
        self.steps = 0
        self.time = 0
        self.hints_used = 0
        self.is_running = False
        self.last_time = 0
    
    def start_timer(self):
        self.is_running = True
        self.last_time = pygame.time.get_ticks()
    
    def stop_timer(self):
        self.is_running = False
    
    def reset(self):
        self.steps = 0
        self.time = 0
        self.hints_used = 0
        self.is_running = False
        self.last_time = 0
    
    def update(self):
        if self.is_running:
            current_time = pygame.time.get_ticks()
            elapsed = (current_time - self.last_time) // 1000
            if elapsed >= 1:
                self.time += elapsed
                self.last_time = current_time
    
    def increment_steps(self):
        self.steps += 1
    
    def use_hint(self):
        self.hints_used += 1
    
    def get_steps(self):
        return self.steps
    
    def get_time(self):
        return self.time
    
    def get_hints_used(self):
        return self.hints_used
    
    def format_time(self):
        minutes = self.time // 60
        seconds = self.time % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def draw(self, screen, level_name):
        stats_bg = pygame.Rect(0, 0, SCREEN_WIDTH, 60)
        pygame.draw.rect(screen, (200, 200, 200), stats_bg)
        
        level_text = FONT_MEDIUM.render(f"关卡: {level_name}", True, BLACK)
        level_rect = level_text.get_rect(left=20, top=15)
        screen.blit(level_text, level_rect)
        
        steps_text = FONT_MEDIUM.render(f"步数: {self.steps}", True, BLACK)
        steps_rect = steps_text.get_rect(left=200, top=15)
        screen.blit(steps_text, steps_rect)
        
        time_text = FONT_MEDIUM.render(f"时间: {self.format_time()}", True, BLACK)
        time_rect = time_text.get_rect(left=350, top=15)
        screen.blit(time_text, time_rect)
    
    def draw_win_screen(self, screen, level_name):
        overlay = pygame.Surface((SCREEN_WIDTH, 600))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        win_title = FONT_LARGE.render("🎉 恭喜通关！", True, (255, 255, 0))
        win_rect = win_title.get_rect(center=(SCREEN_WIDTH // 2, 180))
        screen.blit(win_title, win_rect)
        
        level_text = FONT_MEDIUM.render(f"关卡: {level_name}", True, WHITE)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(level_text, level_rect)
        
        steps_text = FONT_MEDIUM.render(f"总步数: {self.steps}", True, WHITE)
        steps_rect = steps_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(steps_text, steps_rect)
        
        time_text = FONT_MEDIUM.render(f"用时: {self.format_time()}", True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
        screen.blit(time_text, time_rect)