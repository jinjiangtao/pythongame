import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.enemy import Enemy, EnemyManager

class TestEnemy(unittest.TestCase):
    def setUp(self):
        self.normal_enemy = Enemy(240, 100, 'normal')
        self.fast_enemy = Enemy(240, 100, 'fast')
        self.heavy_enemy = Enemy(240, 100, 'heavy')
        self.boss = Enemy(240, 100, 'boss')
        
    def test_initialization(self):
        self.assertEqual(self.normal_enemy.x, 240)
        self.assertEqual(self.normal_enemy.y, 100)
        self.assertEqual(self.normal_enemy.type, 'normal')
        self.assertTrue(self.normal_enemy.is_active())
        
    def test_movement(self):
        initial_y = self.normal_enemy.y
        self.normal_enemy.update(0)
        self.assertEqual(self.normal_enemy.y, initial_y + self.normal_enemy.speed)
        
    def test_take_damage(self):
        self.assertEqual(self.normal_enemy.health, 20)
        
        result = self.normal_enemy.take_damage(10)
        self.assertFalse(result)
        self.assertEqual(self.normal_enemy.health, 10)
        
        result = self.normal_enemy.take_damage(10)
        self.assertTrue(result)
        self.assertFalse(self.normal_enemy.is_active())
        
    def test_boss_identification(self):
        self.assertFalse(self.normal_enemy.is_boss())
        self.assertTrue(self.boss.is_boss())
        
    def test_score(self):
        self.assertEqual(self.normal_enemy.get_score(), 100)
        self.assertEqual(self.fast_enemy.get_score(), 150)
        self.assertEqual(self.heavy_enemy.get_score(), 300)
        self.assertEqual(self.boss.get_score(), 2000)

class TestEnemyManager(unittest.TestCase):
    def setUp(self):
        self.manager = EnemyManager()
        
    def test_add_enemy(self):
        self.assertEqual(self.manager.get_active_count(), 0)
        
        self.manager.add_enemy(240, 100, 'normal')
        self.assertEqual(self.manager.get_active_count(), 1)
        
    def test_add_boss(self):
        self.manager.add_boss()
        self.assertEqual(self.manager.get_active_count(), 1)
        self.assertTrue(self.manager.has_boss())
        
    def test_clear_all(self):
        self.manager.add_enemy(240, 100, 'normal')
        self.manager.add_enemy(300, 150, 'fast')
        
        self.assertEqual(self.manager.get_active_count(), 2)
        self.manager.clear_all()
        self.assertEqual(self.manager.get_active_count(), 0)
        
    def test_update_removes_inactive(self):
        enemy = Enemy(240, 100, 'normal')
        enemy.health = 0
        enemy.active = False
        
        self.manager.add_enemy(240, 100, 'normal')
        self.manager.enemies[0].active = False
        
        self.manager.update(0)
        self.assertEqual(self.manager.get_active_count(), 0)

if __name__ == '__main__':
    unittest.main()