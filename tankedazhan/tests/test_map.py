import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.map import GameMap
from src.config import *

class TestGameMap(unittest.TestCase):
    def test_map_creation(self):
        game_map = GameMap(1)
        self.assertEqual(game_map.level, 1)
        self.assertFalse(game_map.base_destroyed)
        self.assertIsNotNone(game_map.base_position)
    
    def test_map_tile_types(self):
        game_map = GameMap(1)
        has_brick = False
        has_steel = False
        has_grass = False
        has_base = False
        
        for row in game_map.tiles:
            for tile in row:
                if tile == BRICK:
                    has_brick = True
                elif tile == STEEL:
                    has_steel = True
                elif tile == GRASS:
                    has_grass = True
                elif tile == BASE:
                    has_base = True
        
        self.assertTrue(has_brick)
        self.assertTrue(has_steel)
        self.assertTrue(has_grass)
        self.assertTrue(has_base)
    
    def test_check_collision(self):
        game_map = GameMap(1)
        
        class MockRect:
            def __init__(self, left, top, width, height):
                self.left = left
                self.top = top
                self.right = left + width
                self.bottom = top + height
        
        rect = MockRect(GRID_SIZE * 2, GRID_SIZE * 2, GRID_SIZE - 1, GRID_SIZE - 1)
        result = game_map.check_collision(rect)
        self.assertIsInstance(result, bool)
    
    def test_check_bullet_collision_brick(self):
        game_map = GameMap(1)
        
        class MockBullet:
            def __init__(self, x, y):
                self.x = x
                self.y = y
            
            def get_rect(self):
                return type('obj', (object,), {'centerx': self.x, 'centery': self.y})
        
        for row in range(game_map.map_height):
            for col in range(game_map.map_width):
                if game_map.tiles[row][col] == BRICK:
                    bullet = MockBullet(col * GRID_SIZE + GRID_SIZE // 2, 
                                       row * GRID_SIZE + GRID_SIZE // 2)
                    result, pos = game_map.check_bullet_collision(bullet)
                    self.assertEqual(result, "destroy")
                    self.assertEqual(pos, (col, row))
                    self.assertEqual(game_map.tiles[row][col], EMPTY)
                    break
            else:
                continue
            break
    
    def test_check_bullet_collision_steel(self):
        game_map = GameMap(1)
        
        class MockBullet:
            def __init__(self, x, y):
                self.x = x
                self.y = y
            
            def get_rect(self):
                return type('obj', (object,), {'centerx': self.x, 'centery': self.y})
        
        for row in range(game_map.map_height):
            for col in range(game_map.map_width):
                if game_map.tiles[row][col] == STEEL:
                    bullet = MockBullet(col * GRID_SIZE + GRID_SIZE // 2, 
                                       row * GRID_SIZE + GRID_SIZE // 2)
                    result, pos = game_map.check_bullet_collision(bullet)
                    self.assertEqual(result, "block")
                    self.assertIsNone(pos)
                    self.assertEqual(game_map.tiles[row][col], STEEL)
                    break
            else:
                continue
            break
    
    def test_is_grass(self):
        game_map = GameMap(1)
        
        for row in range(game_map.map_height):
            for col in range(game_map.map_width):
                if game_map.tiles[row][col] == GRASS:
                    x = col * GRID_SIZE + GRID_SIZE // 2
                    y = row * GRID_SIZE + GRID_SIZE // 2
                    self.assertTrue(game_map.is_grass(x, y))
                    break
            else:
                continue
            break
        
        self.assertFalse(game_map.is_grass(-1, -1))

if __name__ == '__main__':
    unittest.main()