import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.props import Prop, PropManager

class TestProp(unittest.TestCase):
    def setUp(self):
        self.prop = Prop(240, 360, 'power_up')
        
    def test_initialization(self):
        self.assertEqual(self.prop.x, 240)
        self.assertEqual(self.prop.y, 360)
        self.assertEqual(self.prop.type, 'power_up')
        self.assertTrue(self.prop.is_active())
        
    def test_update(self):
        initial_y = self.prop.y
        self.prop.update()
        self.assertEqual(self.prop.y, initial_y + self.prop.speed)
        
    def test_out_of_bounds(self):
        self.prop.y = 800
        self.prop.update()
        self.assertFalse(self.prop.is_active())
        
    def test_get_config(self):
        config = self.prop.get_config()
        self.assertIn('color', config)
        
    def test_types(self):
        power_prop = Prop(240, 360, 'power_up')
        shield_prop = Prop(240, 360, 'shield')
        health_prop = Prop(240, 360, 'health')
        bomb_prop = Prop(240, 360, 'bomb')
        
        self.assertEqual(power_prop.type, 'power_up')
        self.assertEqual(shield_prop.type, 'shield')
        self.assertEqual(health_prop.type, 'health')
        self.assertEqual(bomb_prop.type, 'bomb')

class TestPropManager(unittest.TestCase):
    def setUp(self):
        self.manager = PropManager()
        
    def test_add_prop(self):
        self.assertEqual(len(self.manager.get_props()), 0)
        
        self.manager.add_prop(240, 360, 'power_up')
        self.assertEqual(len(self.manager.get_props()), 1)
        
    def test_try_spawn(self):
        self.manager.set_drop_chance(1.0)
        self.manager.try_spawn(240, 360)
        self.assertEqual(len(self.manager.get_props()), 1)
        
    def test_update_removes_inactive(self):
        self.manager.add_prop(240, 800, 'power_up')
        
        self.manager.update()
        self.assertEqual(len(self.manager.get_props()), 0)
        
    def test_clear_all(self):
        self.manager.add_prop(240, 360, 'power_up')
        self.manager.add_prop(300, 400, 'shield')
        
        self.assertEqual(len(self.manager.get_props()), 2)
        self.manager.clear_all()
        self.assertEqual(len(self.manager.get_props()), 0)
        
    def test_drop_chance(self):
        self.assertEqual(self.manager.drop_chance, 0.15)
        
        self.manager.set_drop_chance(0.5)
        self.assertEqual(self.manager.drop_chance, 0.5)
        
        self.manager.set_drop_chance(1.5)
        self.assertEqual(self.manager.drop_chance, 1.0)
        
        self.manager.set_drop_chance(-0.5)
        self.assertEqual(self.manager.drop_chance, 0.0)

if __name__ == '__main__':
    unittest.main()