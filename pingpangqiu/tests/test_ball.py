import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ball import Ball
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BALL_SIZE,
    BALL_SPEED_X, BALL_SPEED_Y
)


class MockPaddle:
    def __init__(self, x, y, width=15, height=100):
        import pygame
        self.rect = pygame.Rect(x, y, width, height)

    def get_center_y(self):
        return self.rect.y + self.rect.height // 2


class TestBall(unittest.TestCase):
    def test_ball_initialization(self):
        ball = Ball()
        expected_x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        expected_y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        self.assertEqual(ball.rect.x, expected_x)
        self.assertEqual(ball.rect.y, expected_y)
        self.assertEqual(ball.rect.width, BALL_SIZE)
        self.assertEqual(ball.rect.height, BALL_SIZE)

    def test_ball_move(self):
        ball = Ball()
        initial_x = ball.rect.x
        initial_y = ball.rect.y
        ball.move()
        self.assertEqual(ball.rect.x, initial_x + ball.speed_x)
        self.assertEqual(ball.rect.y, initial_y + ball.speed_y)

    def test_bounce_y(self):
        ball = Ball()
        initial_speed = ball.speed_y
        ball.bounce_y()
        self.assertEqual(ball.speed_y, -initial_speed)

    def test_bounce_x(self):
        ball = Ball()
        initial_speed = ball.speed_x
        ball.bounce_x()
        self.assertEqual(ball.speed_x, -initial_speed)

    def test_get_center_y(self):
        ball = Ball()
        ball.rect.y = 100
        expected_center = 100 + BALL_SIZE // 2
        self.assertEqual(ball.get_center_y(), expected_center)

    def test_is_out_of_bounds_left(self):
        ball = Ball()
        ball.rect.left = -10
        self.assertTrue(ball.is_out_of_bounds_left())
        ball.rect.left = 10
        self.assertFalse(ball.is_out_of_bounds_left())

    def test_is_out_of_bounds_right(self):
        ball = Ball()
        ball.rect.right = SCREEN_WIDTH + 10
        self.assertTrue(ball.is_out_of_bounds_right())
        ball.rect.right = SCREEN_WIDTH - 10
        self.assertFalse(ball.is_out_of_bounds_right())

    def test_check_wall_collision_top(self):
        ball = Ball()
        ball.rect.top = -5
        ball.speed_y = -BALL_SPEED_Y
        ball.check_wall_collision()
        self.assertEqual(ball.rect.top, 0)
        self.assertEqual(ball.speed_y, BALL_SPEED_Y)

    def test_check_wall_collision_bottom(self):
        ball = Ball()
        ball.rect.bottom = SCREEN_HEIGHT + 5
        ball.speed_y = BALL_SPEED_Y
        ball.check_wall_collision()
        self.assertEqual(ball.rect.bottom, SCREEN_HEIGHT)
        self.assertEqual(ball.speed_y, -BALL_SPEED_Y)

    def test_check_paddle_collision(self):
        ball = Ball()
        paddle = MockPaddle(400, 300)
        ball.rect.x = 390
        ball.rect.y = 320
        ball.speed_x = -BALL_SPEED_X
        
        initial_speed_x = ball.speed_x
        ball.check_paddle_collision(paddle)
        self.assertEqual(ball.speed_x, -initial_speed_x)


if __name__ == '__main__':
    unittest.main()