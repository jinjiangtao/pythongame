import pygame
import math
import sys
import random
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    EXP_PER_LEVEL
)
from player import Player
from enemy import Enemy
from weapon import Weapon
from particle import ExperienceOrb, HitParticle
from upgrade import UpgradeManager


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("吸血鬼幸存者 - Python版")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    player = Player()
    weapon = Weapon()
    upgrade_manager = UpgradeManager()
    enemies = []
    experience_orbs = []
    hit_particles = []

    game_state = "playing"
    current_upgrades = []
    upgrade_buttons = []

    last_spawn_time = 0
    spawn_interval = 2000
    game_time = 0
    difficulty = 1.0

    running = True
    while running:
        dt = clock.tick(FPS)
        game_time += dt

        difficulty = 1.0 + (game_time / 60000) * 2.0
        spawn_interval = max(500, 2000 - (game_time / 1000) * 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and game_state == "upgrading":
                for rect, upgrade in upgrade_buttons:
                    if rect.collidepoint(event.pos):
                        upgrade_manager.apply_upgrade(upgrade, player, weapon)
                        game_state = "playing"
                        break

        keys = pygame.key.get_pressed()

        if game_state == "playing":
            player.update(keys, SCREEN_WIDTH, SCREEN_HEIGHT)

            now = pygame.time.get_ticks()
            if now - last_spawn_time > spawn_interval:
                enemy = Enemy(difficulty)
                enemies.append(enemy)
                last_spawn_time = now

            for enemy in enemies:
                enemy.update(player)

            for orb in experience_orbs:
                orb.update(player)

            for particle in hit_particles:
                particle.update()

            hit_enemies = weapon.attack(player, enemies, hit_particles)
            if hit_enemies:
                for enemy in hit_enemies:
                    enemy.hp -= weapon.damage
                    hit_particles.append(HitParticle(enemy.x, enemy.y))

            new_enemies = []
            for enemy in enemies:
                if enemy.hp <= 0:
                    experience_orbs.append(ExperienceOrb(enemy.x, enemy.y))
                else:
                    new_enemies.append(enemy)
            enemies = new_enemies

            new_orbs = []
            for orb in experience_orbs:
                dx = player.x - orb.x
                dy = player.y - orb.y
                dist = math.hypot(dx, dy)
                if dist < player.radius + orb.radius:
                    player.exp += orb.value
                else:
                    new_orbs.append(orb)
            experience_orbs = new_orbs

            if player.exp >= player.exp_to_next_level:
                player.exp -= player.exp_to_next_level
                player.level += 1
                player.exp_to_next_level = int(EXP_PER_LEVEL * (1 + (player.level - 1) * 0.5))
                current_upgrades = upgrade_manager.get_random_upgrades(3)
                game_state = "upgrading"

            for enemy in enemies:
                dx = player.x - enemy.x
                dy = player.y - enemy.y
                dist = math.hypot(dx, dy)
                if dist < player.radius + enemy.radius:
                    player.hp -= 0.5
                    if player.hp <= 0:
                        player.alive = False
                        game_state = "game_over"

            hit_particles = [p for p in hit_particles if p.alive]

        screen.fill((30, 30, 30))

        if game_state == "playing":
            pygame.draw.circle(screen, (100, 100, 100), (int(player.x), int(player.y)), weapon.attack_range, 2)

            for orb in experience_orbs:
                orb.draw(screen)

            for particle in hit_particles:
                particle.draw(screen)

            for enemy in enemies:
                enemy.draw(screen)

            player.draw(screen)

            hp_bar_width = 200
            hp_bar_height = 20
            hp_fill = (player.hp / player.max_hp) * hp_bar_width
            pygame.draw.rect(screen, (255, 0, 0), (20, 20, hp_bar_width, hp_bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (20, 20, hp_fill, hp_bar_height))
            hp_text = font.render(f"HP: {int(player.hp)}/{player.max_hp}", True, (255, 255, 255))
            screen.blit(hp_text, (20, 50))

            exp_bar_width = 200
            exp_bar_height = 20
            exp_fill = (player.exp / player.exp_to_next_level) * exp_bar_width
            pygame.draw.rect(screen, (100, 100, 100), (20, 80, exp_bar_width, exp_bar_height))
            pygame.draw.rect(screen, (255, 215, 0), (20, 80, exp_fill, exp_bar_height))
            exp_text = font.render(f"EXP: {player.exp}/{player.exp_to_next_level}", True, (255, 255, 255))
            screen.blit(exp_text, (20, 110))

            level_text = font.render(f"等级: {player.level}", True, (255, 255, 255))
            screen.blit(level_text, (20, 140))

        elif game_state == "upgrading":
            player.draw(screen)
            for orb in experience_orbs:
                orb.draw(screen)
            for enemy in enemies:
                enemy.draw(screen)
            upgrade_buttons = upgrade_manager.draw_upgrade_menu(screen, current_upgrades, SCREEN_WIDTH, SCREEN_HEIGHT)

        elif game_state == "game_over":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))
            game_over_text = font.render("游戏结束! 按R重新开始", True, (255, 255, 255))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)

            if keys[pygame.K_r]:
                player = Player()
                weapon = Weapon()
                enemies = []
                experience_orbs = []
                hit_particles = []
                game_state = "playing"
                game_time = 0
                difficulty = 1.0
                last_spawn_time = 0

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
