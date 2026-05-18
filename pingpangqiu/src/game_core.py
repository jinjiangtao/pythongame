import pygame
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR,
    WIN_SCORE, WHITE, BLACK
)
from src.paddle import PlayerPaddle, AIPaddle
from src.ball import Ball


class GameCore:
    def __init__(self, screen):
        self.screen = screen
        self.player_paddle = PlayerPaddle()
        self.ai_paddle = AIPaddle()
        self.ball = Ball()
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner = None
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def update(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player_paddle.move_up()
        if keys[pygame.K_DOWN]:
            self.player_paddle.move_down()

        self.ai_paddle.update(self.ball)

        self.ball.move()
        self.ball.check_wall_collision()
        self.ball.check_paddle_collision(self.player_paddle)
        self.ball.check_paddle_collision(self.ai_paddle)

        self.check_score()

    def check_score(self):
        if self.ball.is_out_of_bounds_left():
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.is_out_of_bounds_right():
            self.player_score += 1
            self.ball.reset()

        if self.player_score >= WIN_SCORE:
            self.game_over = True
            self.winner = "玩家"
        elif self.ai_score >= WIN_SCORE:
            self.game_over = True
            self.winner = "AI"

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        pygame.draw.line(
            self.screen, WHITE,
            (SCREEN_WIDTH // 2, 0),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT),
            2
        )

        self.player_paddle.draw(self.screen)
        self.ai_paddle.draw(self.screen)
        self.ball.draw(self.screen)

        self.draw_score()

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def draw_score(self):
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        self.screen.blit(player_text, (SCREEN_WIDTH // 4, 20))
        self.screen.blit(ai_text, (3 * SCREEN_WIDTH // 4, 20))

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        text = self.font.render(f"{self.winner}获胜!", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)

        restart_text = self.small_font.render(
            "按空格键重新开始", True, WHITE
        )
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        )
        self.screen.blit(restart_text, restart_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.reset_game()

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner = None
        self.ball.reset()
        self.player_paddle = PlayerPaddle()
        self.ai_paddle = AIPaddle()