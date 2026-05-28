import pygame
from config import *


class ScoreTimer:
    def __init__(self):
        self.score = 0
        self.level = INITIAL_LEVEL
        self.time_left = GAME_DURATION
        self.start_time = pygame.time.get_ticks()
        self.game_over = False
        self.game_started = False
        
        self.combo = 0
        self.max_combo = 0
        self.total_catches = 0
        self.special_catches = {'flash': 0, 'accel': 0, 'trick': 0}
        self.prop_collects = {'time': 0, 'catch_all': 0, 'score': 0}
        
        self.combo_timer = 0
        self.combo_timeout = 2000
    
    def update(self):
        if self.game_over or not self.game_started:
            return
        
        elapsed = pygame.time.get_ticks() - self.start_time
        self.time_left = max(0, GAME_DURATION - elapsed // 1000)
        
        if self.combo > 0:
            if pygame.time.get_ticks() - self.combo_timer > self.combo_timeout:
                self.break_combo()
        
        if self.time_left <= 0:
            self.game_over = True
        
        new_level = self.score // LEVEL_UP_SCORE + 1
        if new_level > self.level:
            self.level = new_level
    
    def add_score(self, points, special_type=None):
        if points > 0:
            self.combo += 1
            self.combo_timer = pygame.time.get_ticks()
            
            if self.combo > self.max_combo:
                self.max_combo = self.combo
            
            self.total_catches += 1
            
            if special_type and special_type in self.special_catches:
                self.special_catches[special_type] += 1
            
            combo_bonus = 0
            if self.combo >= COMBO_BONUS_THRESHOLD:
                combo_bonus = int(points * COMBO_BONUS_MULTIPLIER * (self.combo - COMBO_BONUS_THRESHOLD + 1))
                points += combo_bonus
            
            self.score += points
            return combo_bonus
        else:
            self.score = max(0, self.score + points)
            if special_type == 'trick':
                self.special_catches['trick'] += 1
            return 0
    
    def break_combo(self):
        self.combo = 0
    
    def add_time(self, seconds):
        self.time_left += seconds
    
    def collect_prop(self, prop_type):
        if prop_type and prop_type in self.prop_collects:
            self.prop_collects[prop_type] += 1
    
    def reset(self):
        self.score = 0
        self.level = INITIAL_LEVEL
        self.time_left = GAME_DURATION
        self.start_time = pygame.time.get_ticks()
        self.game_over = False
        self.game_started = True
        
        self.combo = 0
        self.max_combo = 0
        self.total_catches = 0
        self.special_catches = {'flash': 0, 'accel': 0, 'trick': 0}
        self.prop_collects = {'time': 0, 'catch_all': 0, 'score': 0}
        self.combo_timer = 0
    
    def get_chinese_font(self, size):
        font_paths = [
            'C:/Windows/Fonts/simhei.ttf',
            'C:/Windows/Fonts/msyh.ttc',
            'C:/Windows/Fonts/simsun.ttc',
        ]
        for path in font_paths:
            try:
                return pygame.font.Font(path, size)
            except:
                continue
        return pygame.font.Font(None, size)
    
    def draw(self, screen):
        self.draw_top_bar(screen)
    
    def draw_top_bar(self, screen):
        bar_height = 70
        bar_rect = pygame.Rect(0, 0, SCREEN_WIDTH, bar_height)
        
        bar_surface = pygame.Surface((SCREEN_WIDTH, bar_height), pygame.SRCALPHA)
        pygame.draw.rect(bar_surface, (*TOP_BAR_COLOR, 220), bar_rect)
        pygame.draw.rect(bar_surface, (*self.darken_color(TOP_BAR_COLOR, 0.8), 255), 
                        bar_rect, 3)
        
        pygame.draw.rect(bar_surface, (255, 255, 255, 100), 
                        (10, 10, SCREEN_WIDTH - 20, bar_height - 20), 2, border_radius=10)
        
        screen.blit(bar_surface, (0, 0))
        
        font_large = self.get_chinese_font(24)
        font_medium = self.get_chinese_font(20)
        
        score_text = font_large.render(f'得分: {self.score}', True, TEXT_COLOR)
        score_rect = score_text.get_rect(left=30, centery=bar_height // 2)
        screen.blit(score_text, score_rect)
        
        combo_text = font_medium.render(f'连击: {self.combo}', True, 
                                       SUCCESS_COLOR if self.combo >= COMBO_BONUS_THRESHOLD else TEXT_COLOR)
        combo_rect = combo_text.get_rect(left=30, centery=bar_height // 2 + 25)
        screen.blit(combo_text, combo_rect)
        
        time_text = font_large.render(f'时间: {self.time_left}s', True, TEXT_COLOR)
        time_rect = time_text.get_rect(centerx=SCREEN_WIDTH // 2, centery=bar_height // 2)
        screen.blit(time_text, time_rect)
        
        level_target = self.level * LEVEL_UP_SCORE
        progress = min(1.0, self.score / level_target)
        progress_bar_width = 120
        progress_bar_height = 8
        progress_bar_x = SCREEN_WIDTH // 2 - progress_bar_width // 2
        progress_bar_y = bar_height // 2 + 18
        
        pygame.draw.rect(screen, (200, 200, 200), 
                        (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 
                        border_radius=4)
        pygame.draw.rect(screen, SUCCESS_COLOR, 
                        (progress_bar_x, progress_bar_y, int(progress_bar_width * progress), progress_bar_height), 
                        border_radius=4)
        
        level_text = font_large.render(f'关卡 {self.level}', True, TEXT_COLOR)
        level_rect = level_text.get_rect(right=SCREEN_WIDTH - 30, centery=bar_height // 2)
        screen.blit(level_text, level_rect)
        
        target_text = font_medium.render(f'目标: {level_target}', True, TEXT_COLOR)
        target_rect = target_text.get_rect(right=SCREEN_WIDTH - 30, centery=bar_height // 2 + 25)
        screen.blit(target_text, target_rect)
    
    def darken_color(self, color, factor):
        return tuple(max(0, int(c * factor)) for c in color)
    
    def draw_game_over_screen(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        panel_width = 500
        panel_height = 450
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2
        
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (50, 50, 80, 240), 
                        (0, 0, panel_width, panel_height), border_radius=20)
        pygame.draw.rect(panel_surface, GOLD_COLOR, 
                        (0, 0, panel_width, panel_height), 4, border_radius=20)
        
        screen.blit(panel_surface, (panel_x, panel_y))
        
        font_title = self.get_chinese_font(42)
        font_large = self.get_chinese_font(28)
        font_medium = self.get_chinese_font(22)
        
        title_text = font_title.render('游戏结束!', True, GOLD_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 50))
        screen.blit(title_text, title_rect)
        
        y_offset = panel_y + 110
        
        stats = [
            (f'最终得分: {self.score}', TEXT_COLOR),
            (f'达到关卡: {self.level}', TEXT_COLOR),
            (f'最高连击: {self.max_combo}', SUCCESS_COLOR if self.max_combo >= COMBO_BONUS_THRESHOLD else TEXT_COLOR),
            (f'捕捉数量: {self.total_catches}', TEXT_COLOR),
            (f'闪光宠: {self.special_catches["flash"]}只', FLASH_PET_COLOR),
            (f'加速宠: {self.special_catches["accel"]}只', ACCEL_PET_COLOR),
            (f'恶作剧宠: {self.special_catches["trick"]}只', TRICK_PET_COLOR),
        ]
        
        for text, color in stats:
            stat_text = font_large.render(text, True, color)
            stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(stat_text, stat_rect)
            y_offset += 35
        
        y_offset += 10
        
        restart_text = font_medium.render('按 R 键重新开始', True, SUCCESS_COLOR)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(restart_text, restart_rect)
        
        quit_text = font_medium.render('按 ESC 键退出游戏', True, FAILURE_COLOR)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 30))
        screen.blit(quit_text, quit_rect)
    
    def draw_start_screen(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        font_title = self.get_chinese_font(56)
        font_medium = self.get_chinese_font(28)
        font_small = self.get_chinese_font(20)
        
        title_text = font_title.render('抓萌宠小游戏', True, GOLD_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title_text, title_rect)
        
        instructions = [
            '🎯 点击捕捉萌宠获得分数',
            '⚡ 连续捕捉积累连击获得额外奖励',
            '✨ 闪光宠 = 3倍分数 | ⚡ 加速宠 = 快速加分 | ❌ 恶作剧宠 = 扣分',
            '🎁 收集道具获得时间加成、全屏捕捉、分数翻倍',
            '📈 每达成目标分数进入下一关，难度递增'
        ]
        
        y_offset = SCREEN_HEIGHT // 2 - 50
        for instruction in instructions:
            text = font_small.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 35
        
        start_text = font_medium.render('点击任意位置开始游戏', True, SUCCESS_COLOR)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))
        screen.blit(start_text, start_rect)
