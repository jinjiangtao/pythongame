import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tank import Tank
from src.config import *

class TestTank(unittest.TestCase):
    def test_tank_creation(self):
        tank = Tank(100, 200, DIR_UP, True)
        self.assertEqual(tank.x, 100)
        self.assertEqual(tank.y, 200)
        self.assertEqual(tank.direction, DIR_UP)
        self.assertTrue(tank.is_player)
        self.assertEqual(tank.health, PLAYER_HEALTH)
    
    def test_tank_clamp_position(self):
        tank = Tank(-10, -10, DIR_UP, True)
        tank.clamp_position()
        self.assertEqual(tank.x, 0)
        self.assertEqual(tank.y, 0)
        
        tank2 = Tank(SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10, DIR_UP, True)
        tank2.clamp_position()
        self.assertEqual(tank2.x, SCREEN_WIDTH - tank2.width)
        self.assertEqual(tank2.y, SCREEN_HEIGHT - tank2.height)
    
    def test_tank_take_damage(self):
        tank = Tank(100, 200, DIR_UP, True)
        initial_health = tank.health
        
        result = tank.take_damage()
        self.assertEqual(tank.health, initial_health - 1)
        self.assertFalse(result)
        
        tank.take_damage(initial_health - 1)
        result = tank.take_damage()
        self.assertTrue(result)
    
    def test_tank_shoot_cooldown(self):
        tank = Tank(100, 200, DIR_UP, True)
        
        bullet = tank.shoot(0)
        self.assertIsNotNone(bullet)
        
        bullet2 = tank.shoot(100)
        self.assertIsNone(bullet2)
        
        bullet3 = tank.shoot(600)
        self.assertIsNotNone(bullet3)

if __name__ == '__main__':
    unittest.main()