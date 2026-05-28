import pygame
import sys
from config import *
from game_area import GameArea
from score_timer import ScoreTimer

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('抓萌宠小游戏')
        
        self.game_area = GameArea()
        self.score_timer = ScoreTimer()
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.font_large = self.get_chinese_font(48)
        self.font_medium = self.get_chinese_font(32)
        
        self.click_effect = None
    
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
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.score_timer.game_over:
                    self.reset_game()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.score_timer.game_over:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    success, points = self.game_area.handle_click(mouse_x, mouse_y)
                    if success:
                        self.score_timer.add_score(points)
                        self.click_effect = (mouse_x, mouse_y, 0)
    
    def reset_game(self):
        self.score_timer.reset()
        self.game_area.clear_pets()
    
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        title_text = self.font_large.render('游戏结束!', True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title_text, title_rect)
        
        score_text = self.font_medium.render(f'最终得分: {self.score_timer.score}', True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        level_text = self.font_medium.render(f'达到关卡: {self.score_timer.level}', True, WHITE)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(level_text, level_rect)
        
        restart_text = self.font_medium.render('按 R 键重新开始', True, SUCCESS_COLOR)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 110))
        self.screen.blit(restart_text, restart_rect)
        
        quit_text = self.font_medium.render('按 ESC 键退出游戏', True, FAILURE_COLOR)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160))
        self.screen.blit(quit_text, quit_rect)
    
    def draw_click_effect(self):
        if self.click_effect:
            x, y, frame = self.click_effect
            if frame < 10:
                radius = 20 + frame * 5
                alpha = 255 - frame * 25
                pygame.draw.circle(self.screen, (50, 205, 50, alpha), (x, y), radius, 3)
                self.click_effect = (x, y, frame + 1)
            else:
                self.click_effect = None
    
    def run(self):
        while self.running:
            self.handle_events()
            
            self.screen.fill(BACKGROUND_COLOR)
            
            if not self.score_timer.game_over:
                self.score_timer.update()
                self.game_area.update(pygame.time.get_ticks())
            
            self.score_timer.draw(self.screen)
            self.game_area.draw(self.screen)
            
            self.draw_click_effect()
            
            if self.score_timer.game_over:
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()