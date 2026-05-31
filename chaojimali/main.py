import pygame
import sys

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, FONT_SIZE, COIN_VALUE
from player import Player
from world import World
from camera import Camera

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Mario Style Game")
        
        self.font = pygame.font.Font(None, FONT_SIZE)
        
        self.world = World()
        self.player = Player(100, SCREEN_HEIGHT - 150)
        self.camera = Camera()
        
        self.score = 0
        self.coin_count = 0
        
        self.game_over = False
        self.clock = pygame.time.Clock()
        
        self.coin_sound = None
        try:
            self.coin_sound = pygame.mixer.Sound('coin.wav')
        except FileNotFoundError:
            pass
    
    def play_coin_sound(self):
        if self.coin_sound:
            self.coin_sound.play()
    
    def check_coin_collisions(self):
        for coin in self.world.coins:
            if not coin.collected and self.player.rect.colliderect(coin.rect):
                coin.collect()
                self.coin_count += 1
                self.score += COIN_VALUE
                self.play_coin_sound()
    
    def check_enemy_collisions(self):
        for enemy in self.world.enemies:
            if not enemy.alive:
                continue
            
            if self.player.rect.colliderect(enemy.rect):
                if self.player.velocity_y > 0 and self.player.y + self.player.height - 10 <= enemy.y:
                    enemy.die()
                    self.score += 100
                    self.player.velocity_y = -8
                else:
                    self.game_over = True
    
    def draw_ui(self):
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        coin_text = self.font.render(f"Coins: {self.coin_count}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(coin_text, (10, 40))
    
    def draw_game_over(self):
        game_over_text = self.font.render("GAME OVER", True, BLACK)
        restart_text = self.font.render("Press R to restart", True, BLACK)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def restart(self):
        self.world = World()
        self.player = Player(100, SCREEN_HEIGHT - 150)
        self.camera = Camera()
        self.score = 0
        self.coin_count = 0
        self.game_over = False
    
    def run(self):
        running = True
        while running:
            self.screen.fill(WHITE)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.restart()
            
            if not self.game_over:
                self.player.handle_input()
                self.player.update(self.world.platforms)
                self.camera.update(self.player.x, self.world.world_width)
                
                for enemy in self.world.enemies:
                    enemy.update()
                
                for coin in self.world.coins:
                    coin.update()
                
                self.check_coin_collisions()
                self.check_enemy_collisions()
                
                for platform in self.world.platforms:
                    platform.draw(self.screen, self.camera.x)
                
                for coin in self.world.coins:
                    coin.draw(self.screen, self.camera.x)
                
                for enemy in self.world.enemies:
                    enemy.draw(self.screen, self.camera.x)
                
                self.player.draw(self.screen, self.camera.x)
                
                self.draw_ui()
            else:
                for platform in self.world.platforms:
                    platform.draw(self.screen, self.camera.x)
                self.player.draw(self.screen, self.camera.x)
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()