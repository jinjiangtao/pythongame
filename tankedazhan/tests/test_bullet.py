import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bullet import Bullet
from src.config import *

class TestBullet(unittest.TestCase):
    def test_bullet_creation(self):
        bullet = Bullet(100, 200, DIR_UP, True)
        self.assertEqual(bullet.x, 100)
        self.assertEqual(bullet.y, 200)
        self.assertEqual(bullet.direction, DIR_UP)
        self.assertTrue(bullet.is_player)
        self.assertTrue(bullet.active)
    
    def test_bullet_update_up(self):
        bullet = Bullet(100, 200, DIR_UP, True)
        initial_y = bullet.y
        bullet.update()
        self.assertEqual(bullet.y, initial_y - BULLET_SPEED)
    
    def test_bullet_update_down(self):
        bullet = Bullet(100, 200, DIR_DOWN, True)
        initial_y = bullet.y
        bullet.update()
        self.assertEqual(bullet.y, initial_y + BULLET_SPEED)
    
    def test_bullet_update_left(self):
        bullet = Bullet(100, 200, DIR_LEFT, True)
        initial_x = bullet.x
        bullet.update()
        self.assertEqual(bullet.x, initial_x - BULLET_SPEED)
    
    def test_bullet_update_right(self):
        bullet = Bullet(100, 200, DIR_RIGHT, True)
        initial_x = bullet.x
        bullet.update()
        self.assertEqual(bullet.x, initial_x + BULLET_SPEED)
    
    def test_bullet_out_of_bounds(self):
        bullet = Bullet(-10, 100, DIR_LEFT, True)
        bullet.update()
        self.assertFalse(bullet.active)
        
        bullet2 = Bullet(SCREEN_WIDTH + 10, 100, DIR_RIGHT, True)
        bullet2.update()
        self.assertFalse(bullet2.active)
        
        bullet3 = Bullet(100, -10, DIR_UP, True)
        bullet3.update()
        self.assertFalse(bullet3.active)
        
        bullet4 = Bullet(100, SCREEN_HEIGHT + 10, DIR_DOWN, True)
        bullet4.update()
        self.assertFalse(bullet4.active)

if __name__ == '__main__':
    unittest.main()