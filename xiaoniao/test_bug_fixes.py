import unittest
import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bird import Bird
from slingshot import Slingshot
from game_state import GameState

class TestBugFixes(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
    
    def tearDown(self):
        pygame.quit()
    
    def test_bird_launch_after_drag(self):
        """测试小鸟拖拽后可以正常发射（修复bug2）"""
        bird = Bird()
        slingshot = Slingshot()
        game_state = GameState()
        
        self.assertFalse(bird.is_flying)
        self.assertEqual(bird.x, slingshot.x)
        self.assertEqual(bird.y, slingshot.y - 30)
        
        slingshot.is_dragging = True
        slingshot.drag_end = (100, 550)
        
        bird.x, bird.y = slingshot.get_bird_position()
        self.assertEqual(bird.x, 100)
        self.assertEqual(bird.y, 550)
        
        slingshot.is_dragging = False
        slingshot.launch_bird(bird, game_state)
        
        self.assertTrue(bird.is_flying)
        self.assertTrue(bird.vx != 0 or bird.vy != 0)
        self.assertEqual(game_state.birds_left, 2)
    
    def test_bird_not_reset_while_dragging(self):
        """测试拖拽时小鸟不会被重置（修复bug2）"""
        bird = Bird()
        slingshot = Slingshot()
        game_state = GameState()
        
        slingshot.is_dragging = True
        slingshot.drag_end = (100, 550)
        
        bird.x, bird.y = slingshot.get_bird_position()
        original_x, original_y = bird.x, bird.y
        
        if not bird.is_flying and not slingshot.is_dragging and not game_state.is_game_over() and game_state.birds_left > 0:
            bird.reset()
        
        self.assertEqual(bird.x, original_x)
        self.assertEqual(bird.y, original_y)
    
    def test_drawing_order(self):
        """测试绘制顺序确保说明文字不会遮挡游戏元素（修复bug1）"""
        from settings import SCREEN_WIDTH, SCREEN_HEIGHT, LIGHT_GREEN, RED, WHITE
        
        self.screen.fill(LIGHT_GREEN)
        
        instructions = [
            "游戏说明:",
            "1. 点击并拖拽小鸟发射",
            "2. 击打猪头获得 100 分",
            "3. 击打方块获得 20 分",
            "4. 消灭所有猪头获胜",
            "5. 用完小鸟则失败",
            "6. 按 R 键重新开始"
        ]
        
        font_path = "C:/Windows/Fonts/simhei.ttf"
        if os.path.exists(font_path):
            small_font = pygame.font.Font(font_path, 24)
        else:
            small_font = pygame.font.Font(None, 24)
        
        for i, text in enumerate(instructions):
            text_surface = small_font.render(text, True, (50, 50, 50))
            self.screen.blit(text_surface, (SCREEN_WIDTH - 180, 80 + i * 22))
        
        slingshot = Slingshot()
        slingshot.draw(self.screen)
        
        bird = Bird()
        bird.x, bird.y = slingshot.get_bird_position()
        bird.draw(self.screen)
        
        pixel_at_bird = self.screen.get_at((int(bird.x), int(bird.y)))
        self.assertEqual(pixel_at_bird[:3], RED[:3])
        
        pixel_at_instruction = self.screen.get_at((SCREEN_WIDTH - 170, 90))
        self.assertEqual(pixel_at_instruction[:3], (50, 50, 50))

if __name__ == '__main__':
    unittest.main()