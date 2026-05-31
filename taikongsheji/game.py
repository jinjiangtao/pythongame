import pygame
import random
from settings import *
from player import Player
from alien import AlienFleet
from bullet import Bullet

class Game:
    def __init__(self):
        self.player = Player()
        self.alien_fleet = AlienFleet()
        self.player_bullets = []
        self.alien_bullets = []
        self.score = 0
        self.level = 1
        self.state = "start"
        self.show_level_text = False
        self.level_text_timer = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if self.state in ["gameover", "start"]:
                        self.reset_game()

                if event.key == pygame.K_SPACE:
                    if self.state == "playing":
                        self.shoot()

                if event.key == pygame.K_RETURN:
                    if self.state == "start":
                        self.state = "playing"

        return True

    def shoot(self):
        bullet = Bullet(
            self.player.x + self.player.width // 2,
            self.player.y,
            is_player_bullet=True
        )
        self.player_bullets.append(bullet)

    def alien_shoot(self):
        if self.alien_fleet.can_shoot():
            random_alien = random.choice(self.alien_fleet.aliens)
            bullet = Bullet(
                random_alien.x + random_alien.width // 2,
                random_alien.y + random_alien.height,
                is_player_bullet=False
            )
            self.alien_bullets.append(bullet)

    def update(self):
        if self.state != "playing":
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()

        self.player_bullets = [b for b in self.player_bullets if not b.is_off_screen()]
        self.alien_bullets = [b for b in self.alien_bullets if not b.is_off_screen()]

        for bullet in self.player_bullets:
            bullet.update()

        for bullet in self.alien_bullets:
            bullet.update()

        self.alien_fleet.update()
        self.alien_shoot()

        for bullet in self.player_bullets[:]:
            hit_alien = self.alien_fleet.check_collision(bullet)
            if hit_alien:
                self.player_bullets.remove(bullet)
                self.alien_fleet.remove_alien(hit_alien)
                self.score += ALIEN_POINTS

        for bullet in self.alien_bullets[:]:
            if self.player.get_rect().colliderect(bullet.get_rect()):
                self.alien_bullets.remove(bullet)
                if self.player.hit():
                    self.state = "gameover"
                    return

        for alien in self.alien_fleet.aliens:
            if alien.y + alien.height >= self.player.y:
                self.state = "gameover"
                return

        if self.alien_fleet.is_empty():
            self.level += 1
            self.alien_fleet.reset(self.level)
            self.player_bullets.clear()
            self.alien_bullets.clear()
            self.show_level_text = True
            self.level_text_timer = 120

        if self.show_level_text:
            self.level_text_timer -= 1
            if self.level_text_timer <= 0:
                self.show_level_text = False

    def draw_text(self, text, font_obj, color, center_pos):
        text_surface = font_obj.render(text, True, color)
        text_rect = text_surface.get_rect(center=center_pos)
        screen.blit(text_surface, text_rect)

    def draw(self):
        screen.fill(BLACK)

        if self.state == "start":
            self.draw_text("太空侵略者", font, GREEN, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.draw_text("按 ENTER 开始游戏", small_font, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.draw_text("按 R 重开", small_font, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            self.draw_text("← → 移动  空格 射击", small_font, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
            return

        if self.state == "gameover":
            self.draw_text("GAME OVER", font, RED, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.draw_text(f"最终得分: {self.score}", small_font, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.draw_text(f"到达第 {self.level} 关", small_font, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            self.draw_text("按 R 重新开始", small_font, GREEN, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
            return

        if self.show_level_text:
            self.draw_text(f"第 {self.level} 关!", font, YELLOW, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            return

        self.player.draw()
        self.alien_fleet.draw()

        for bullet in self.player_bullets:
            bullet.draw()

        for bullet in self.alien_bullets:
            bullet.draw()

        self.draw_text(f"得分: {self.score}", small_font, WHITE, (100, 30))
        self.draw_text(f"关卡: {self.level}", small_font, WHITE, (SCREEN_WIDTH // 2, 30))
        self.draw_text(f"生命: {self.player.lives}", small_font, WHITE, (SCREEN_WIDTH - 100, 30))

    def reset_game(self):
        self.player.reset()
        self.alien_fleet.reset(1)
        self.player_bullets.clear()
        self.alien_bullets.clear()
        self.score = 0
        self.level = 1
        self.state = "playing"
        self.show_level_text = False
