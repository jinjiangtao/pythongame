
import pygame
import sys
import os
from constants import *
from map import GameMap
from pacman import Pacman
from ghost import Ghost
from sound_manager import SoundManager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("吃豆人")
        
        self.font = self._get_chinese_font()
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.game_map = GameMap()
        self.pacman = Pacman(self.game_map.get_pacman_start())
        
        ghost_starts = self.game_map.get_ghost_starts()
        self.ghosts = [
            Ghost(GHOST_RED, ghost_starts[0]),
            Ghost(GHOST_PINK, ghost_starts[1]),
            Ghost(GHOST_CYAN, ghost_starts[2]),
            Ghost(GHOST_ORANGE, ghost_starts[3])
        ]
        
        self.score = 0
        self.lives = INITIAL_LIVES
        self.level = 1
        self.ghost_eaten_count = 0
        self.game_state = GAME_STATE_PLAYING
        
        try:
            self.sound_manager = SoundManager()
        except:
            self.sound_manager = None

    def _get_chinese_font(self):
        font_size = 24
        possible_fonts = [
            "simhei.ttf",
            "msyh.ttc",
            "simsun.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simsun.ttc"
        ]
        
        for font_path in possible_fonts:
            try:
                if os.path.exists(font_path):
                    return pygame.font.Font(font_path, font_size)
            except:
                continue
        
        return pygame.font.Font(None, font_size)

    def reset_level(self):
        self.game_map.reset()
        self.pacman.reset()
        for ghost in self.ghosts:
            ghost.reset()
            ghost.speed = GHOST_SPEED + (self.level - 1) * 0.3
        self.ghost_eaten_count = 0

    def reset_game(self):
        self.score = 0
        self.lives = INITIAL_LIVES
        self.level = 1
        self.game_state = GAME_STATE_PLAYING
        self.reset_level()

    def check_collisions(self):
        grid_x, grid_y = self.pacman.get_grid_pos()
        cell = self.game_map.eat_dot(grid_x, grid_y)
        
        if cell == MAP_DOT:
            self.score += 10
            if self.sound_manager:
                self.sound_manager.play('dot')
        elif cell == MAP_POWER_PELLET:
            self.score += 50
            self.ghost_eaten_count = 0
            for ghost in self.ghosts:
                ghost.set_vulnerable()
            if self.sound_manager:
                self.sound_manager.play('power_pellet')
        
        pacman_x, pacman_y = self.pacman.get_pos()
        
        for ghost in self.ghosts:
            ghost_x, ghost_y = ghost.get_pos()
            dist = ((pacman_x - ghost_x) ** 2 + (pacman_y - ghost_y) ** 2) ** 0.5
            
            if dist < CELL_SIZE // 2:
                if ghost.is_vulnerable():
                    ghost.set_eaten()
                    self.ghost_eaten_count += 1
                    points = 200 * (2 ** (self.ghost_eaten_count - 1))
                    self.score += points
                    if self.sound_manager:
                        self.sound_manager.play('eat_ghost')
                elif not self.pacman.invincible and not ghost.is_eaten():
                    self.lives -= 1
                    if self.sound_manager:
                        self.sound_manager.play('death')
                    
                    if self.lives <= 0:
                        self.game_state = GAME_STATE_GAME_OVER
                    else:
                        self.pacman.reset()
                        self.pacman.set_invincible(120)
                        for ghost in self.ghosts:
                            ghost.reset()
                            ghost.speed = GHOST_SPEED + (self.level - 1) * 0.3
        
        if self.game_map.dots_remaining == 0:
            self.level += 1
            self.reset_level()

    def update(self):
        if self.game_state != GAME_STATE_PLAYING:
            return
        
        self.pacman.update(self.game_map)
        
        for i, ghost in enumerate(self.ghosts):
            red_pos = self.ghosts[0].get_grid_pos()
            ghost.update(
                self.game_map,
                self.pacman.get_grid_pos(),
                self.pacman.direction,
                red_pos,
                self.level
            )
        
        self.check_collisions()

    def draw(self):
        self.screen.fill(BLACK)
        
        self.game_map.draw(self.screen)
        
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        self.pacman.draw(self.screen)
        
        self.draw_ui()
        
        if self.game_state == GAME_STATE_GAME_OVER:
            self.draw_game_over()
        elif self.game_state == GAME_STATE_LEVEL_COMPLETE:
            pass
        
        pygame.display.flip()

    def draw_ui(self):
        score_text = self.font.render(f"得分: {self.score}", True, WHITE)
        lives_text = self.font.render(f"生命: {self.lives}", True, WHITE)
        level_text = self.font.render(f"关卡: {self.level}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (150, 10))
        self.screen.blit(level_text, (280, 10))

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("游戏结束!", True, RED)
        restart_text = self.font.render("按空格键重新开始", True, WHITE)
        
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(restart_text, restart_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if self.game_state == GAME_STATE_GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                else:
                    if event.key == pygame.K_UP:
                        self.pacman.set_next_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.pacman.set_next_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.pacman.set_next_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.set_next_direction(RIGHT)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
