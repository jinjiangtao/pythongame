import pygame
import random
import settings
from player import Player
from cloud_platform import CloudPlatform
from ui import UIManager

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("云端平台跳跃")
        self.clock = pygame.time.Clock()
        
        self.player = Player()
        self.platforms = []
        self.ui_manager = UIManager(self.screen)
        
        self.score = 0
        self.level = 1
        self.game_state = "start"
        self.scroll_speed = settings.INITIAL_SCROLL_SPEED
        self.max_platforms = settings.MAX_PLATFORMS
        self.last_score_y = settings.SCREEN_HEIGHT
        
        self.start_button = None
        self.retry_button = None
        
        self.init_platforms()

    def init_platforms(self):
        self.platforms = []
        for i in range(self.max_platforms):
            y = settings.SCREEN_HEIGHT - i * (settings.SCREEN_HEIGHT // self.max_platforms)
            width = random.randint(settings.PLATFORM_MIN_WIDTH, settings.PLATFORM_MAX_WIDTH)
            x = random.randint(10, settings.GAME_WIDTH - width - 10)
            moving = random.random() < 0.3
            self.platforms.append(CloudPlatform(x, y, width, moving))
        
        self.platforms[0].x = settings.GAME_WIDTH // 2 - self.platforms[0].width // 2
        self.platforms[0].y = settings.SCREEN_HEIGHT - 50

    def reset_game(self):
        self.player.reset()
        self.score = 0
        self.level = 1
        self.scroll_speed = settings.INITIAL_SCROLL_SPEED
        self.last_score_y = settings.SCREEN_HEIGHT
        self.max_platforms = settings.MAX_PLATFORMS
        self.init_platforms()

    def update_level(self):
        new_level = self.score // settings.SCORE_PER_LEVEL + 1
        if new_level > self.level:
            self.level = new_level
            self.scroll_speed = (settings.INITIAL_SCROLL_SPEED + 
                               (self.level - 1) * settings.LEVEL_SPEED_INCREMENT)
            self.max_platforms = max(settings.MIN_PLATFORMS, 
                                   settings.MAX_PLATFORMS - 
                                   (self.level - 1) * settings.LEVEL_PLATFORM_DECREMENT)

    def check_collision(self):
        self.player.on_ground = False
        
        for platform in self.platforms:
            if (self.player.velocity_y > 0 and 
                self.player.rect.bottom > platform.rect.top and 
                self.player.rect.bottom < platform.rect.top + 20 and 
                self.player.rect.right > platform.rect.left and 
                self.player.rect.left < platform.rect.right):
                if self.player.y + self.player.height - self.player.velocity_y <= platform.y:
                    self.player.y = platform.y - self.player.height
                    self.player.velocity_y = 0
                    self.player.on_ground = True
                    self.player.can_double_jump = True
                    
                    if platform.y < self.last_score_y - 50:
                        self.score += settings.SCORE_PER_PLATFORM
                        self.last_score_y = platform.y

    def spawn_platforms(self):
        top_platform_y = min(p.y for p in self.platforms)
        if top_platform_y > 100:
            x, width, moving = CloudPlatform.generate_random_platform(self.level)
            new_y = top_platform_y - random.randint(
                settings.PLATFORM_SPAWN_DISTANCE_MIN + self.level * 10,
                settings.PLATFORM_SPAWN_DISTANCE_MAX + self.level * 15
            )
            self.platforms.append(CloudPlatform(x, new_y, width, moving))
            
            while len(self.platforms) > self.max_platforms:
                self.platforms.pop(0)

    def update(self):
        if self.game_state == "playing":
            keys = pygame.key.get_pressed()
            self.player.update(keys)
            
            for platform in self.platforms:
                platform.update(self.scroll_speed)
            
            self.check_collision()
            self.spawn_platforms()
            self.update_level()
            
            if self.player.y > settings.SCREEN_HEIGHT:
                self.game_state = "gameover"

    def draw(self):
        if self.game_state == "start":
            self.start_button = self.ui_manager.draw_start_screen()
        elif self.game_state == "gameover":
            self.ui_manager.draw_background()
            for platform in self.platforms:
                platform.draw(self.screen)
            self.player.draw(self.screen)
            self.retry_button = self.ui_manager.draw_game_over_screen(self.score, self.level)
        else:
            self.ui_manager.draw_background()
            for platform in self.platforms:
                platform.draw(self.screen)
            self.player.draw(self.screen)
            
            self.ui_manager.draw_game_hud(self.score, self.level, self.player.on_ground)
            self.ui_manager.draw_sidebar(self.score, self.level, self.scroll_speed)
            
            self.start_button = None
            self.retry_button = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_r and self.game_state != "start":
                    self.reset_game()
                    self.game_state = "playing"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (self.start_button and 
                    self.start_button.collidepoint(event.pos) and 
                    self.game_state == "start"):
                    self.game_state = "playing"
                if (self.retry_button and 
                    self.retry_button.collidepoint(event.pos) and 
                    self.game_state == "gameover"):
                    self.reset_game()
                    self.game_state = "playing"
        
        return True

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(settings.FPS)
