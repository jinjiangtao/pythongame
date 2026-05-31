import pygame
import random


class UpgradeManager:
    def __init__(self):
        self.upgrades = [
            {"name": "攻击速度+20%", "effect": "attack_speed", "value": 0.8},
            {"name": "伤害+25%", "effect": "damage", "value": 1.25},
            {"name": "移动速度+15%", "effect": "move_speed", "value": 1.15},
            {"name": "最大血量+30", "effect": "max_hp", "value": 30},
            {"name": "攻击范围+30", "effect": "attack_range", "value": 30}
        ]
        self.font = None

    def init_font(self):
        if not self.font:
            self.font = pygame.font.Font(None, 36)

    def get_random_upgrades(self, count=3):
        return random.sample(self.upgrades, count)

    def apply_upgrade(self, upgrade, player, weapon):
        effect = upgrade["effect"]
        value = upgrade["value"]
        if effect == "attack_speed":
            weapon.attack_interval = int(weapon.attack_interval * value)
        elif effect == "damage":
            weapon.damage = int(weapon.damage * value)
        elif effect == "move_speed":
            player.speed *= value
        elif effect == "max_hp":
            player.max_hp += value
            player.hp += value
        elif effect == "attack_range":
            weapon.attack_range += value

    def draw_upgrade_menu(self, surface, upgrades, screen_width, screen_height):
        self.init_font()
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        title = self.font.render("选择升级 (点击选择)", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen_width // 2, 100))
        surface.blit(title, title_rect)

        button_width = 300
        button_height = 80
        spacing = 40
        total_width = button_width * 3 + spacing * 2
        start_x = (screen_width - total_width) // 2
        y = 250

        buttons = []
        for i, upgrade in enumerate(upgrades):
            x = start_x + i * (button_width + spacing)
            button_rect = pygame.Rect(x, y, button_width, button_height)
            pygame.draw.rect(surface, (50, 50, 50), button_rect)
            pygame.draw.rect(surface, (200, 200, 200), button_rect, 2)
            text = self.font.render(upgrade["name"], True, (255, 255, 255))
            text_rect = text.get_rect(center=button_rect.center)
            surface.blit(text, text_rect)
            buttons.append((button_rect, upgrade))

        return buttons
