import pygame
from config import FONT_MEDIUM, BLACK, WHITE, SCREEN_WIDTH, FONT_LARGE, FONT_SMALL, FONT_XLARGE

class GameStats:
    def __init__(self):
        self.steps = 0
        self.time = 0
        self.hints_used = 0
        self.is_running = False
        self.last_time = 0
        self.stars = 0
        self.theme = {
            "stats_bg": (200, 200, 200),
            "stats_text": (0, 0, 0),
            "text_color": (255, 255, 255)
        }
    
    def set_theme(self, theme):
        self.theme = theme
    
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
        self.stars = 0
    
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
    
    def set_stars(self, stars):
        self.stars = stars
    
    def get_stars(self):
        return self.stars
    
    def format_time(self):
        minutes = self.time // 60
        seconds = self.time % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def draw(self, screen, level_name, mode="classic", time_limit=0, step_limit=0):
        stats_bg = pygame.Rect(0, 0, SCREEN_WIDTH, 60)
        pygame.draw.rect(screen, self.theme["stats_bg"], stats_bg)
        
        pygame.draw.rect(screen, (150, 150, 150), stats_bg, 2)
        
        level_text = FONT_MEDIUM.render(f"关卡: {level_name}", True, self.theme["stats_text"])
        level_rect = level_text.get_rect(left=20, top=15)
        screen.blit(level_text, level_rect)
        
        steps_text = FONT_MEDIUM.render(f"步数: {self.steps}", True, self.theme["stats_text"])
        steps_rect = steps_text.get_rect(left=180, top=15)
        screen.blit(steps_text, steps_rect)
        
        if step_limit > 0:
            steps_remaining = step_limit - self.steps
            steps_color = (0, 150, 0) if steps_remaining > 5 else ((255, 150, 0) if steps_remaining > 0 else (255, 0, 0))
            steps_remaining_text = FONT_MEDIUM.render(f"/ {step_limit}", True, steps_color)
            steps_remaining_rect = steps_remaining_text.get_rect(left=steps_rect.right + 5, top=15)
            screen.blit(steps_remaining_text, steps_remaining_rect)
        
        time_text = FONT_MEDIUM.render(f"时间: {self.format_time()}", True, self.theme["stats_text"])
        time_rect = time_text.get_rect(left=330, top=15)
        screen.blit(time_text, time_rect)
        
        if time_limit > 0:
            time_remaining = time_limit - self.time
            time_color = (0, 150, 0) if time_remaining > 30 else ((255, 150, 0) if time_remaining > 10 else (255, 0, 0))
            time_remaining_text = FONT_MEDIUM.render(f"/ {time_limit}s", True, time_color)
            time_remaining_rect = time_remaining_text.get_rect(left=time_rect.right + 5, top=15)
            screen.blit(time_remaining_text, time_remaining_rect)
        
        mode_text = FONT_SMALL.render(f"模式: {self._get_mode_name(mode)}", True, self.theme["stats_text"])
        mode_rect = mode_text.get_rect(right=SCREEN_WIDTH - 20, top=10)
        screen.blit(mode_text, mode_rect)
    
    def _get_mode_name(self, mode):
        mode_names = {
            "classic": "经典",
            "timed": "限时",
            "limited_steps": "限步"
        }
        return mode_names.get(mode, "经典")
    
    def draw_win_screen(self, screen, level_name):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        win_title = FONT_XLARGE.render("🎉 恭喜通关！", True, (255, 255, 0))
        win_rect = win_title.get_rect(center=(SCREEN_WIDTH // 2, 180))
        screen.blit(win_title, win_rect)
        
        level_text = FONT_MEDIUM.render(f"关卡: {level_name}", True, self.theme["text_color"])
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(level_text, level_rect)
        
        steps_text = FONT_MEDIUM.render(f"总步数: {self.steps}", True, self.theme["text_color"])
        steps_rect = steps_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(steps_text, steps_rect)
        
        time_text = FONT_MEDIUM.render(f"用时: {self.format_time()}", True, self.theme["text_color"])
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
        screen.blit(time_text, time_rect)
        
        star_x = SCREEN_WIDTH // 2 - 60
        star_y = 400
        for i in range(3):
            star = "★" if i < self.stars else "☆"
            star_font = FONT_XLARGE
            star_color = (255, 215, 0) if i < self.stars else (100, 100, 100)
            star_text = star_font.render(star, True, star_color)
            
            star_scale = 1.0
            if i < self.stars:
                star_scale = 1.0 + (pygame.time.get_ticks() // 200 % 2) * 0.1
            
            scaled_star = pygame.transform.scale(star_text, 
                (int(star_text.get_width() * star_scale), int(star_text.get_height() * star_scale)))
            star_rect = scaled_star.get_rect(left=star_x + i * 60, top=star_y)
            screen.blit(scaled_star, star_rect)
        
        stars_label = FONT_MEDIUM.render("星级评价", True, self.theme["text_color"])
        stars_label_rect = stars_label.get_rect(center=(SCREEN_WIDTH // 2, 460))
        screen.blit(stars_label, stars_label_rect)
    
    def draw_failure_screen(self, screen, level_name, reason):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        fail_title = FONT_XLARGE.render("😢 游戏失败", True, (255, 100, 100))
        fail_rect = fail_title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(fail_title, fail_rect)
        
        reason_text = FONT_LARGE.render(reason, True, (255, 150, 100))
        reason_rect = reason_text.get_rect(center=(SCREEN_WIDTH // 2, 270))
        screen.blit(reason_text, reason_rect)
        
        level_text = FONT_MEDIUM.render(f"关卡: {level_name}", True, self.theme["text_color"])
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 330))
        screen.blit(level_text, level_rect)
        
        steps_text = FONT_MEDIUM.render(f"已用步数: {self.steps}", True, self.theme["text_color"])
        steps_rect = steps_text.get_rect(center=(SCREEN_WIDTH // 2, 380))
        screen.blit(steps_text, steps_rect)
        
        time_text = FONT_MEDIUM.render(f"已用时间: {self.format_time()}", True, self.theme["text_color"])
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 430))
        screen.blit(time_text, time_rect)