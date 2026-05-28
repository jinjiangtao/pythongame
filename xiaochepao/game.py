import pygame
import random
import sys
import os
from constants import *
from car import Car
from obstacle import ObstacleManager
from powerup import PowerUpManager

def get_chinese_font(size):
    font_names = ['simhei', 'simsun', 'msyh', 'microsoftyahei', 'kaiti', 'fangsong']
    for font_name in font_names:
        try:
            return pygame.font.SysFont(font_name, size)
        except:
            continue
    
    font_paths = [
        'C:\\Windows\\Fonts\\simhei.ttf',
        'C:\\Windows\\Fonts\\simsun.ttc',
        'C:\\Windows\\Fonts\\msyh.ttc',
        'C:\\Windows\\Fonts\\msyhbd.ttc',
    ]
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, size)
            except:
                continue
    
    return pygame.font.Font(None, size)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("小车跑酷")
        
        self.clock = pygame.time.Clock()
        self.reset()
        
        self.font = get_chinese_font(36)
        self.small_font = get_chinese_font(24)
    
    def reset(self):
        self.car = Car()
        self.obstacle_manager = ObstacleManager()
        self.powerup_manager = PowerUpManager()
        self.score = 0
        self.game_over = False
        self.last_score_time = pygame.time.get_ticks()
        self.current_speed = BASE_OBSTACLE_SPEED
        
        self.slow_mode = False
        self.slow_timer = 0
        self.double_score = False
        self.double_score_timer = 0
    
    def get_adjusted_speed(self):
        speed = self.current_speed
        if self.slow_mode:
            speed *= POWERUP_SLOW_FACTOR
        return speed
    
    def update_speed(self):
        target_speed = BASE_OBSTACLE_SPEED + (self.score * SPEED_INCREMENT)
        self.current_speed = min(target_speed, MAX_SPEED)
    
    def spawn_objects(self):
        self.obstacle_manager.spawn_obstacle(self.score)
        self.powerup_manager.spawn_powerup()
    
    def update_score(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_score_time >= 100:
            score_increment = 2 if self.double_score else 1
            self.score += score_increment
            self.last_score_time = current_time
    
    def update_powerup_timers(self):
        if self.slow_mode:
            self.slow_timer -= 16
            if self.slow_timer <= 0:
                self.slow_mode = False
        
        if self.double_score:
            self.double_score_timer -= 16
            if self.double_score_timer <= 0:
                self.double_score = False
    
    def check_pixel_collision(self, car, obstacle):
        car_mask = car.get_mask()
        obstacle_mask = obstacle.get_mask()
        
        offset_x = obstacle.x - car.x
        offset_y = obstacle.y - car.y
        
        overlap = car_mask.overlap(obstacle_mask, (offset_x, offset_y))
        if overlap:
            overlap_area = 0
            for dy in range(-5, 6):
                for dx in range(-5, 6):
                    if obstacle_mask.get_at((overlap[0] + dx, overlap[1] + dy)):
                        if car_mask.get_at((overlap[0] + dx - offset_x, overlap[1] + dy - offset_y)):
                            overlap_area += 1
            return overlap_area > 10
        return False
    
    def check_collisions(self):
        if self.car.is_invincible:
            return
        
        for obstacle in self.obstacle_manager.get_obstacles():
            if self.check_pixel_collision(self.car, obstacle):
                self.game_over = True
                break
    
    def check_powerup_collisions(self):
        for powerup in self.powerup_manager.get_powerups():
            if self.car.get_rect().colliderect(powerup.get_rect()):
                powerup.picked = True
                
                if powerup.type == "slow":
                    self.slow_mode = True
                    self.slow_timer = POWERUP_DURATION
                elif powerup.type == "invincible":
                    self.car.set_invincible(POWERUP_DURATION)
                elif powerup.type == "double_score":
                    self.double_score = True
                    self.double_score_timer = POWERUP_DURATION
    
    def update(self):
        if not self.game_over:
            self.car.update()
            
            self.update_speed()
            self.update_powerup_timers()
            
            self.spawn_objects()
            
            speed = self.get_adjusted_speed()
            self.obstacle_manager.update(speed)
            self.powerup_manager.update(speed)
            
            self.update_score()
            self.check_collisions()
            self.check_powerup_collisions()
    
    def draw_background(self):
        sky_color = BLUE
        if self.slow_mode:
            sky_color = (30, 100, 200)
        
        self.screen.fill(sky_color)
        
        for i in range(0, SCREEN_WIDTH, 100):
            cloud_color = (100, 180, 255) if self.slow_mode else (70, 180, 255)
            pygame.draw.rect(self.screen, cloud_color, (i, 0, 50, SCREEN_HEIGHT))
        
        pygame.draw.rect(self.screen, GREEN, (0, GROUND_Y, SCREEN_WIDTH, GROUND_HEIGHT))
        
        pygame.draw.rect(self.screen, DARK_GRAY, (0, GROUND_Y, SCREEN_WIDTH, 10))
        
        for i in range(0, SCREEN_WIDTH, 40):
            pygame.draw.rect(self.screen, GRAY, (i, GROUND_Y + 20, 20, 5))
    
    def draw_ui(self):
        score_text = self.font.render(f"分数: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        
        speed_text = self.small_font.render(f"速度: {int(self.current_speed * 10) / 10}x", True, WHITE)
        self.screen.blit(speed_text, (20, 60))
        
        active_effects = []
        if self.slow_mode:
            active_effects.append("减速")
        if self.car.is_invincible:
            active_effects.append("无敌")
        if self.double_score:
            active_effects.append("双倍")
        
        if active_effects:
            effects_text = self.small_font.render("效果: " + ", ".join(active_effects), True, YELLOW)
            self.screen.blit(effects_text, (SCREEN_WIDTH - 200, 60))
        
        hint_text = self.small_font.render("空格键跳跃(支持二段跳) | R键重新开始 | ESC键退出", True, WHITE)
        self.screen.blit(hint_text, (SCREEN_WIDTH - 400, 20))
    
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("游戏结束!", True, RED)
        score_text = self.font.render(f"最终分数: {self.score}", True, YELLOW)
        restart_text = self.small_font.render("按 R 键重新开始 | 按 ESC 键退出", True, WHITE)
        
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def draw(self):
        self.draw_background()
        
        self.obstacle_manager.draw(self.screen)
        self.powerup_manager.draw(self.screen)
        
        self.car.draw(self.screen)
        
        self.draw_ui()
        
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.car.jump()
                
                if event.key == pygame.K_r:
                    self.reset()
                
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)