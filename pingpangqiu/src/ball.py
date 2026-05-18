import pygame
import random
from src.config import (
    BALL_SIZE, BALL_SPEED_X, BALL_SPEED_Y,
    SCREEN_WIDTH, SCREEN_HEIGHT, BALL_COLOR
)


class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(
            SCREEN_WIDTH // 2 - BALL_SIZE // 2,
            SCREEN_HEIGHT // 2 - BALL_SIZE // 2,
            BALL_SIZE,
            BALL_SIZE
        )
        self.speed_x = BALL_SPEED_X * random.choice([1, -1])
        self.speed_y = BALL_SPEED_Y * random.choice([1, -1])

    def draw(self, screen):
        pygame.draw.ellipse(screen, BALL_COLOR, self.rect)

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def bounce_y(self):
        self.speed_y *= -1

    def bounce_x(self):
        self.speed_x *= -1

    def check_wall_collision(self):
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.bounce_y()
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT

    def check_paddle_collision(self, paddle):
        if self.rect.colliderect(paddle.rect):
            self.bounce_x()
            overlap_y = self.get_center_y() - paddle.get_center_y()
            normalized_overlap = overlap_y / (paddle.rect.height / 2)
            self.speed_y = BALL_SPEED_Y * normalized_overlap

    def get_center_y(self):
        return self.rect.y + BALL_SIZE // 2

    def is_out_of_bounds_left(self):
        return self.rect.left <= 0

    def is_out_of_bounds_right(self):
        return self.rect.right >= SCREEN_WIDTH