import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(240, 620)
        
    def test_initial_position(self):
        x, y = self.player.get_position()
        self.assertEqual(x, 240)
        self.assertEqual(y, 620)
        
    def test_movement(self):
        initial_x, initial_y = self.player.get_position()
        
        self.player.keys['up'] = True
        self.player.move()
        _, new_y = self.player.get_position()
        self.assertEqual(new_y, initial_y - self.player.speed)
        
        self.player.keys['up'] = False
        self.player.keys['down'] = True
        self.player.move()
        _, new_y = self.player.get_position()
        self.assertEqual(new_y, initial_y)
        
        self.player.keys['down'] = False
        self.player.keys['left'] = True
        self.player.move()
        new_x, _ = self.player.get_position()
        self.assertEqual(new_x, initial_x - self.player.speed)
        
        self.player.keys['left'] = False
        self.player.keys['right'] = True
        self.player.move()
        new_x, _ = self.player.get_position()
        self.assertEqual(new_x, initial_x)
        
    def test_boundary_constraints(self):
        self.player.x = 10
        self.player.keys['left'] = True
        self.player.move()
        self.assertTrue(self.player.x >= self.player.size // 2)
        
        self.player.x = 470
        self.player.keys['right'] = True
        self.player.move()
        self.assertTrue(self.player.x <= 480 - self.player.size // 2)
        
    def test_health_management(self):
        self.assertEqual(self.player.get_health(), 100)
        
        self.player.take_damage(30)
        self.assertEqual(self.player.get_health(), 70)
        
        self.player.heal(20)
        self.assertEqual(self.player.get_health(), 90)
        
        self.player.heal(20)
        self.assertEqual(self.player.get_health(), 100)
        
    def test_power_level(self):
        self.assertEqual(self.player.get_power_level(), 1)
        
        self.player.power_up()
        self.assertEqual(self.player.get_power_level(), 2)
        
        self.player.power_up()
        self.assertEqual(self.player.get_power_level(), 3)
        
        self.player.power_up()
        self.assertEqual(self.player.get_power_level(), 3)
        
    def test_bomb_management(self):
        self.assertEqual(self.player.get_bomb_count(), 1)
        
        self.player.add_bomb()
        self.assertEqual(self.player.get_bomb_count(), 2)
        
        result = self.player.use_bomb()
        self.assertTrue(result)
        self.assertEqual(self.player.get_bomb_count(), 1)
        
        self.player.use_bomb()
        self.assertEqual(self.player.get_bomb_count(), 0)
        
        result = self.player.use_bomb()
        self.assertFalse(result)
        
    def test_invincible_state(self):
        self.assertFalse(self.player.is_invincible())
        
        self.player.take_damage(10)
        self.assertTrue(self.player.is_invincible())
        
    def test_shield(self):
        self.assertFalse(self.player.is_shield_active())
        
        self.player.activate_shield(5000)
        self.assertTrue(self.player.is_shield_active())
        
    def test_death(self):
        self.assertTrue(self.player.is_active())
        
        self.player.take_damage(50)
        self.assertTrue(self.player.is_active())
        
        self.player.invincible = False
        self.player.take_damage(60)
        self.assertFalse(self.player.is_active())

if __name__ == '__main__':
    unittest.main()