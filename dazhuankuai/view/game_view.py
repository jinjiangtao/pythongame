import pygame

class GameView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.grey = (100, 100, 100)

    def render(self, game_model):
        self.screen.fill(self.black)
        self._render_bricks(game_model.bricks)
        self._render_paddle(game_model.paddle)
        self._render_balls(game_model.balls)
        self._render_props(game_model.props)
        self._render_score_animations(game_model.score_animations)
        self._render_ui(game_model)
        self._render_explosions(game_model.explosions)
        if game_model.paused:
            self._render_pause_overlay()

    def _render_bricks(self, bricks):
        for brick in bricks:
            if not brick.destroyed:
                color = brick.get_color()
                rect = pygame.Rect(brick.x, brick.y, brick.width, brick.height)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.white, rect, 2)
                if brick.type in ['reinforced', 'hardened']:
                    text = self.small_font.render(str(brick.hits_remaining), True, self.white)
                    text_rect = text.get_rect(center=brick.get_center())
                    self.screen.blit(text, text_rect)

    def _render_paddle(self, paddle):
        if paddle:
            paddle_rect = pygame.Rect(
                paddle.x - paddle.width // 2,
                paddle.y - paddle.height // 2,
                paddle.width,
                paddle.height
            )
            gradient = pygame.Surface((paddle.width, paddle.height))
            for i in range(paddle.height):
                ratio = i / paddle.height
                color = (
                    int(100 + 155 * ratio),
                    int(150 + 105 * ratio),
                    int(255 * ratio)
                )
                pygame.draw.line(gradient, color, (0, i), (paddle.width, i))
            self.screen.blit(gradient, paddle_rect)
            pygame.draw.rect(self.screen, self.white, paddle_rect, 2)
            if paddle.suck_balls:
                glow = pygame.Surface((paddle.width + 20, paddle.height + 10), pygame.SRCALPHA)
                pygame.draw.ellipse(glow, (0, 255, 255, 50), glow.get_rect())
                self.screen.blit(glow, (paddle.x - paddle.width // 2 - 10, paddle.y - paddle.height // 2 - 5))

    def _render_balls(self, balls):
        for ball in balls:
            if ball.invincible:
                for i in range(3):
                    radius = ball.radius + i * 2
                    alpha = max(0, 50 - i * 20)
                    glow = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(glow, (255, 255, 255, alpha), (radius, radius), radius)
                    self.screen.blit(glow, (ball.x - radius, ball.y - radius))
            self._render_trail(ball)
            pygame.draw.circle(self.screen, self.white, (int(ball.x), int(ball.y)), ball.radius)
            pygame.draw.circle(self.screen, (200, 200, 255), (int(ball.x), int(ball.y)), ball.radius - 2)

    def _render_trail(self, ball):
        for i, (tx, ty) in enumerate(ball.trail):
            alpha = int(50 * (i / len(ball.trail)))
            radius = ball.radius * (i / len(ball.trail))
            pygame.draw.circle(self.screen, (200, 200, 255, alpha), (int(tx), int(ty)), int(radius))

    def _render_props(self, props):
        for prop in props:
            if not prop.collected:
                pygame.draw.circle(self.screen, prop.color, (int(prop.x), int(prop.y)), prop.radius)
                pygame.draw.circle(self.screen, self.white, (int(prop.x), int(prop.y)), prop.radius, 2)
                text = self.small_font.render(prop.symbol, True, self.black)
                text_rect = text.get_rect(center=(prop.x, prop.y))
                self.screen.blit(text, text_rect)

    def _render_score_animations(self, animations):
        for anim in animations:
            alpha = max(0, 255 - anim['frame'] * 8)
            text = self.font.render(f"+{anim['points']}", True, (255, 200, 0, alpha))
            text_rect = text.get_rect(center=(anim['x'], anim['y']))
            self.screen.blit(text, text_rect)

    def _render_ui(self, game_model):
        score_text = self.font.render(f"得分: {game_model.score}", True, self.white)
        high_score_text = self.small_font.render(f"最高分: {game_model.high_score}", True, self.grey)
        level_text = self.font.render(f"关卡: {game_model.current_level}", True, self.white)
        
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(high_score_text, (20, 50))
        self.screen.blit(level_text, (self.screen.get_width() - 120, 20))
        
        for i in range(game_model.lives):
            heart = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.polygon(heart, (255, 50, 50), [
                (10, 2), (12, 8), (20, 8), (14, 13), (16, 20),
                (10, 15), (4, 20), (6, 13), (0, 8), (8, 8)
            ])
            self.screen.blit(heart, (self.screen.get_width() - 120 + i * 25, 50))

    def _render_explosions(self, explosions):
        for exp in explosions:
            radius = exp.get('radius', 10)
            alpha = int(255 * (1 - exp.get('frame', 0) / 30))
            pygame.draw.circle(self.screen, (255, 200, 50, alpha), 
                              (int(exp['x']), int(exp['y'])), radius)
            pygame.draw.circle(self.screen, (255, 100, 0, alpha), 
                              (int(exp['x']), int(exp['y'])), int(radius * 0.6))
            pygame.draw.circle(self.screen, (255, 255, 255, alpha), 
                              (int(exp['x']), int(exp['y'])), int(radius * 0.3))

    def _render_pause_overlay(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        pause_text = self.font.render("游戏暂停", True, self.white)
        continue_text = self.small_font.render("按空格键继续", True, self.grey)
        pause_rect = pause_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 20))
        continue_rect = continue_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 20))
        self.screen.blit(pause_text, pause_rect)
        self.screen.blit(continue_text, continue_rect)
