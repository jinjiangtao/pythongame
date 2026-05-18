import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BLOCK_SIZE = 25
GRID_WIDTH = 10
GRID_HEIGHT = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)

COLORS = [
    (0, 255, 255),   
    (255, 0, 0),     
    (0, 255, 0),     
    (0, 0, 255),     
    (255, 255, 0),   
    (255, 165, 0),   
    (128, 0, 128)    
]

SHAPES = [
    [[1, 1, 1, 1]],
    
    [[1, 1],
     [1, 1]],
    
    [[0, 1, 0],
     [1, 1, 1]],
    
    [[0, 1, 1],
     [1, 1, 0]],
    
    [[1, 1, 0],
     [0, 1, 1]],
    
    [[1, 0, 0],
     [1, 1, 1]],
    
    [[0, 0, 1],
     [1, 1, 1]]
]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("俄罗斯方块")
        
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        self.reset_game()
        self.draw_initial_screen()
    
    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        
        self.base_speed = 1000
        self.last_drop_time = pygame.time.get_ticks()
    
    def new_piece(self):
        shape_idx = random.randint(0, len(SHAPES) - 1)
        return {
            'shape': SHAPES[shape_idx],
            'color': COLORS[shape_idx],
            'x': GRID_WIDTH // 2 - len(SHAPES[shape_idx][0]) // 2,
            'y': 0
        }
    
    def draw_initial_screen(self):
        self.screen.fill(BLACK)
        
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("俄罗斯方块", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        start_font = pygame.font.Font(None, 32)
        start_text = start_font.render("按 空格键 开始游戏", True, LIGHT_GRAY)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(start_text, start_rect)
        
        controls_font = pygame.font.Font(None, 24)
        controls_lines = [
            "← → 移动",
            "↑ 旋转",
            "↓ 加速下落",
            "空格 快速落底",
            "P 暂停/继续",
            "R 重新开始",
            "ESC 退出"
        ]
        y_pos = 320
        for line in controls_lines:
            text = controls_font.render(line, True, LIGHT_GRAY)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            self.screen.blit(text, rect)
            y_pos += 30
        
        pygame.display.update()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
    
    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = self.grid[y][x]
                rect = pygame.Rect(
                    x * BLOCK_SIZE,
                    y * BLOCK_SIZE,
                    BLOCK_SIZE - 1,
                    BLOCK_SIZE - 1
                )
                pygame.draw.rect(self.screen, color, rect)
    
    def draw_piece(self, piece, offset_x=0, offset_y=0):
        shape = piece['shape']
        color = piece['color']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        (piece['x'] + x + offset_x) * BLOCK_SIZE,
                        (piece['y'] + y + offset_y) * BLOCK_SIZE,
                        BLOCK_SIZE - 1,
                        BLOCK_SIZE - 1
                    )
                    pygame.draw.rect(self.screen, color, rect)
    
    def draw_next_piece(self):
        next_x = GRID_WIDTH + 2
        next_y = 2
        
        title_font = pygame.font.Font(None, 24)
        title_text = title_font.render("下一个", True, WHITE)
        title_rect = title_text.get_rect(topleft=(next_x * BLOCK_SIZE, next_y * BLOCK_SIZE - 30))
        self.screen.blit(title_text, title_rect)
        
        shape = self.next_piece['shape']
        color = self.next_piece['color']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        (next_x + x) * BLOCK_SIZE,
                        (next_y + y) * BLOCK_SIZE,
                        BLOCK_SIZE - 1,
                        BLOCK_SIZE - 1
                    )
                    pygame.draw.rect(self.screen, color, rect)
    
    def draw_score(self):
        score_x = GRID_WIDTH + 2
        score_y = 10
        
        font = pygame.font.Font(None, 24)
        
        score_text = font.render(f"得分: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(topleft=(score_x * BLOCK_SIZE, score_y * BLOCK_SIZE))
        self.screen.blit(score_text, score_rect)
        
        level_text = font.render(f"等级: {self.level}", True, WHITE)
        level_rect = level_text.get_rect(topleft=(score_x * BLOCK_SIZE, (score_y + 2) * BLOCK_SIZE))
        self.screen.blit(level_text, level_rect)
        
        lines_text = font.render(f"消除: {self.lines_cleared}", True, WHITE)
        lines_rect = lines_text.get_rect(topleft=(score_x * BLOCK_SIZE, (score_y + 4) * BLOCK_SIZE))
        self.screen.blit(lines_text, lines_rect)
    
    def draw_game_over(self):
        overlay = pygame.Surface((GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 48)
        text = font.render("游戏结束", True, WHITE)
        rect = text.get_rect(center=(GRID_WIDTH * BLOCK_SIZE // 2, GRID_HEIGHT * BLOCK_SIZE // 2 - 30))
        self.screen.blit(text, rect)
        
        font = pygame.font.Font(None, 24)
        text = font.render(f"最终得分: {self.score}", True, WHITE)
        rect = text.get_rect(center=(GRID_WIDTH * BLOCK_SIZE // 2, GRID_HEIGHT * BLOCK_SIZE // 2 + 10))
        self.screen.blit(text, rect)
        
        text = font.render("按 R 重新开始", True, LIGHT_GRAY)
        rect = text.get_rect(center=(GRID_WIDTH * BLOCK_SIZE // 2, GRID_HEIGHT * BLOCK_SIZE // 2 + 50))
        self.screen.blit(text, rect)
    
    def draw_paused(self):
        overlay = pygame.Surface((GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 48)
        text = font.render("暂停", True, WHITE)
        rect = text.get_rect(center=(GRID_WIDTH * BLOCK_SIZE // 2, GRID_HEIGHT * BLOCK_SIZE // 2))
        self.screen.blit(text, rect)
        
        font = pygame.font.Font(None, 24)
        text = font.render("按 P 继续", True, LIGHT_GRAY)
        rect = text.get_rect(center=(GRID_WIDTH * BLOCK_SIZE // 2, GRID_HEIGHT * BLOCK_SIZE // 2 + 40))
        self.screen.blit(text, rect)
    
    def draw_right_panel(self):
        panel_rect = pygame.Rect(
            GRID_WIDTH * BLOCK_SIZE,
            0,
            SCREEN_WIDTH - GRID_WIDTH * BLOCK_SIZE,
            SCREEN_HEIGHT
        )
        pygame.draw.rect(self.screen, GRAY, panel_rect)
    
    def is_valid_move(self, piece, offset_x=0, offset_y=0):
        shape = piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece['x'] + x + offset_x
                    new_y = piece['y'] + y + offset_y
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        return True
    
    def rotate_piece(self):
        shape = self.current_piece['shape']
        rotated = list(zip(*shape[::-1]))
        rotated = [list(row) for row in rotated]
        
        original_shape = self.current_piece['shape']
        self.current_piece['shape'] = rotated
        
        kicks = [0, 1, -1, 2, -2]
        for kick in kicks:
            if self.is_valid_move(self.current_piece, kick, 0):
                self.current_piece['x'] += kick
                return
        self.current_piece['shape'] = original_shape
    
    def lock_piece(self):
        shape = self.current_piece['shape']
        color = self.current_piece['color']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = color
        
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        
        if not self.is_valid_move(self.current_piece):
            self.game_over = True
    
    def clear_lines(self):
        lines_cleared = 0
        new_grid = []
        
        for row in self.grid:
            if all(cell != 0 for cell in row):
                lines_cleared += 1
            else:
                new_grid.append(row)
        
        for _ in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        self.grid = new_grid
        
        if lines_cleared > 0:
            self.lines_cleared += lines_cleared
            points = [0, 100, 300, 500, 800]
            self.score += points[lines_cleared] * self.level
            self.level = self.lines_cleared // 10 + 1
    
    def drop_piece(self):
        if self.is_valid_move(self.current_piece, 0, 1):
            self.current_piece['y'] += 1
        else:
            self.lock_piece()
    
    def hard_drop(self):
        while self.is_valid_move(self.current_piece, 0, 1):
            self.current_piece['y'] += 1
            self.score += 2
        self.lock_piece()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    continue
                
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                
                if self.paused:
                    continue
                
                if event.key == pygame.K_r:
                    self.reset_game()
                
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                if event.key == pygame.K_LEFT:
                    if self.is_valid_move(self.current_piece, -1, 0):
                        self.current_piece['x'] -= 1
                
                if event.key == pygame.K_RIGHT:
                    if self.is_valid_move(self.current_piece, 1, 0):
                        self.current_piece['x'] += 1
                
                if event.key == pygame.K_UP:
                    self.rotate_piece()
                
                if event.key == pygame.K_DOWN:
                    if self.is_valid_move(self.current_piece, 0, 1):
                        self.current_piece['y'] += 1
                        self.score += 1
                
                if event.key == pygame.K_SPACE:
                    self.hard_drop()
    
    def update(self):
        if self.game_over or self.paused:
            return
        
        current_time = pygame.time.get_ticks()
        speed = max(100, self.base_speed - (self.level - 1) * 100)
        
        if current_time - self.last_drop_time >= speed:
            self.drop_piece()
            self.last_drop_time = current_time
    
    def draw(self):
        self.screen.fill(BLACK)
        
        self.draw_right_panel()
        self.draw_grid()
        self.draw_piece(self.current_piece)
        self.draw_next_piece()
        self.draw_score()
        
        if self.game_over:
            self.draw_game_over()
        elif self.paused:
            self.draw_paused()
        
        pygame.display.update()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = Tetris()
    game.run()
