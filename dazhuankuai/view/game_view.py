import pygame

class GameView:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.colors = {
            'background': (10, 10, 30),
            'paddle': (100, 200, 255),
            'paddle_sticky': (255, 150, 100),
            'ball': (255, 255, 255),
            'trail': (100, 150, 255),
            'normal_brick': (100, 150, 255),
            'reinforced_brick': (150, 100, 255),
            'indestructible_brick': (80, 80, 80),
            'explosive_brick': (255, 100, 100),
            'text': (255, 255, 255),
            'score': (255, 200, 100)
        }
        
        self.hit_effects = []
        self.score_animations = []

    def add_hit_effect(self, x, y, color):
        self.hit_effects.append({
            'x': x,
            'y': y,
            'color': color,
            'radius': 5,
            'max_radius': 25,
            'alpha': 255
        })

    def add_score_animation(self, x, y, points):
        self.score_animations.append({
            'x': x,
            'y': y,
            'points': points,
            'offset_y': 0,
            'alpha': 255
        })

    def update_effects(self):
        for effect in self.hit_effects[:]:
            effect['radius'] += 2
            effect['alpha'] -= 10
            if effect['alpha'] <= 0:
                self.hit_effects.remove(effect)
        
        for anim in self.score_animations[:]:
            anim['offset_y'] -= 2
            anim['alpha'] -= 5
            if anim['alpha'] <= 0:
                self.score_animations.remove(anim)

    def draw_background(self):
        self.screen.fill(self.colors['background'])
        
        for i in range(0, self.width, 40):
            pygame.draw.line(self.screen, (30, 30, 60), (i, 0), (i, self.height), 1)
        for i in range(0, self.height, 40):
            pygame.draw.line(self.screen, (30, 30, 60), (0, i), (self.width, i), 1)

    def draw_paddle(self, paddle_rect, is_sticky):
        x, y, w, h = paddle_rect
        
        color = self.colors['paddle_sticky'] if is_sticky else self.colors['paddle']
        
        pygame.draw.rect(self.screen, color, (x, y, w, h), border_radius=5)
        
        pygame.draw.rect(self.screen, (255, 255, 255), (x + 5, y + 2, w - 10, 4), border_radius=2)

    def draw_ball(self, ball_rect, trail, is_invincible):
        x, y, w, h = ball_rect
        
        for i, (tx, ty) in enumerate(trail):
            alpha = int(255 * (i / len(trail)) * 0.5)
            size = int(w * (i / len(trail)))
            pygame.draw.circle(self.screen, (self.colors['trail'][0], self.colors['trail'][1], self.colors['trail'][2], alpha), 
                               (int(tx + w/2), int(ty + h/2)), size)
        
        color = (255, 200, 100) if is_invincible else self.colors['ball']
        pygame.draw.circle(self.screen, color, (int(x + w/2), int(y + h/2)), int(w/2))
        
        if is_invincible:
            pygame.draw.circle(self.screen, (255, 255, 255), (int(x + w/2), int(y + h/2)), int(w/2), 2)

    def draw_bricks(self, bricks):
        for brick in bricks:
            if brick.is_destroyed():
                continue
            
            x, y, w, h = brick.get_rect()
            
            if brick.type == 'normal':
                color = self.colors['normal_brick']
            elif brick.type == 'reinforced':
                color = self.colors['reinforced_brick']
                if brick.health == 1:
                    color = (200, 150, 255)
            elif brick.type == 'indestructible':
                color = self.colors['indestructible_brick']
            elif brick.type == 'explosive':
                color = self.colors['explosive_brick']
            else:
                color = self.colors['normal_brick']
            
            pygame.draw.rect(self.screen, color, (x, y, w, h), border_radius=3)
            
            pygame.draw.rect(self.screen, (255, 255, 255), (x + 2, y + 2, w - 4, 3), border_radius=1)
            
            if brick.type == 'reinforced' and brick.max_health > 1:
                health_ratio = brick.health / brick.max_health
                pygame.draw.rect(self.screen, (255, 255, 255), 
                               (x + 2, y + h - 5, int((w - 4) * health_ratio), 3), border_radius=1)
            
            if brick.type == 'indestructible':
                pygame.draw.line(self.screen, (120, 120, 120), (x + 10, y + h//2), (x + w - 10, y + h//2), 2)
                pygame.draw.line(self.screen, (120, 120, 120), (x + w//2, y + 5), (x + w//2, y + h - 5), 2)

    def draw_props(self, props):
        prop_colors = {
            'paddle_expand': (100, 255, 100),
            'paddle_shrink': (255, 100, 100),
            'ball_accelerate': (255, 200, 50),
            'ball_decelerate': (50, 200, 255),
            'ball_split': (200, 100, 255),
            'extra_life': (255, 100, 200),
            'sticky_paddle': (255, 150, 100),
            'invincible': (255, 255, 100)
        }
        
        prop_symbols = {
            'paddle_expand': '↔',
            'paddle_shrink': '↕',
            'ball_accelerate': '▲',
            'ball_decelerate': '▼',
            'ball_split': '✦',
            'extra_life': '♥',
            'sticky_paddle': '●',
            'invincible': '★'
        }
        
        for prop in props:
            x, y, w, h = prop.get_rect()
            color = prop_colors.get(prop.type, (200, 200, 200))
            
            pygame.draw.rect(self.screen, color, (x, y, w, h), border_radius=5)
            
            symbol = prop_symbols.get(prop.type, '?')
            text = self.small_font.render(symbol, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + w//2, y + h//2))
            self.screen.blit(text, text_rect)

    def draw_score(self, score, high_score):
        score_text = self.font.render(f"得分: {score}", True, self.colors['score'])
        high_score_text = self.small_font.render(f"最高分: {high_score}", True, (200, 200, 200))
        
        self.screen.blit(score_text, (20, 15))
        self.screen.blit(high_score_text, (20, 50))

    def draw_lives(self, lives):
        life_icon = '♥'
        lives_text = self.font.render(f"生命: {' '.join([life_icon] * lives)}", True, (255, 100, 100))
        self.screen.blit(lives_text, (self.width - 200, 15))

    def draw_level(self, level):
        level_text = self.font.render(f"关卡: {level}", True, (100, 255, 200))
        self.screen.blit(level_text, (self.width // 2 - 60, 15))

    def draw_paused(self):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        paused_text = self.font.render("游戏暂停", True, (255, 255, 255))
        resume_text = self.small_font.render("按 P 键继续", True, (200, 200, 200))
        
        self.screen.blit(paused_text, (self.width // 2 - 80, self.height // 2 - 30))
        self.screen.blit(resume_text, (self.width // 2 - 70, self.height // 2 + 10))

    def draw_effects(self):
        for effect in self.hit_effects:
            pygame.draw.circle(self.screen, 
                               (effect['color'][0], effect['color'][1], effect['color'][2], effect['alpha']),
                               (int(effect['x']), int(effect['y'])),
                               int(effect['radius']))
        
        for anim in self.score_animations:
            text = self.small_font.render(f"+{anim['points']}", True, (255, 200, 100))
            text.set_alpha(anim['alpha'])
            self.screen.blit(text, (anim['x'], anim['y'] + anim['offset_y']))

    def render(self, paddle_rect, balls, bricks, props, score, high_score, lives, level, is_paused, is_invincible):
        self.draw_background()
        self.draw_bricks(bricks)
        self.draw_props(props)
        self.draw_paddle(paddle_rect, False)
        
        for ball in balls:
            if ball.active:
                self.draw_ball(ball.get_rect(), ball.get_trail(), is_invincible)
        
        self.draw_score(score, high_score)
        self.draw_lives(lives)
        self.draw_level(level)
        self.draw_effects()
        
        if is_paused:
            self.draw_paused()
        
        pygame.display.flip()