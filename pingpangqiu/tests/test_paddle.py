import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.paddle import Paddle, PlayerPaddle, AIPaddle
from src.config import (
    SCREEN_HEIGHT, PADDLE_HEIGHT, PADDLE_WIDTH,
    PLAYER_PADDLE_X, AI_PADDLE_X, PLAYER_COLOR, AI_COLOR
)


class MockBall:
    def __init__(self, center_y):
        self._center_y = center_y

    def get_center_y(self):
        return self._center_y


class TestPaddle(unittest.TestCase):
    def test_paddle_initialization(self):
        paddle = Paddle(100, 200, (255, 0, 0))
        self.assertEqual(paddle.rect.x, 100)
        self.assertEqual(paddle.rect.y, 200)
        self.assertEqual(paddle.rect.width, PADDLE_WIDTH)
        self.assertEqual(paddle.rect.height, PADDLE_HEIGHT)
        self.assertEqual(paddle.color, (255, 0, 0))

    def test_move_up_within_bounds(self):
        paddle = Paddle(100, 100, (255, 0, 0))
        initial_y = paddle.rect.y
        paddle.move_up()
        self.assertEqual(paddle.rect.y, initial_y - paddle.speed)

    def test_move_up_at_top_boundary(self):
        paddle = Paddle(100, 0, (255, 0, 0))
        initial_y = paddle.rect.y
        paddle.move_up()
        self.assertEqual(paddle.rect.y, initial_y)

    def test_move_down_within_bounds(self):
        paddle = Paddle(100, 100, (255, 0, 0))
        initial_y = paddle.rect.y
        paddle.move_down()
        self.assertEqual(paddle.rect.y, initial_y + paddle.speed)

    def test_move_down_at_bottom_boundary(self):
        paddle = Paddle(100, SCREEN_HEIGHT - PADDLE_HEIGHT, (255, 0, 0))
        initial_y = paddle.rect.y
        paddle.move_down()
        self.assertEqual(paddle.rect.y, initial_y)

    def test_get_center_y(self):
        paddle = Paddle(100, 100, (255, 0, 0))
        expected_center = 100 + PADDLE_HEIGHT // 2
        self.assertEqual(paddle.get_center_y(), expected_center)

    def test_set_speed(self):
        paddle = Paddle(100, 100, (255, 0, 0))
        paddle.set_speed(10)
        self.assertEqual(paddle.speed, 10)


class TestPlayerPaddle(unittest.TestCase):
    def test_player_paddle_initialization(self):
        player = PlayerPaddle()
        self.assertEqual(player.rect.x, PLAYER_PADDLE_X)
        self.assertEqual(player.rect.y, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.assertEqual(player.color, PLAYER_COLOR)


class TestAIPaddle(unittest.TestCase):
    def test_ai_paddle_initialization(self):
        ai = AIPaddle()
        self.assertEqual(ai.rect.x, AI_PADDLE_X)
        self.assertEqual(ai.rect.y, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.assertEqual(ai.color, AI_COLOR)

    def test_ai_move_toward_ball(self):
        ai = AIPaddle()
        initial_y = ai.rect.y
        
        ball_above = MockBall(ai.get_center_y() - 50)
        ai.update(ball_above)
        self.assertEqual(ai.rect.y, initial_y - ai.speed)
        
        ball_below = MockBall(ai.get_center_y() + 50)
        ai.update(ball_below)
        self.assertEqual(ai.rect.y, initial_y)


if __name__ == '__main__':
    unittest.main()