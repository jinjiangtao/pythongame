import pygame
import random
import time
from constants import *
from hole import Hole
from mole import Mole
from scoreboard import ScoreBoard
from font_utils import get_chinese_font
from sound_manager import SoundManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("打地鼠小游戏")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = 'playing'
        self.score_board = ScoreBoard()
        self.sound_manager = SoundManager()
        
        self.holes = []
        self.moles = []
        self.init_holes()
        
        self.last_mole_time = 0
        self.mole_interval = MAX_MOLE_INTERVAL
        self.mole_visible_duration = BASE_MOLE_DURATION
        
        self.click_effect = None
        self.last_click_time = 0
        
        self.last_level_score = 0
        self.sound_manager.play('game_start')
        
    def init_holes(self):
        total_width = HOLE_COLS * HOLE_WIDTH + (HOLE_COLS - 1) * HOLE_GAP_X
        total_height = HOLE_ROWS * HOLE_HEIGHT + (HOLE_ROWS - 1) * HOLE_GAP_Y
        
        start_x = (SCREEN_WIDTH - total_width) // 2
        start_y = (SCREEN_HEIGHT - GROUND_HEIGHT - total_height) // 2 + 80
        
        for row in range(HOLE_ROWS):
            for col in range(HOLE_COLS):
                x = start_x + col * (HOLE_WIDTH + HOLE_GAP_X)
                y = start_y + row * (HOLE_HEIGHT + HOLE_GAP_Y)
                hole = Hole(x, y)
                self.holes.append(hole)
                mole = Mole(hole)
                mole.set_type()
                self.moles.append(mole)
    
    def update_difficulty(self):
        level = self.score_board.get_level()
        interval_range = MAX_MOLE_INTERVAL - (level - 1) * 100
        self.mole_interval = random.randint(max(MIN_MOLE_INTERVAL, interval_range // 2), interval_range)
        self.mole_visible_duration = max(MIN_MOLE_DURATION, BASE_MOLE_DURATION - (level - 1) * 150)
    
    def check_level_up(self):
        current_score = self.score_board.get_score()
        if current_score - self.last_level_score >= LEVEL_SCORE_THRESHOLD:
            if self.score_board.level_up():
                self.last_level_score = current_score
                self.score_board.add_time(LEVEL_BONUS_TIME)
                self.sound_manager.play('level_up')
                self.update_difficulty()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_state == 'game_over':
                    self.reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == 'playing':
                    self.handle_click(event.pos)
    
    def handle_click(self, pos):
        clicked = False
        hit_mole_type = None
        points = 0
        
        for mole in self.moles:
            if mole.is_visible():
                rect = mole.get_rect()
                if rect.collidepoint(pos):
                    mole.hit(pygame.time.get_ticks())
                    points = mole.get_points()
                    hit_mole_type = mole.type
                    self.score_board.add_score(points)
                    clicked = True
                    break
        
        if clicked:
            self.click_effect = ('hit', pos)
            self.sound_manager.play('hit')
            if hit_mole_type == 'red':
                self.score_board.reset_combo()
        else:
            self.click_effect = ('miss', pos)
            self.sound_manager.play('miss')
            self.score_board.reset_combo()
        
        self.last_click_time = pygame.time.get_ticks()
        self.check_level_up()
    
    def update_moles(self):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_mole_time > self.mole_interval:
            hidden_moles = [m for m in self.moles if m.is_hidden()]
            if hidden_moles:
                mole = random.choice(hidden_moles)
                mole.show()
                self.sound_manager.play('mole_appear')
                self.last_mole_time = current_time
        
        for mole in self.moles:
            mole.update(current_time)
            if mole.is_visible() and current_time - mole.show_time > self.mole_visible_duration:
                mole.state = 'hiding'
                if mole.type != 'red':
                    self.score_board.reset_combo()
    
    def update_timer(self):
        if self.game_state == 'playing':
            self.score_board.set_time(max(0, self.score_board.get_time() - 1))
            if self.score_board.get_time() <= 0:
                self.game_state = 'game_over'
                self.sound_manager.play('game_over')
    
    def draw_background(self):
        self.screen.fill(GREEN)
        
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        pygame.draw.rect(self.screen, BROWN, (0, ground_y, SCREEN_WIDTH, GROUND_HEIGHT))
        
        for i in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(self.screen, DARK_BROWN, (i, ground_y), (i + 20, ground_y + 10), 2)
        
        title_font = get_chinese_font(TITLE_FONT_SIZE)
        title_text = title_font.render("打地鼠", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
        self.screen.blit(title_text, title_rect)
    
    def draw_click_effect(self):
        if self.click_effect and pygame.time.get_ticks() - self.last_click_time < 300:
            effect_type, pos = self.click_effect
            if effect_type == 'hit':
                pygame.draw.circle(self.screen, YELLOW, pos, 20, 3)
            else:
                pygame.draw.circle(self.screen, RED, pos, 20, 3)
    
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font = get_chinese_font(48)
        title_text = font.render("游戏结束", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(title_text, title_rect)
        
        score_text = font.render(f"最终得分: {self.score_board.get_score()}", True, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)
        
        level_text = get_chinese_font(36).render(f"到达关卡: {self.score_board.get_level()}", True, BLUE)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(level_text, level_rect)
        
        max_combo_text = get_chinese_font(36).render(f"最高连击: {self.score_board.max_combo}", True, ORANGE)
        max_combo_rect = max_combo_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(max_combo_text, max_combo_rect)
        
        hint_font = get_chinese_font(FONT_SIZE)
        hint_text = hint_font.render("按 R 键重新开始 | 按 ESC 退出", True, WHITE)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130))
        self.screen.blit(hint_text, hint_rect)
    
    def reset_game(self):
        self.score_board.reset()
        self.game_state = 'playing'
        self.last_mole_time = 0
        self.mole_interval = MAX_MOLE_INTERVAL
        self.mole_visible_duration = BASE_MOLE_DURATION
        self.last_level_score = 0
        
        for mole in self.moles:
            mole.state = 'hidden'
            mole.current_y = mole.center_y + HOLE_HEIGHT // 2
            mole.set_type()
        
        self.sound_manager.play('game_start')
    
    def run(self):
        timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(timer_event, 1000)
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r and self.game_state == 'game_over':
                        self.reset_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_state == 'playing':
                        self.handle_click(event.pos)
                elif event.type == timer_event:
                    if self.game_state == 'playing':
                        self.update_timer()
            
            if self.game_state == 'playing':
                self.update_moles()
            
            self.draw_background()
            
            for hole in self.holes:
                hole.draw(self.screen)
            
            for mole in self.moles:
                mole.draw(self.screen)
            
            self.score_board.draw(self.screen)
            self.draw_click_effect()
            
            if self.game_state == 'game_over':
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()