import pygame
import sys
import random
import os
from enum import Enum

class CellState(Enum):
    HIDDEN = 0
    REVEALED = 1
    FLAGGED = 2

class GameStatus(Enum):
    READY = 0
    PLAYING = 1
    WON = 2
    LOST = 3

class MinesweeperGame:
    def __init__(self, width=9, height=9, mines=10):
        self.WIDTH = width
        self.HEIGHT = height
        self.MINES = mines
        self.CELL_SIZE = 30
        self.PADDING = 50
        
        self.screen_width = self.WIDTH * self.CELL_SIZE + self.PADDING
        self.screen_height = self.HEIGHT * self.CELL_SIZE + self.PADDING
        
        pygame.init()
        info = pygame.display.Info()
        screen_x = (info.current_w - self.screen_width) // 2
        screen_y = (info.current_h - self.screen_height) // 2
        
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{screen_x},{screen_y}"
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("扫雷游戏")
        
        pygame.display.flip()
        
        self.clock = pygame.time.Clock()
        
        font_names = ["msyh", "simhei", "simsun", "arial", "dejavusans"]
        self.font = None
        self.big_font = None
        
        for font_name in font_names:
            try:
                self.font = pygame.font.SysFont(font_name, 24)
                self.big_font = pygame.font.SysFont(font_name, 36)
                test_text = self.font.render("测试", True, (255, 255, 255))
                break
            except:
                continue
        
        if self.font is None:
            self.font = pygame.font.Font(None, 24)
            self.big_font = pygame.font.Font(None, 36)
        
        self.number_colors = {
            1: (0, 0, 255),
            2: (0, 128, 0),
            3: (255, 0, 0),
            4: (0, 0, 128),
            5: (128, 0, 0),
            6: (0, 128, 128),
            7: (0, 0, 0),
            8: (128, 128, 128)
        }
        
        self.reset_game()
    
    def reset_game(self):
        self.board = [[0 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.cell_states = [[CellState.HIDDEN for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.game_status = GameStatus.READY
        self.start_time = 0
        self.elapsed_time = 0
        self.mines_placed = False
        self.flag_count = 0
    
    def place_mines(self, exclude_x, exclude_y):
        mines_placed = 0
        while mines_placed < self.MINES:
            x = random.randint(0, self.WIDTH - 1)
            y = random.randint(0, self.HEIGHT - 1)
            
            if abs(x - exclude_x) <= 1 and abs(y - exclude_y) <= 1:
                continue
            
            if self.board[y][x] != -1:
                self.board[y][x] = -1
                mines_placed += 1
        
        self.calculate_numbers()
        self.mines_placed = True
    
    def calculate_numbers(self):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1),  (1, 0), (1, 1)]
        
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if self.board[y][x] == -1:
                    continue
                
                count = 0
                for dy, dx in directions:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < self.HEIGHT and 0 <= nx < self.WIDTH:
                        if self.board[ny][nx] == -1:
                            count += 1
                self.board[y][x] = count
    
    def reveal_cell(self, x, y):
        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            return
        
        if self.cell_states[y][x] != CellState.HIDDEN:
            return
        
        if not self.mines_placed:
            self.place_mines(x, y)
            self.game_status = GameStatus.PLAYING
            self.start_time = pygame.time.get_ticks()
        
        self.cell_states[y][x] = CellState.REVEALED
        
        if self.board[y][x] == -1:
            self.game_status = GameStatus.LOST
            self.reveal_all_mines()
            return
        
        if self.board[y][x] == 0:
            directions = [(-1, -1), (-1, 0), (-1, 1),
                          (0, -1),          (0, 1),
                          (1, -1),  (1, 0), (1, 1)]
            for dy, dx in directions:
                self.reveal_cell(x + dx, y + dy)
        
        self.check_win()
    
    def toggle_flag(self, x, y):
        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            return
        
        if self.cell_states[y][x] == CellState.HIDDEN:
            self.cell_states[y][x] = CellState.FLAGGED
            self.flag_count += 1
        elif self.cell_states[y][x] == CellState.FLAGGED:
            self.cell_states[y][x] = CellState.HIDDEN
            self.flag_count -= 1
    
    def reveal_all_mines(self):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if self.board[y][x] == -1:
                    self.cell_states[y][x] = CellState.REVEALED
    
    def check_win(self):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if self.board[y][x] != -1 and self.cell_states[y][x] != CellState.REVEALED:
                    return
        self.game_status = GameStatus.WON
    
    def draw_cell(self, x, y):
        cell_x = (x * self.CELL_SIZE) + (self.PADDING // 2)
        cell_y = (y * self.CELL_SIZE) + (self.PADDING // 2)
        rect = pygame.Rect(cell_x, cell_y, self.CELL_SIZE - 1, self.CELL_SIZE - 1)
        
        state = self.cell_states[y][x]
        value = self.board[y][x]
        
        if state == CellState.HIDDEN:
            pygame.draw.rect(self.screen, (192, 192, 192), rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
            pygame.draw.line(self.screen, (128, 128, 128), (cell_x, cell_y + self.CELL_SIZE - 1), (cell_x + self.CELL_SIZE - 1, cell_y + self.CELL_SIZE - 1))
            pygame.draw.line(self.screen, (128, 128, 128), (cell_x + self.CELL_SIZE - 1, cell_y), (cell_x + self.CELL_SIZE - 1, cell_y + self.CELL_SIZE - 1))
        elif state == CellState.FLAGGED:
            pygame.draw.rect(self.screen, (255, 0, 0), rect)
            flag_text = self.font.render("F", True, (255, 255, 255))
            self.screen.blit(flag_text, (cell_x + 8, cell_y + 4))
        elif state == CellState.REVEALED:
            pygame.draw.rect(self.screen, (220, 220, 220), rect)
            if value == -1:
                mine_text = self.font.render("*", True, (0, 0, 0))
                self.screen.blit(mine_text, (cell_x + 10, cell_y + 4))
            elif value > 0:
                num_text = self.font.render(str(value), True, self.number_colors[value])
                self.screen.blit(num_text, (cell_x + 8, cell_y + 4))
    
    def draw_top_bar(self):
        bar_rect = pygame.Rect(0, 0, self.screen_width, self.PADDING - 10)
        pygame.draw.rect(self.screen, (128, 128, 128), bar_rect)
        
        remaining_mines = self.MINES - self.flag_count
        mines_text = self.font.render(f"剩余地雷: {remaining_mines}", True, (255, 255, 255))
        self.screen.blit(mines_text, (10, 10))
        
        time_text = self.font.render(f"时间: {self.elapsed_time}s", True, (255, 255, 255))
        self.screen.blit(time_text, (self.screen_width - 120, 10))
        
        status_text = ""
        if self.game_status == GameStatus.READY:
            status_text = "点击开始游戏"
        elif self.game_status == GameStatus.PLAYING:
            status_text = "游戏中..."
        elif self.game_status == GameStatus.WON:
            status_text = "恭喜获胜！"
        elif self.game_status == GameStatus.LOST:
            status_text = "游戏结束"
        
        status_surface = self.font.render(status_text, True, (255, 255, 255))
        status_x = (self.screen_width - status_surface.get_width()) // 2
        self.screen.blit(status_surface, (status_x, 10))
    
    def draw_game_over_popup(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        if self.game_status == GameStatus.WON:
            title_text = self.big_font.render("🎉 恭喜获胜！", True, (0, 255, 0))
        else:
            title_text = self.big_font.render("💥 游戏结束", True, (255, 0, 0))
        
        title_x = (self.screen_width - title_text.get_width()) // 2
        title_y = self.screen_height // 2 - 60
        self.screen.blit(title_text, (title_x, title_y))
        
        time_text = self.font.render(f"用时: {self.elapsed_time}秒", True, (255, 255, 255))
        time_x = (self.screen_width - time_text.get_width()) // 2
        time_y = self.screen_height // 2 - 10
        self.screen.blit(time_text, (time_x, time_y))
        
        restart_text = self.font.render("按 R 键重新开始", True, (0, 255, 255))
        restart_x = (self.screen_width - restart_text.get_width()) // 2
        restart_y = self.screen_height // 2 + 30
        self.screen.blit(restart_text, (restart_x, restart_y))
        
        quit_text = self.font.render("按 Q 键退出游戏", True, (255, 165, 0))
        quit_x = (self.screen_width - quit_text.get_width()) // 2
        quit_y = self.screen_height // 2 + 60
        self.screen.blit(quit_text, (quit_x, quit_y))
    
    def run(self):
        running = True
        while running:
            self.screen.fill((128, 128, 128))
            
            if self.game_status == GameStatus.PLAYING:
                current_time = pygame.time.get_ticks()
                self.elapsed_time = (current_time - self.start_time) // 1000
            
            self.draw_top_bar()
            
            for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    self.draw_cell(x, y)
            
            if self.game_status in (GameStatus.WON, GameStatus.LOST):
                self.draw_game_over_popup()
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_status in (GameStatus.WON, GameStatus.LOST):
                        continue
                    
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    cell_x = (mouse_x - self.PADDING // 2) // self.CELL_SIZE
                    cell_y = (mouse_y - self.PADDING // 2) // self.CELL_SIZE
                    
                    if 0 <= cell_x < self.WIDTH and 0 <= cell_y < self.HEIGHT:
                        if event.button == 1:
                            self.reveal_cell(cell_x, cell_y)
                        elif event.button == 3:
                            if self.game_status == GameStatus.READY:
                                self.game_status = GameStatus.PLAYING
                                self.start_time = pygame.time.get_ticks()
                            self.toggle_flag(cell_x, cell_y)
            
            self.clock.tick(30)
        
        pygame.quit()
        sys.exit()

def main():
    width, height, mines = 9, 9, 10
    
    game = MinesweeperGame(width, height, mines)
    game.run()

if __name__ == "__main__":
    main()
