"""
俄罗斯方块游戏测试用例
测试游戏的核心功能模块
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import pygame
from tetris import Piece, GameBoard, GameController, GameConfig, GameState


class TestPiece(unittest.TestCase):
    """测试方块类"""
    
    def setUp(self):
        """测试前准备"""
        self.piece = Piece(0)
    
    def test_piece_initialization(self):
        """测试方块初始化"""
        self.assertEqual(self.piece.piece_type, 0)
        self.assertEqual(self.piece.rotation, 0)
        self.assertEqual(self.piece.x, GameConfig.BOARD_COLS // 2 - 2)
        self.assertEqual(self.piece.y, 0)
        self.assertIsNotNone(self.piece.color)
    
    def test_piece_get_blocks(self):
        """测试获取方块单元格"""
        blocks = self.piece.get_blocks()
        self.assertIsInstance(blocks, list)
        self.assertEqual(len(blocks), 4)
        for block in blocks:
            self.assertIsInstance(block, tuple)
            self.assertEqual(len(block), 2)
    
    def test_piece_rotation(self):
        """测试方块旋转"""
        original_blocks = self.piece.get_blocks()
        self.piece.rotate()
        rotated_blocks = self.piece.get_blocks()
        self.assertNotEqual(original_blocks, rotated_blocks)
        self.assertEqual(self.piece.rotation, 1)
    
    def test_piece_full_rotation(self):
        """测试方块完整旋转一圈"""
        for i in range(4):
            self.piece.rotate()
        self.assertEqual(self.piece.rotation, 0)
    
    def test_piece_movement(self):
        """测试方块移动"""
        original_x = self.piece.x
        self.piece.move_left()
        self.assertEqual(self.piece.x, original_x - 1)
        
        self.piece.move_right()
        self.assertEqual(self.piece.x, original_x)
        
        original_y = self.piece.y
        self.piece.move_down()
        self.assertEqual(self.piece.y, original_y + 1)
    
    def test_get_absolute_positions(self):
        """测试获取绝对位置"""
        positions = self.piece.get_absolute_positions()
        self.assertEqual(len(positions), 4)
        for x, y in positions:
            self.assertGreaterEqual(x, self.piece.x)
            self.assertGreaterEqual(y, self.piece.y)
    
    def test_all_piece_types(self):
        """测试所有7种方块类型"""
        for piece_type in range(7):
            piece = Piece(piece_type)
            self.assertEqual(piece.piece_type, piece_type)
            self.assertIsNotNone(piece.color)
            blocks = piece.get_blocks()
            self.assertEqual(len(blocks), 4)


class TestGameBoard(unittest.TestCase):
    """测试游戏板类"""
    
    def setUp(self):
        """测试前准备"""
        self.board = GameBoard()
        self.piece = Piece(0)
    
    def test_board_initialization(self):
        """测试游戏板初始化"""
        self.assertEqual(self.board.width, GameConfig.BOARD_COLS)
        self.assertEqual(self.board.height, GameConfig.BOARD_ROWS)
        self.assertEqual(len(self.board.grid), GameConfig.BOARD_ROWS)
        self.assertEqual(len(self.board.grid[0]), GameConfig.BOARD_COLS)
    
    def test_board_is_empty(self):
        """测试游戏板初始为空"""
        for row in self.board.grid:
            for cell in row:
                self.assertIsNone(cell)
    
    def test_is_valid_position_center(self):
        """测试有效位置检测 - 中心位置"""
        self.assertTrue(self.board.is_valid_position(self.piece))
    
    def test_is_valid_position_left_boundary(self):
        """测试有效位置检测 - 左边界"""
        self.piece.x = -1
        self.assertFalse(self.board.is_valid_position(self.piece))
    
    def test_is_valid_position_right_boundary(self):
        """测试有效位置检测 - 右边界"""
        self.piece.x = GameConfig.BOARD_COLS
        self.assertFalse(self.board.is_valid_position(self.piece))
    
    def test_is_valid_position_bottom_boundary(self):
        """测试有效位置检测 - 底部边界"""
        self.piece.y = GameConfig.BOARD_ROWS
        self.assertFalse(self.board.is_valid_position(self.piece))
    
    def test_lock_piece(self):
        """测试锁定方块"""
        self.board.lock_piece(self.piece)
        locked = False
        for y, row in enumerate(self.board.grid):
            for x, cell in enumerate(row):
                if cell is not None:
                    locked = True
                    self.assertEqual(cell, self.piece.color)
        self.assertTrue(locked)
    
    def test_clear_empty_lines(self):
        """测试清除空行"""
        lines = self.board.clear_lines()
        self.assertEqual(lines, 0)
    
    def test_clear_full_line(self):
        """测试清除满行"""
        for x in range(GameConfig.BOARD_COLS):
            self.board.grid[GameConfig.BOARD_ROWS - 1][x] = (255, 0, 0)
        
        lines = self.board.clear_lines()
        self.assertEqual(lines, 1)
    
    def test_clear_multiple_lines(self):
        """测试清除多行"""
        for y in range(GameConfig.BOARD_ROWS - 2, GameConfig.BOARD_ROWS):
            for x in range(GameConfig.BOARD_COLS):
                self.board.grid[y][x] = (0, 255, 0)
        
        lines = self.board.clear_lines()
        self.assertEqual(lines, 2)
    
    def test_is_game_over_empty_board(self):
        """测试游戏结束检测 - 空板"""
        self.assertFalse(self.board.is_game_over())
    
    def test_is_game_over_top_row_filled(self):
        """测试游戏结束检测 - 顶层有方块"""
        self.board.grid[0][0] = (255, 0, 0)
        self.assertTrue(self.board.is_game_over())
    
    def test_reset_board(self):
        """测试重置游戏板"""
        self.board.grid[0][0] = (255, 0, 0)
        self.board.reset()
        
        for row in self.board.grid:
            for cell in row:
                self.assertIsNone(cell)


class TestGameConfig(unittest.TestCase):
    """测试游戏配置"""
    
    def test_piece_shapes_count(self):
        """测试方块形状数量"""
        self.assertEqual(len(GameConfig.PIECE_SHAPES), 7)
    
    def test_piece_shapes_rotation_count(self):
        """测试每个方块的旋转状态数"""
        for shape in GameConfig.PIECE_SHAPES:
            self.assertEqual(len(shape), 4)
    
    def test_piece_colors_count(self):
        """测试方块颜色数量"""
        self.assertEqual(len(GameConfig.PIECE_COLORS), 7)
    
    def test_speed_levels_count(self):
        """测试速度等级数量"""
        self.assertEqual(len(GameConfig.SPEED_LEVELS), 10)
    
    def test_score_values_keys(self):
        """测试分数值的键"""
        expected_keys = [1, 2, 3, 4]
        for key in expected_keys:
            self.assertIn(key, GameConfig.SCORE_VALUES)
    
    def test_score_values_positive(self):
        """测试分数值为正数"""
        for score in GameConfig.SCORE_VALUES.values():
            self.assertGreater(score, 0)
    
    def test_speed_levels_decreasing(self):
        """测试速度等级递减 (速度值应该递减)"""
        for i in range(len(GameConfig.SPEED_LEVELS) - 1):
            self.assertLess(GameConfig.SPEED_LEVELS[i + 1], 
                          GameConfig.SPEED_LEVELS[i])


class TestPieceTypes(unittest.TestCase):
    """测试每种方块类型的特性"""
    
    def test_I_piece(self):
        """测试I型方块"""
        piece = Piece(0)
        self.assertEqual(piece.color, (255, 0, 0))
        blocks = piece.get_blocks()
        self.assertEqual(len(blocks), 4)
    
    def test_O_piece(self):
        """测试O型方块"""
        piece = Piece(1)
        self.assertEqual(piece.color, (0, 255, 255))
        blocks = piece.get_blocks()
        self.assertEqual(len(blocks), 4)
    
    def test_T_piece(self):
        """测试T型方块"""
        piece = Piece(2)
        self.assertEqual(piece.color, (255, 255, 0))
        blocks = piece.get_blocks()
        self.assertEqual(len(blocks), 4)
    
    def test_S_piece(self):
        """测试S型方块"""
        piece = Piece(3)
        self.assertEqual(piece.color, (128, 0, 128))
        blocks = piece.get_blocks()
        self.assertEqual(len(blocks), 4)
    
    def test_Z_piece(self):
        """测试Z型方块"""
        piece = Piece(4)
        self.assertEqual(piece.color, (0, 255, 0))
        blocks = piece.get_blocks()
        self.assertEqual(len(blocks), 4)
    
    def test_J_piece(self):
        """测试J型方块"""
        piece = Piece(5)
        self.assertEqual(piece.color, (0, 0, 255))
        blocks = piece.get_blocks()
        self.assertEqual(len(blocks), 4)
    
    def test_L_piece(self):
        """测试L型方块"""
        piece = Piece(6)
        self.assertEqual(piece.color, (255, 165, 0))
        blocks = piece.get_blocks()
        self.assertEqual(len(blocks), 4)


class TestCollisionDetection(unittest.TestCase):
    """测试碰撞检测"""
    
    def setUp(self):
        """测试前准备"""
        self.board = GameBoard()
    
    def test_no_collision_empty_board(self):
        """测试空板无碰撞"""
        piece = Piece(0)
        self.assertTrue(self.board.is_valid_position(piece))
    
    def test_collision_with_block(self):
        """测试与方块碰撞"""
        piece = Piece(0)
        self.board.lock_piece(piece)
        
        piece2 = Piece(1)
        piece2.x = piece.x
        piece2.y = piece.y
        
        self.assertFalse(self.board.is_valid_position(piece2))
    
    def test_wall_collision_left(self):
        """测试墙壁碰撞 - 左侧"""
        piece = Piece(0)
        piece.x = -2
        self.assertFalse(self.board.is_valid_position(piece))
    
    def test_wall_collision_right(self):
        """测试墙壁碰撞 - 右侧"""
        piece = Piece(0)
        piece.x = GameConfig.BOARD_COLS - 1
        self.assertFalse(self.board.is_valid_position(piece))
    
    def test_floor_collision(self):
        """测试底部碰撞"""
        piece = Piece(0)
        piece.y = GameConfig.BOARD_ROWS - 4
        self.assertTrue(self.board.is_valid_position(piece))
        
        piece.y = GameConfig.BOARD_ROWS
        self.assertFalse(self.board.is_valid_position(piece))


class TestScoring(unittest.TestCase):
    """测试计分系统"""
    
    def test_single_line_score(self):
        """测试单行消除分数"""
        self.assertEqual(GameConfig.SCORE_VALUES[1], 100)
    
    def test_double_line_score(self):
        """测试双行消除分数"""
        self.assertEqual(GameConfig.SCORE_VALUES[2], 300)
    
    def test_triple_line_score(self):
        """测试三行消除分数"""
        self.assertEqual(GameConfig.SCORE_VALUES[3], 500)
    
    def test_tetris_score(self):
        """测试四行消除分数 (满堂红)"""
        self.assertEqual(GameConfig.SCORE_VALUES[4], 800)
    
    def test_score_increases_with_lines(self):
        """测试消除行数越多分数越高"""
        for i in range(1, 4):
            self.assertGreater(GameConfig.SCORE_VALUES[i + 1], 
                             GameConfig.SCORE_VALUES[i])


class TestGameStates(unittest.TestCase):
    """测试游戏状态"""
    
    def test_game_states_enum(self):
        """测试游戏状态枚举"""
        self.assertEqual(GameState.READY.value, 0)
        self.assertEqual(GameState.PLAYING.value, 1)
        self.assertEqual(GameState.PAUSED.value, 2)
        self.assertEqual(GameState.GAME_OVER.value, 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
