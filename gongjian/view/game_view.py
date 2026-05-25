import pygame
import math

class GameView:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 72)

    def draw_background(self):
        sky_gradient = pygame.Surface((self.width, self.height))
        for y in range(self.height):
            color = (135, 206, 230 - int(y * 0.3))
            pygame.draw.line(sky_gradient, color, (0, y), (self.width, y))
        self.screen.blit(sky_gradient, (0, 0))

        for i in range(3):
            cloud_x = (i * 300 + pygame.time.get_ticks() // 50) % (self.width + 100) - 50
            self.draw_cloud(cloud_x, 50 + i * 30)

        pygame.draw.rect(self.screen, (34, 139, 34), (0, self.height - 80, self.width, 80))

        for i in range(10):
            tree_x = i * 80 + 20
            self.draw_tree(tree_x, self.height - 80)

    def draw_cloud(self, x, y):
        cloud_color = (255, 255, 255)
        pygame.draw.circle(self.screen, cloud_color, (x, y), 30)
        pygame.draw.circle(self.screen, cloud_color, (x + 25, y - 10), 25)
        pygame.draw.circle(self.screen, cloud_color, (x + 50, y), 30)

    def draw_tree(self, x, ground_y):
        pygame.draw.rect(self.screen, (139, 69, 19), (x - 8, ground_y - 30, 16, 30))
        pygame.draw.polygon(self.screen, (34, 139, 34), [
            (x, ground_y - 60),
            (x - 25, ground_y - 30),
            (x + 25, ground_y - 30)
        ])
        pygame.draw.polygon(self.screen, (22, 88, 22), [
            (x, ground_y - 45),
            (x - 18, ground_y - 30),
            (x + 18, ground_y - 30)
        ])

    def draw_archer(self, archer):
        body_x = archer.x
        body_y = archer.y

        pygame.draw.circle(self.screen, (255, 255, 255), (body_x, body_y - 35), 12)
        pygame.draw.rect(self.screen, (0, 100, 200), (body_x - 12, body_y - 23, 24, 30))
        pygame.draw.line(self.screen, (255, 255, 255), (body_x - 12, body_y), (body_x - 25, body_y + 15), 3)
        pygame.draw.line(self.screen, (255, 255, 255), (body_x + 12, body_y), (body_x + 25, body_y + 15), 3)
        pygame.draw.line(self.screen, (255, 255, 255), (body_x - 8, body_y - 15), (body_x - 25, body_y - 10), 3)

        bow_length = 30 + archer.power // 3
        start_x = body_x + 15
        start_y = body_y - 20
        end_x = start_x + bow_length * math.cos(math.radians(archer.angle))
        end_y = start_y + bow_length * math.sin(math.radians(archer.angle))

        pygame.draw.line(self.screen, (139, 69, 19), (start_x, start_y), (end_x, end_y), 4)
        pygame.draw.line(self.screen, (139, 69, 19), (start_x, start_y), (start_x - 8, start_y - 5), 3)
        pygame.draw.line(self.screen, (139, 69, 19), (end_x, end_y), (end_x + 8, end_y - 5), 3)

        if archer.is_charging:
            string_x = start_x - 10 * math.cos(math.radians(archer.angle))
            string_y = start_y - 10 * math.sin(math.radians(archer.angle))
            pygame.draw.line(self.screen, (200, 200, 200), (start_x, start_y), (string_x, string_y), 2)
            pygame.draw.line(self.screen, (200, 200, 200), (end_x, end_y), (string_x, string_y), 2)

            arrow_x = string_x + 15 * math.cos(math.radians(archer.angle))
            arrow_y = string_y + 15 * math.sin(math.radians(archer.angle))
            self.draw_arrow_at_position(arrow_x, arrow_y, archer.angle)

    def draw_arrow_at_position(self, x, y, angle):
        arrow_surface = pygame.Surface((30, 6), pygame.SRCALPHA)
        pygame.draw.rect(arrow_surface, (169, 169, 169), (0, 0, 25, 6))
        pygame.draw.polygon(arrow_surface, (200, 100, 50), [
            (25, 3),
            (30, 0),
            (25, 6)
        ])
        rotated = pygame.transform.rotate(arrow_surface, -angle)
        rect = rotated.get_rect(center=(x, y))
        self.screen.blit(rotated, rect)

    def draw_arrow(self, arrow):
        self.draw_arrow_at_position(arrow.x, arrow.y, arrow.angle)

    def draw_target(self, target):
        colors = {
            'normal': (255, 0, 0),
            'fast': (255, 165, 0),
            'bonus': (0, 255, 0)
        }
        color = colors.get(target.type, (255, 0, 0))
        
        pygame.draw.circle(self.screen, color, (target.x, target.y), target.width // 2)
        pygame.draw.circle(self.screen, (255, 255, 255), (target.x, target.y), target.width // 3)
        pygame.draw.circle(self.screen, color, (target.x, target.y), target.width // 6)

    def draw_flying_target(self, target):
        pygame.draw.ellipse(self.screen, (255, 100, 100), 
                           (target.x - target.width // 2, target.y - target.height // 2, 
                            target.width, target.height))
        pygame.draw.line(self.screen, (0, 0, 0), (target.x - 10, target.y), (target.x + 10, target.y), 2)
        pygame.draw.circle(self.screen, (255, 255, 255), (target.x - 5, target.y - 5), 4)
        pygame.draw.circle(self.screen, (255, 255, 255), (target.x + 5, target.y - 5), 4)
        pygame.draw.circle(self.screen, (0, 0, 0), (target.x - 5, target.y - 5), 2)
        pygame.draw.circle(self.screen, (0, 0, 0), (target.x + 5, target.y - 5), 2)

    def draw_power_up(self, power_up):
        colors = {
            'arrow': (255, 200, 100),
            'score': (200, 100, 255),
            'health': (100, 200, 255)
        }
        icons = {
            'arrow': '箭',
            'score': '分',
            'health': '命'
        }
        color = colors.get(power_up.type, (255, 255, 255))
        
        pygame.draw.circle(self.screen, color, (power_up.x, power_up.y), power_up.width // 2)
        pygame.draw.circle(self.screen, (255, 255, 255), (power_up.x, power_up.y), power_up.width // 2, 2)
        
        text = self.small_font.render(icons[power_up.type], True, (0, 0, 0))
        text_rect = text.get_rect(center=(power_up.x, power_up.y))
        self.screen.blit(text, text_rect)

    def draw_ui(self, game_state):
        score_text = self.font.render(f"得分: {game_state.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))

        arrows_text = self.font.render(f"箭矢: {game_state.arrows}", True, (255, 255, 255))
        self.screen.blit(arrows_text, (20, 60))

        lives_text = self.font.render(f"生命: {'❤' * game_state.lives}", True, (255, 0, 0))
        self.screen.blit(lives_text, (20, 100))

        level_text = self.font.render(f"关卡: {game_state.level}", True, (255, 255, 255))
        self.screen.blit(level_text, (self.width - 120, 20))

        if game_state.paused:
            pause_text = self.large_font.render("游戏暂停", True, (255, 255, 0))
            pause_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(pause_text, pause_rect)

            hint_text = self.font.render("按 P 键继续游戏", True, (255, 255, 255))
            hint_rect = hint_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
            self.screen.blit(hint_text, hint_rect)

        if game_state.game_over:
            game_over_text = self.large_font.render("游戏结束", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
            self.screen.blit(game_over_text, game_over_rect)

            final_score = self.font.render(f"最终得分: {game_state.score}", True, (255, 255, 255))
            score_rect = final_score.get_rect(center=(self.width // 2, self.height // 2 + 10))
            self.screen.blit(final_score, score_rect)

            restart_text = self.font.render("按 R 键重新开始", True, (0, 255, 0))
            restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 70))
            self.screen.blit(restart_text, restart_rect)

    def draw_message(self, game_state):
        if game_state.message and pygame.time.get_ticks() - game_state.message_time < 1500:
            message_text = self.font.render(game_state.message, True, (255, 255, 0))
            message_rect = message_text.get_rect(center=(self.width // 2, self.height - 100))
            pygame.draw.rect(self.screen, (0, 0, 0, 150), 
                           (message_rect.left - 10, message_rect.top - 5, 
                            message_rect.width + 20, message_rect.height + 10))
            self.screen.blit(message_text, message_rect)

    def draw_instructions(self):
        instructions = [
            "← → 移动射手",
            "鼠标左键按住蓄力",
            "松开鼠标发射箭矢",
            "P 暂停/继续",
            "ESC 退出游戏"
        ]
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, (255, 255, 255))
            self.screen.blit(text, (self.width - 180, 60 + i * 30))

    def draw_power_bar(self, archer):
        if archer.is_charging:
            bar_width = 200
            bar_height = 15
            bar_x = self.width // 2 - bar_width // 2
            bar_y = self.height - 50

            pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            
            power_color = (0, 255, 0)
            if archer.power > 70:
                power_color = (255, 255, 0)
            if archer.power > 90:
                power_color = (255, 0, 0)
            
            filled_width = int(bar_width * (archer.power / archer.max_power))
            pygame.draw.rect(self.screen, power_color, (bar_x, bar_y, filled_width, bar_height))
            
            power_text = self.small_font.render(f"力度: {archer.power}%", True, (255, 255, 255))
            text_rect = power_text.get_rect(center=(self.width // 2, bar_y - 10))
            self.screen.blit(power_text, text_rect)