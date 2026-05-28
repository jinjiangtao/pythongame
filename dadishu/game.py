import pygame
import random
import time
from constants import *
from hole import Hole
from mole import Mole
from scoreboard import ScoreBoard

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("打地鼠小游戏")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = 'playing'
        self.score_board = ScoreBoard()
        
        self.holes = []
        self.moles = []
        self.init_holes()
        
        self.last_mole_time = 0
        self.mole_interval = 1000
        self.mole_visible_duration = 2000
        
        self.click_effect = None
        self.last_click_time = 0
        
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
                self.moles.append(Mole(hole))
    
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
        for mole in self.moles:
            if mole.is_visible():
                rect = mole.get_rect()
                if rect.collidepoint(pos):
                    mole.hit(pygame.time.get_ticks())
                    self.score_board.add_score()
                    clicked = True
                    break
        
        if clicked:
            self.click_effect = ('hit', pos)
        else:
            self.click_effect = ('miss', pos)
        self.last_click_time = pygame.time.get_ticks()
    
    def update_moles(self):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_mole_time > self.mole_interval:
            hidden_moles = [m for m in self.moles if m.is_hidden()]
            if hidden_moles:
                random.choice(hidden_moles).show()
                self.last_mole_time = current_time
                self.mole_interval = random.randint(500, 1500)
        
        for mole in self.moles:
            mole.update(current_time)
            if mole.is_visible() and current_time - mole.show_time > self.mole_visible_duration:
                mole.state = 'hiding'
    
    def update_timer(self):
        if self.game_state == 'playing':
            elapsed = pygame.time.get_ticks() // 1000
            remaining = GAME_DURATION - elapsed
            self.score_board.set_time(max(0, remaining))
            if remaining <= 0:
                self.game_state = 'game_over'
    
    def draw_background(self):
        self.screen.fill(GREEN)
        
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        pygame.draw.rect(self.screen, BROWN, (0, ground_y, SCREEN_WIDTH, GROUND_HEIGHT))
        
        for i in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(self.screen, DARK_BROWN, (i, ground_y), (i + 20, ground_y + 10), 2)
        
        title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
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
        
        font = pygame.font.Font(None, 48)
        title_text = font.render("游戏结束", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(title_text, title_rect)
        
        score_text = font.render(f"最终得分: {self.score_board.get_score()}", True, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        hint_font = pygame.font.Font(None, FONT_SIZE)
        hint_text = hint_font.render("按 R 键重新开始 | 按 ESC 退出", True, WHITE)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(hint_text, hint_rect)
    
    def reset_game(self):
        self.score_board.reset()
        self.game_state = 'playing'
        self.last_mole_time = 0
        self.mole_interval = 1000
        
        for mole in self.moles:
            mole.state = 'hidden'
            mole.current_y = mole.center_y + HOLE_HEIGHT // 2
        
        pygame.time.set_timer(pygame.USEREVENT, 0)
    
    def run(self):
        while self.running:
            self.handle_events()
            
            if self.game_state == 'playing':
                self.update_timer()
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