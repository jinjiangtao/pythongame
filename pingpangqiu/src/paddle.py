import pygame
from src.config import (
    PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED, AI_PADDLE_SPEED,
    SCREEN_HEIGHT, PLAYER_COLOR, AI_COLOR, PLAYER_PADDLE_X, AI_PADDLE_X
)


class Paddle:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = color
        self.speed = PADDLE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def set_speed(self, speed):
        self.speed = speed

    def get_center_y(self):
        return self.rect.y + PADDLE_HEIGHT // 2


class PlayerPaddle(Paddle):
    def __init__(self):
        y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        super().__init__(PLAYER_PADDLE_X, y, PLAYER_COLOR)


class AIPaddle(Paddle):
    def __init__(self):
        y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        super().__init__(AI_PADDLE_X, y, AI_COLOR)
        self.speed = AI_PADDLE_SPEED

    def update(self, ball):
        paddle_center = self.get_center_y()
        ball_center = ball.get_center_y()

        if paddle_center < ball_center:
            self.move_down()
        elif paddle_center > ball_center:
            self.move_up()