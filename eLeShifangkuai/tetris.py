"""
俄罗斯方块游戏 - Tetris Game
使用Python + pygame开发的经典俄罗斯方块游戏
单文件实现，代码规范，注释清晰，可直接运行
"""

import pygame
import random
import sys
from enum import Enum
from typing import List, Tuple, Optional

# ============================================================================
# 常量配置模块
# ============================================================================

class GameConfig:
    """游戏配置类"""
    # 游戏窗口尺寸
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    
    # 游戏板尺寸 (列数 x 行数)
    BOARD_COLS = 10
    BOARD_ROWS = 20
    
    # 方块单元大小
    BLOCK_SIZE = 30
    
    # 游戏板位置
    BOARD_X = 50
    BOARD_Y = 50
    
    # 右侧信息面板起始位置
    INFO_PANEL_X = BOARD_X + BOARD_COLS * BLOCK_SIZE + 50
    
    # 颜色定义
    COLORS = {
        'background': (30, 30, 40),
        'board_bg': (20, 20, 30),
        'grid_line': (40, 40, 50),
        'text': (255, 255, 255),
        'text_highlight': (255, 200, 100),
    }
    
    # 7种经典方块的颜色
    PIECE_COLORS = [
        (255, 0, 0),      # I型 - 红色
        (0, 255, 255),    # O型 - 青色
        (255, 255, 0),    # T型 - 黄色
        (128, 0, 128),    # S型 - 紫色
        (0, 255, 0),      # Z型 - 绿色
        (0, 0, 255),      # J型 - 蓝色
        (255, 165, 0),    # L型 - 橙色
    ]
    
    # 方块形状定义 (每个方块有4个旋转状态)
    PIECE_SHAPES = [
        # I型
        [[(0,1), (1,1), (2,1), (3,1)],
         [(1,0), (1,1), (1,2), (1,3)],
         [(0,1), (1,1), (2,1), (3,1)],
         [(1,0), (1,1), (1,2), (1,3)]],
        # O型
        [[(0,0), (0,1), (1,0), (1,1)],
         [(0,0), (0,1), (1,0), (1,1)],
         [(0,0), (0,1), (1,0), (1,1)],
         [(0,0), (0,1), (1,0), (1,1)]],
        # T型
        [[(0,1), (1,0), (1,1), (1,2)],
         [(0,1), (1,1), (1,2), (2,1)],
         [(1,0), (1,1), (1,2), (2,1)],
         [(0,1), (1,0), (1,1), (2,1)]],
        # S型
        [[(0,1), (0,2), (1,0), (1,1)],
         [(0,0), (1,0), (1,1), (2,1)],
         [(1,1), (1,2), (2,0), (2,1)],
         [(0,0), (1,0), (1,1), (2,1)]],
        # Z型
        [[(0,0), (0,1), (1,1), (1,2)],
         [(0,2), (1,1), (1,2), (2,1)],
         [(1,0), (1,1), (2,1), (2,2)],
         [(0,1), (1,0), (1,1), (2,0)]],
        # J型
        [[(0,0), (1,0), (1,1), (1,2)],
         [(0,1), (0,2), (1,1), (2,1)],
         [(1,0), (1,1), (1,2), (2,2)],
         [(0,1), (1,1), (2,0), (2,1)]],
        # L型
        [[(0,2), (1,0), (1,1), (1,2)],
         [(0,1), (1,1), (2,1), (2,2)],
         [(1,0), (1,1), (1,2), (2,0)],
         [(0,0), (0,1), (1,1), (2,1)]],
    ]
    
    # 难度等级对应的下落速度 (毫秒)
    SPEED_LEVELS = [
        800,   # 等级1
        650,   # 等级2
        500,   # 等级3
        400,   # 等级4
        300,   # 等级5
        200,   # 等级6
        150,   # 等级7
        120,   # 等级8
        100,   # 等级9
        80,    # 等级10
    ]
    
    # 消除行数对应的分数
    SCORE_VALUES = {
        1: 100,   # 消除1行
        2: 300,   # 消除2行
        3: 500,   # 消除3行
        4: 800,   # 消除4行 (满堂红)
    }


class GameState(Enum):
    """游戏状态枚举"""
    READY = 0      # 准备开始
    PLAYING = 1    # 游戏中
    PAUSED = 2     # 暂停
    GAME_OVER = 3  # 游戏结束


# ============================================================================
# 方块类模块
# ============================================================================

class Piece:
    """方块类 - 表示一个俄罗斯方块"""
    
    def __init__(self, piece_type: int):
        """
        初始化方块
        
        Args:
            piece_type: 方块类型 (0-6 对应7种经典方块)
        """
        self.piece_type = piece_type
        self.color = GameConfig.PIECE_COLORS[piece_type]
        self.rotation = 0
        self.x = GameConfig.BOARD_COLS // 2 - 2
        self.y = 0
    
    def get_blocks(self) -> List[Tuple[int, int]]:
        """
        获取方块当前状态的所有单元格位置
        
        Returns:
            方块单元格相对位置列表
        """
        return GameConfig.PIECE_SHAPES[self.piece_type][self.rotation]
    
    def get_absolute_positions(self) -> List[Tuple[int, int]]:
        """
        获取方块在游戏板上的绝对位置
        
        Returns:
            绝对位置列表 (x, y)
        """
        blocks = self.get_blocks()
        return [(self.x + bx, self.y + by) for bx, by in blocks]
    
    def rotate(self) -> None:
        """顺时针旋转方块"""
        self.rotation = (self.rotation + 1) % 4
    
    def move_left(self) -> None:
        """向左移动"""
        self.x -= 1
    
    def move_right(self) -> None:
        """向右移动"""
        self.x += 1
    
    def move_down(self) -> None:
        """向下移动"""
        self.y += 1
    
    def move_up(self) -> None:
        """向上移动 (用于快速落底后的修正)"""
        self.y -= 1


# ============================================================================
# 游戏板类模块
# ============================================================================

class GameBoard:
    """游戏板类 - 管理游戏区域内的所有方块"""
    
    def __init__(self):
        """初始化游戏板"""
        self.width = GameConfig.BOARD_COLS
        self.height = GameConfig.BOARD_ROWS
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def is_valid_position(self, piece: Piece) -> bool:
        """
        检查方块位置是否有效
        
        Args:
            piece: 要检查的方块
            
        Returns:
            是否有效
        """
        for x, y in piece.get_absolute_positions():
            if x < 0 or x >= self.width or y >= self.height:
                return False
            if y >= 0 and self.grid[y][x] is not None:
                return False
        return True
    
    def lock_piece(self, piece: Piece) -> None:
        """
        将方块锁定到游戏板
        
        Args:
            piece: 要锁定的方块
        """
        for x, y in piece.get_absolute_positions():
            if 0 <= y < self.height and 0 <= x < self.width:
                self.grid[y][x] = piece.color
    
    def clear_lines(self) -> int:
        """
        清除已填满的行
        
        Returns:
            清除的行数
        """
        lines_cleared = 0
        y = self.height - 1
        
        while y >= 0:
            if all(cell is not None for cell in self.grid[y]):
                lines_cleared += 1
                del self.grid[y]
                self.grid.insert(0, [None for _ in range(self.width)])
            else:
                y -= 1
        
        return lines_cleared
    
    def is_game_over(self) -> bool:
        """
        检查游戏是否结束 (顶部有方块)
        
        Returns:
            是否游戏结束
        """
        return any(cell is not None for cell in self.grid[0])
    
    def reset(self) -> None:
        """重置游戏板"""
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]


# ============================================================================
# 游戏控制器类模块
# ============================================================================

class GameController:
    """游戏控制器 - 管理游戏逻辑和状态"""
    
    def __init__(self):
        """初始化游戏控制器"""
        pygame.init()
        pygame.display.set_caption('俄罗斯方块 - Tetris')
        
        self.screen = pygame.display.set_mode(
            (GameConfig.WINDOW_WIDTH, GameConfig.WINDOW_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 24)
        
        self.board = GameBoard()
        self.current_piece: Optional[Piece] = None
        self.next_piece: Optional[Piece] = None
        self.state = GameState.READY
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        
        self.last_drop_time = 0
        self.drop_speed = GameConfig.SPEED_LEVELS[0]
        
        self._generate_next_piece()
    
    def _generate_next_piece(self) -> None:
        """生成下一个方块"""
        self.next_piece = Piece(random.randint(0, 6))
    
    def spawn_piece(self) -> bool:
        """
        生成新方块
        
        Returns:
            是否成功生成 (失败则游戏结束)
        """
        self.current_piece = self.next_piece
        self.current_piece.x = GameConfig.BOARD_COLS // 2 - 2
        self.current_piece.y = 0
        
        self._generate_next_piece()
        
        if not self.board.is_valid_position(self.current_piece):
            self.state = GameState.GAME_OVER
            return False
        
        return True
    
    def move_piece(self, dx: int, dy: int) -> bool:
        """
        移动方块
        
        Args:
            dx: X方向移动量
            dy: Y方向移动量
            
        Returns:
            是否移动成功
        """
        if self.current_piece is None or self.state != GameState.PLAYING:
            return False
        
        original_x = self.current_piece.x
        original_y = self.current_piece.y
        
        self.current_piece.x += dx
        self.current_piece.y += dy
        
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.x = original_x
            self.current_piece.y = original_y
            return False
        
        return True
    
    def rotate_piece(self) -> bool:
        """
        旋转方块
        
        Returns:
            是否旋转成功
        """
        if self.current_piece is None or self.state != GameState.PLAYING:
            return False
        
        original_rotation = self.current_piece.rotation
        self.current_piece.rotate()
        
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.rotation = original_rotation
            return False
        
        return True
    
    def drop_piece(self) -> bool:
        """
        让方块下落一行
        
        Returns:
            方块是否成功下落
        """
        return self.move_piece(0, 1)
    
    def instant_drop(self) -> None:
        """快速落底 - 方块直接落到底部"""
        if self.current_piece is None or self.state != GameState.PLAYING:
            return
        
        while self.move_piece(0, 1):
            pass
        
        self._lock_current_piece()
    
    def _lock_current_piece(self) -> None:
        """锁定当前方块并处理消除"""
        if self.current_piece is None:
            return
        
        self.board.lock_piece(self.current_piece)
        lines = self.board.clear_lines()
        
        if lines > 0:
            self.lines_cleared += lines
            self.score += GameConfig.SCORE_VALUES.get(lines, 0) * self.level
            self._update_level()
        
        self.spawn_piece()
    
    def _update_level(self) -> None:
        """更新游戏等级"""
        self.level = min(10, self.lines_cleared // 10 + 1)
        self.drop_speed = GameConfig.SPEED_LEVELS[self.level - 1]
    
    def handle_events(self) -> None:
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = GameState.GAME_OVER
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
    
    def _handle_keydown(self, key: int) -> None:
        """处理键盘按下事件"""
        if key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        
        if self.state == GameState.READY:
            if key == pygame.K_RETURN or key == pygame.K_SPACE:
                self._start_game()
        
        elif self.state == GameState.PLAYING:
            if key == pygame.K_LEFT:
                self.move_piece(-1, 0)
            elif key == pygame.K_RIGHT:
                self.move_piece(1, 0)
            elif key == pygame.K_UP:
                self.rotate_piece()
            elif key == pygame.K_DOWN:
                self.drop_piece()
            elif key == pygame.K_SPACE:
                self.instant_drop()
            elif key == pygame.K_p or key == pygame.K_PAUSE:
                self.state = GameState.PAUSED
        
        elif self.state == GameState.PAUSED:
            if key == pygame.K_p or key == pygame.K_PAUSE or key == pygame.K_RETURN:
                self.state = GameState.PLAYING
        
        elif self.state == GameState.GAME_OVER:
            if key == pygame.K_RETURN or key == pygame.K_SPACE:
                self._restart_game()
    
    def _start_game(self) -> None:
        """开始游戏"""
        self.board.reset()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.drop_speed = GameConfig.SPEED_LEVELS[0]
        self.state = GameState.PLAYING
        self.spawn_piece()
    
    def _restart_game(self) -> None:
        """重新开始游戏"""
        self._start_game()
    
    def update(self, current_time: int) -> None:
        """
        更新游戏逻辑
        
        Args:
            current_time: 当前时间 (毫秒)
        """
        if self.state != GameState.PLAYING:
            return
        
        if current_time - self.last_drop_time > self.drop_speed:
            if not self.drop_piece():
                self._lock_current_piece()
            self.last_drop_time = current_time
    
    def _draw_block(self, x: int, y: int, color: Tuple[int, int, int], 
                   highlight: bool = False) -> None:
        """
        绘制单个方块
        
        Args:
            x: X坐标
            y: Y坐标
            color: 颜色
            highlight: 是否高亮边框
        """
        rect = pygame.Rect(x, y, GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE)
        
        pygame.draw.rect(self.screen, color, rect)
        
        pygame.draw.rect(self.screen, 
                        tuple(min(255, c + 50) for c in color), 
                        rect, 2)
        
        if highlight:
            pygame.draw.line(self.screen, (255, 255, 255),
                           (x, y), (x + GameConfig.BLOCK_SIZE, y), 2)
    
    def _draw_board(self) -> None:
        """绘制游戏板"""
        board_rect = pygame.Rect(
            GameConfig.BOARD_X,
            GameConfig.BOARD_Y,
            GameConfig.BOARD_COLS * GameConfig.BLOCK_SIZE,
            GameConfig.BOARD_ROWS * GameConfig.BLOCK_SIZE
        )
        pygame.draw.rect(self.screen, GameConfig.COLORS['board_bg'], board_rect)
        pygame.draw.rect(self.screen, GameConfig.COLORS['grid_line'], 
                        board_rect, 2)
        
        for y in range(GameConfig.BOARD_ROWS):
            for x in range(GameConfig.BOARD_COLS):
                if self.board.grid[y][x]:
                    self._draw_block(
                        GameConfig.BOARD_X + x * GameConfig.BLOCK_SIZE,
                        GameConfig.BOARD_Y + y * GameConfig.BLOCK_SIZE,
                        self.board.grid[y][x]
                    )
    
    def _draw_current_piece(self) -> None:
        """绘制当前下落的方块"""
        if self.current_piece is None:
            return
        
        for x, y in self.current_piece.get_absolute_positions():
            if y >= 0:
                self._draw_block(
                    GameConfig.BOARD_X + x * GameConfig.BLOCK_SIZE,
                    GameConfig.BOARD_Y + y * GameConfig.BLOCK_SIZE,
                    self.current_piece.color,
                    highlight=True
                )
    
    def _draw_next_piece_preview(self) -> None:
        """绘制下一个方块预览"""
        preview_x = GameConfig.INFO_PANEL_X
        preview_y = GameConfig.BOARD_Y + 50
        
        label = self.font.render('下一个:', True, GameConfig.COLORS['text'])
        self.screen.blit(label, (preview_x, preview_y))
        
        if self.next_piece:
            preview_block_size = 20
            offset_x = preview_x + 30
            offset_y = preview_y + 40
            
            for bx, by in self.next_piece.get_blocks():
                rect = pygame.Rect(
                    offset_x + bx * preview_block_size,
                    offset_y + by * preview_block_size,
                    preview_block_size,
                    preview_block_size
                )
                pygame.draw.rect(self.screen, self.next_piece.color, rect)
                pygame.draw.rect(self.screen, 
                               tuple(min(255, c + 50) for c in self.next_piece.color), 
                               rect, 1)
    
    def _draw_score_info(self) -> None:
        """绘制分数信息"""
        info_x = GameConfig.INFO_PANEL_X
        info_y = GameConfig.BOARD_Y + 180
        
        score_label = self.font.render('得分:', True, GameConfig.COLORS['text'])
        self.screen.blit(score_label, (info_x, info_y))
        
        score_value = self.font_large.render(str(self.score), True, 
                                            GameConfig.COLORS['text_highlight'])
        self.screen.blit(score_value, (info_x, info_y + 30))
        
        level_label = self.font.render('等级:', True, GameConfig.COLORS['text'])
        self.screen.blit(level_label, (info_x, info_y + 80))
        
        level_value = self.font.render(str(self.level), True, 
                                      GameConfig.COLORS['text_highlight'])
        self.screen.blit(level_value, (info_x, info_y + 110))
        
        lines_label = self.font.render('消除行数:', True, GameConfig.COLORS['text'])
        self.screen.blit(lines_label, (info_x, info_y + 150))
        
        lines_value = self.font.render(str(self.lines_cleared), True, 
                                      GameConfig.COLORS['text_highlight'])
        self.screen.blit(lines_value, (info_x, info_y + 180))
    
    def _draw_controls(self) -> None:
        """绘制操作说明"""
        info_x = GameConfig.INFO_PANEL_X
        info_y = GameConfig.BOARD_Y + 420
        
        controls = [
            '操作说明:',
            '← → : 移动',
            '↑ : 旋转',
            '↓ : 加速下落',
            '空格 : 快速落底',
            'P : 暂停/继续',
            'ESC : 退出'
        ]
        
        for i, text in enumerate(controls):
            if i == 0:
                label = self.font.render(text, True, GameConfig.COLORS['text_highlight'])
            else:
                label = self.font_small.render(text, True, GameConfig.COLORS['text'])
            self.screen.blit(label, (info_x, info_y + i * 25))
    
    def _draw_game_state(self) -> None:
        """绘制游戏状态提示"""
        if self.state == GameState.READY:
            text = self.font_large.render('按回车或空格开始', True, 
                                         GameConfig.COLORS['text_highlight'])
            text_rect = text.get_rect(center=(
                GameConfig.BOARD_X + GameConfig.BOARD_COLS * GameConfig.BLOCK_SIZE // 2,
                GameConfig.BOARD_Y + GameConfig.BOARD_ROWS * GameConfig.BLOCK_SIZE // 2
            ))
            self.screen.blit(text, text_rect)
        
        elif self.state == GameState.PAUSED:
            overlay = pygame.Surface(
                (GameConfig.BOARD_COLS * GameConfig.BLOCK_SIZE,
                 GameConfig.BOARD_ROWS * GameConfig.BLOCK_SIZE),
                pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (GameConfig.BOARD_X, GameConfig.BOARD_Y))
            
            text = self.font_large.render('游戏暂停', True, 
                                         GameConfig.COLORS['text_highlight'])
            text_rect = text.get_rect(center=(
                GameConfig.BOARD_X + GameConfig.BOARD_COLS * GameConfig.BLOCK_SIZE // 2,
                GameConfig.BOARD_Y + GameConfig.BOARD_ROWS * GameConfig.BLOCK_SIZE // 2
            ))
            self.screen.blit(text, text_rect)
            
            hint = self.font_small.render('按 P 继续', True, GameConfig.COLORS['text'])
            hint_rect = hint.get_rect(center=(
                GameConfig.BOARD_X + GameConfig.BOARD_COLS * GameConfig.BLOCK_SIZE // 2,
                GameConfig.BOARD_Y + GameConfig.BOARD_ROWS * GameConfig.BLOCK_SIZE // 2 + 40
            ))
            self.screen.blit(hint, hint_rect)
        
        elif self.state == GameState.GAME_OVER:
            overlay = pygame.Surface(
                (GameConfig.BOARD_COLS * GameConfig.BLOCK_SIZE,
                 GameConfig.BOARD_ROWS * GameConfig.BLOCK_SIZE),
                pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (GameConfig.BOARD_X, GameConfig.BOARD_Y))
            
            text = self.font_large.render('游戏结束', True, (255, 100, 100))
            text_rect = text.get_rect(center=(
                GameConfig.BOARD_X + GameConfig.BOARD_COLS * GameConfig.BLOCK_SIZE // 2,
                GameConfig.BOARD_Y + GameConfig.BOARD_ROWS * GameConfig.BLOCK_SIZE // 2 - 20
            ))
            self.screen.blit(text, text_rect)
            
            final_score = self.font.render(f'最终得分: {self.score}', True, 
                                         GameConfig.COLORS['text_highlight'])
            score_rect = final_score.get_rect(center=(
                GameConfig.BOARD_X + GameConfig.BOARD_COLS * GameConfig.BLOCK_SIZE // 2,
                GameConfig.BOARD_Y + GameConfig.BOARD_ROWS * GameConfig.BLOCK_SIZE // 2 + 20
            ))
            self.screen.blit(final_score, score_rect)
            
            hint = self.font_small.render('按回车重新开始', True, GameConfig.COLORS['text'])
            hint_rect = hint.get_rect(center=(
                GameConfig.BOARD_X + GameConfig.BOARD_COLS * GameConfig.BLOCK_SIZE // 2,
                GameConfig.BOARD_Y + GameConfig.BOARD_ROWS * GameConfig.BLOCK_SIZE // 2 + 60
            ))
            self.screen.blit(hint, hint_rect)
    
    def render(self) -> None:
        """渲染所有游戏元素"""
        self.screen.fill(GameConfig.COLORS['background'])
        
        title = self.font_large.render('俄罗斯方块', True, 
                                      GameConfig.COLORS['text_highlight'])
        self.screen.blit(title, (GameConfig.INFO_PANEL_X, 10))
        
        self._draw_board()
        self._draw_current_piece()
        self._draw_next_piece_preview()
        self._draw_score_info()
        self._draw_controls()
        self._draw_game_state()
        
        pygame.display.flip()
    
    def run(self) -> None:
        """主游戏循环"""
        running = True
        
        while running:
            current_time = pygame.time.get_ticks()
            
            self.handle_events()
            self.update(current_time)
            self.render()
            
            self.clock.tick(60)
            
            if self.state == GameState.GAME_OVER and \
               not any(pygame.event.get(pygame.QUIT)):
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                            self._restart_game()
                        elif event.key == pygame.K_ESCAPE:
                            running = False
        
        pygame.quit()


# ============================================================================
# 主程序入口
# ============================================================================

if __name__ == '__main__':
    game = GameController()
    game.run()
