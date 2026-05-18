import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.bullet import Bullet, BulletManager

class TestBullet(unittest.TestCase):
    def setUp(self):
        self.bullet = Bullet(240, 360, (0, -1), 'player_single')
        
    def test_initialization(self):
        self.assertEqual(self.bullet.x, 240)
        self.assertEqual(self.bullet.y, 360)
        self.assertEqual(self.bullet.direction, (0, -1))
        self.assertTrue(self.bullet.is_active())
        
    def test_update(self):
        initial_y = self.bullet.y
        self.bullet.update()
        self.assertEqual(self.bullet.y, initial_y - self.bullet.speed)
        
    def test_deactivate(self):
        self.assertTrue(self.bullet.is_active())
        self.bullet.deactivate()
        self.assertFalse(self.bullet.is_active())
        
    def test_out_of_bounds(self):
        self.bullet.y = 800
        self.bullet.update()
        self.assertFalse(self.bullet.is_active())
        
    def test_damage(self):
        self.assertEqual(self.bullet.get_damage(), 10)

class TestBulletManager(unittest.TestCase):
    def setUp(self):
        self.manager = BulletManager()
        
    def test_add_bullet(self):
        self.assertEqual(self.manager.get_active_count(), 0)
        
        self.manager.add_bullet(240, 360, (0, -1), 'player_single')
        self.assertEqual(self.manager.get_active_count(), 1)
        
    def test_add_player_bullets(self):
        self.manager.add_player_bullets(240, 360, 1)
        self.assertEqual(self.manager.get_active_count(), 1)
        
        self.manager.add_player_bullets(240, 360, 2)
        self.assertEqual(self.manager.get_active_count(), 3)
        
        self.manager.add_player_bullets(240, 360, 3)
        self.assertEqual(self.manager.get_active_count(), 6)
        
    def test_add_enemy_bullet(self):
        self.manager.add_enemy_bullet(240, 100, 'normal')
        self.assertEqual(self.manager.get_active_count(), 1)
        
    def test_update_removes_inactive(self):
        self.manager.add_bullet(240, 800, (0, 1), 'player_single')
        
        self.manager.update()
        self.assertEqual(self.manager.get_active_count(), 0)
        
    def test_clear_all(self):
        self.manager.add_bullet(240, 360, (0, -1), 'player_single')
        self.manager.add_bullet(250, 350, (0, -1), 'player_single')
        
        self.assertEqual(self.manager.get_active_count(), 2)
        self.manager.clear_all()
        self.assertEqual(self.manager.get_active_count(), 0)

if __name__ == '__main__':
    unittest.main()