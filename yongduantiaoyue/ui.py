import pygame
import settings
import os

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = self.get_chinese_font(24)
        self.small_font = self.get_chinese_font(20)
        self.large_font = self.get_chinese_font(42)
    
    def get_chinese_font(self, size):
        fonts = [
            "simhei.ttf",
            "simkai.ttf", 
            "simsun.ttc",
            "msyh.ttc",
            "msyhbd.ttc",
            "mingliu.ttc",
            "kaiu.ttf"
        ]
        
        for font_name in fonts:
            try:
                font_path = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", font_name)
                if os.path.exists(font_path):
                    return pygame.font.Font(font_path, size)
            except:
                continue
        
        try:
            return pygame.font.SysFont("SimHei", size)
        except:
            try:
                return pygame.font.SysFont("Microsoft YaHei", size)
            except:
                return pygame.font.Font(None, size)

    def draw_background(self):
        gradient_rect = pygame.Surface((settings.GAME_WIDTH, settings.SCREEN_HEIGHT))
        for y in range(settings.SCREEN_HEIGHT):
            ratio = y / settings.SCREEN_HEIGHT
            r = int(135 + (255 - 135) * ratio * 0.3)
            g = int(206 + (255 - 206) * ratio * 0.3)
            b = int(235 + (255 - 235) * ratio * 0.3)
            pygame.draw.line(gradient_rect, (r, g, b), (0, y), (settings.GAME_WIDTH, y))
        self.screen.blit(gradient_rect, (0, 0))
        
        for i in range(5):
            cloud_x = (i * 180 + pygame.time.get_ticks() // 50 % 200) % settings.GAME_WIDTH
            cloud_y = 50 + i * 100
            pygame.draw.circle(self.screen, (255, 255, 255, 100), (cloud_x, cloud_y), 40)
            pygame.draw.circle(self.screen, (255, 255, 255, 100), (cloud_x + 30, cloud_y - 10), 35)
            pygame.draw.circle(self.screen, (255, 255, 255, 100), (cloud_x + 60, cloud_y), 40)

    def draw_sidebar(self, score, level, scroll_speed):
        pygame.draw.rect(self.screen, settings.LIGHT_BLUE, 
                        (settings.GAME_WIDTH, 0, settings.SIDE_BAR_WIDTH, settings.SCREEN_HEIGHT))
        pygame.draw.line(self.screen, settings.CLOUD_GRAY, 
                        (settings.GAME_WIDTH, 0), (settings.GAME_WIDTH, settings.SCREEN_HEIGHT), 2)
        
        title_text = self.font.render("游戏信息", True, settings.TEXT_COLOR)
        self.screen.blit(title_text, (settings.GAME_WIDTH + 20, 20))
        
        score_text = self.small_font.render(f"得分: {score}", True, settings.TEXT_COLOR)
        self.screen.blit(score_text, (settings.GAME_WIDTH + 20, 60))
        
        level_text = self.small_font.render(f"关卡: {level}", True, settings.TEXT_COLOR)
        self.screen.blit(level_text, (settings.GAME_WIDTH + 20, 90))
        
        speed_text = self.small_font.render(f"速度: {int(scroll_speed * 10)}", True, settings.TEXT_COLOR)
        self.screen.blit(speed_text, (settings.GAME_WIDTH + 20, 120))
        
        pygame.draw.line(self.screen, settings.CLOUD_GRAY, 
                        (settings.GAME_WIDTH + 10, 150), (settings.SCREEN_WIDTH - 10, 150), 1)
        
        control_title = self.font.render("操作说明", True, settings.TEXT_COLOR)
        self.screen.blit(control_title, (settings.GAME_WIDTH + 20, 170))
        
        controls = [
            "← → 左右移动",
            "空格 跳跃",
            "空格×2 二段跳",
            "R 重新开始",
            "ESC 退出游戏"
        ]
        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, settings.TEXT_COLOR)
            self.screen.blit(control_text, (settings.GAME_WIDTH + 20, 210 + i * 25))

    def draw_start_screen(self):
        self.draw_background()
        
        title_text = self.large_font.render("云端平台跳跃", True, settings.TEXT_COLOR)
        title_rect = title_text.get_rect(center=(settings.GAME_WIDTH // 2, settings.SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(title_text, title_rect)
        
        sub_text = self.font.render("使用方向键移动，空格键跳跃", True, settings.TEXT_COLOR)
        sub_rect = sub_text.get_rect(center=(settings.GAME_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
        self.screen.blit(sub_text, sub_rect)
        
        tips_text = self.small_font.render("提示：支持二段跳！踩上云朵获得分数", True, settings.TEXT_COLOR)
        tips_rect = tips_text.get_rect(center=(settings.GAME_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(tips_text, tips_rect)
        
        start_button = pygame.Rect(settings.GAME_WIDTH // 2 - 80, 
                                  settings.SCREEN_HEIGHT // 2 + 80, 160, 40)
        mouse_pos = pygame.mouse.get_pos()
        if start_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, settings.BUTTON_HOVER, start_button, border_radius=5)
        else:
            pygame.draw.rect(self.screen, settings.BUTTON_COLOR, start_button, border_radius=5)
        
        start_text = self.font.render("开始游戏", True, settings.WHITE)
        start_text_rect = start_text.get_rect(center=start_button.center)
        self.screen.blit(start_text, start_text_rect)
        
        self.draw_sidebar(0, 1, settings.INITIAL_SCROLL_SPEED)
        
        return start_button

    def draw_game_over_screen(self, score, level):
        overlay = pygame.Surface((settings.GAME_WIDTH, settings.SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(settings.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.large_font.render("游戏结束", True, settings.WHITE)
        game_over_rect = game_over_text.get_rect(center=(settings.GAME_WIDTH // 2, settings.SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(game_over_text, game_over_rect)
        
        final_score_text = self.font.render(f"最终得分: {score}", True, settings.WHITE)
        final_score_rect = final_score_text.get_rect(center=(settings.GAME_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
        self.screen.blit(final_score_text, final_score_rect)
        
        level_text = self.font.render(f"到达关卡: {level}", True, settings.WHITE)
        level_rect = level_text.get_rect(center=(settings.GAME_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(level_text, level_rect)
        
        retry_button = pygame.Rect(settings.GAME_WIDTH // 2 - 80, 
                                  settings.SCREEN_HEIGHT // 2 + 80, 160, 40)
        mouse_pos = pygame.mouse.get_pos()
        if retry_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, settings.BUTTON_HOVER, retry_button, border_radius=5)
        else:
            pygame.draw.rect(self.screen, settings.BUTTON_COLOR, retry_button, border_radius=5)
        
        retry_text = self.font.render("重新开始", True, settings.WHITE)
        retry_text_rect = retry_text.get_rect(center=retry_button.center)
        self.screen.blit(retry_text, retry_text_rect)
        
        return retry_button

    def draw_game_hud(self, score, level, on_ground):
        score_text = self.font.render(f"得分: {score}", True, settings.TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))
        
        level_text = self.font.render(f"关卡: {level}", True, settings.TEXT_COLOR)
        self.screen.blit(level_text, (150, 10))
        
        if on_ground:
            status_text = self.font.render("游戏中", True, settings.GREEN)
        else:
            status_text = self.font.render("空中", True, settings.RED)
        self.screen.blit(status_text, (290, 10))
