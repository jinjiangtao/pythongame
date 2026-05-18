import pygame
from src.config import *
from src.tank import Tank
from src.map import GameMap

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.level = 1
        self.game_state = "playing"
        self.score = 0
        
        self.player = None
        self.enemies = []
        self.bullets = []
        self.game_map = None
        
        self.last_enemy_spawn_time = 0
        self.enemy_spawn_interval = 3000
        
        self.init_level()
    
    def init_level(self):
        self.game_map = GameMap(self.level)
        self.player = Tank(SCREEN_WIDTH // 2 - GRID_SIZE, 
                          SCREEN_HEIGHT - GRID_SIZE * 2, 
                          DIR_UP, 
                          is_player=True)
        self.enemies = []
        self.bullets = []
        self.spawn_enemies()
    
    def spawn_enemies(self):
        enemy_count = ENEMY_COUNT_PER_LEVEL[min(self.level - 1, len(ENEMY_COUNT_PER_LEVEL) - 1)]
        spawn_positions = [
            (GRID_SIZE, GRID_SIZE),
            (SCREEN_WIDTH // 2 - GRID_SIZE // 2, GRID_SIZE),
            (SCREEN_WIDTH - GRID_SIZE * 2, GRID_SIZE)
        ]
        
        for i in range(enemy_count):
            x, y = spawn_positions[i % len(spawn_positions)]
            enemy = Tank(x + (i // len(spawn_positions)) * GRID_SIZE * 3, 
                        y, 
                        DIR_DOWN, 
                        is_player=False)
            self.enemies.append(enemy)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_state == "playing":
                    bullet = self.player.shoot(pygame.time.get_ticks())
                    if bullet:
                        self.bullets.append(bullet)
                elif event.key == pygame.K_r:
                    if self.game_state in ["game_over", "victory"]:
                        self.level = 1
                        self.score = 0
                        self.game_state = "playing"
                        self.init_level()
    
    def update(self):
        if self.game_state != "playing":
            return
        
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        
        self.player.update(keys, current_time)
        
        old_player_rect = self.player.get_rect()
        new_player_rect = self.player.get_rect()
        
        if self.game_map.check_collision(new_player_rect):
            self.player.x = old_player_rect.x
            self.player.y = old_player_rect.y
        
        for enemy in self.enemies[:]:
            enemy.update(None, current_time)
            
            old_enemy_rect = enemy.get_rect()
            
            if self.game_map.check_collision(enemy.get_rect()):
                enemy.x = old_enemy_rect.x
                enemy.y = old_enemy_rect.y
                enemy.direction = (enemy.direction + 1) % 4
            
            if enemy.get_rect().colliderect(self.player.get_rect()):
                enemy.x = old_enemy_rect.x
                enemy.y = old_enemy_rect.y
            
            for other_enemy in self.enemies:
                if enemy != other_enemy and enemy.get_rect().colliderect(other_enemy.get_rect()):
                    enemy.x = old_enemy_rect.x
                    enemy.y = old_enemy_rect.y
                    break
            
            if enemy.ai_should_shoot():
                bullet = enemy.shoot(current_time)
                if bullet:
                    self.bullets.append(bullet)
        
        for bullet in self.bullets[:]:
            bullet.update()
            
            if not bullet.active:
                self.bullets.remove(bullet)
                continue
            
            collision_result, _ = self.game_map.check_bullet_collision(bullet)
            if collision_result == "destroy":
                self.bullets.remove(bullet)
                continue
            elif collision_result == "block":
                self.bullets.remove(bullet)
                continue
            elif collision_result == "base":
                self.game_state = "game_over"
                return
            
            if bullet.is_player:
                for enemy in self.enemies[:]:
                    if bullet.get_rect().colliderect(enemy.get_rect()):
                        if enemy.take_damage():
                            self.enemies.remove(enemy)
                            self.score += 100
                        self.bullets.remove(bullet)
                        break
            else:
                if bullet.get_rect().colliderect(self.player.get_rect()):
                    if self.player.take_damage():
                        self.game_state = "game_over"
                    self.bullets.remove(bullet)
        
        if not self.enemies:
            self.game_state = "victory"
    
    def next_level(self):
        self.level += 1
        self.game_state = "playing"
        self.init_level()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        self.game_map.draw(self.screen)
        
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        self.player.draw(self.screen)
        
        self.game_map.draw_grass(self.screen)
        
        self.draw_hud()
        
        if self.game_state == "game_over":
            self.draw_game_over()
        elif self.game_state == "victory":
            self.draw_victory()
    
    def draw_hud(self):
        score_text = FONT.render(f"得分: {self.score}", True, WHITE)
        level_text = FONT.render(f"关卡: {self.level}", True, WHITE)
        health_text = FONT.render(f"生命: {self.player.health}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 10))
        self.screen.blit(health_text, (SCREEN_WIDTH - health_text.get_width() - 10, 10))
    
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = FONT.render("游戏结束", True, RED)
        score_text = FONT.render(f"最终得分: {self.score}", True, WHITE)
        restart_text = FONT.render("按 R 重新开始", True, GREEN)
        
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                        SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
                                    SCREEN_HEIGHT // 2))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                                        SCREEN_HEIGHT // 2 + 50))
    
    def draw_victory(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        victory_text = FONT.render("关卡完成!", True, YELLOW)
        score_text = FONT.render(f"当前得分: {self.score}", True, WHITE)
        next_level_text = FONT.render("按 R 进入下一关", True, GREEN)
        
        self.screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, 
                                        SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
                                    SCREEN_HEIGHT // 2))
        self.screen.blit(next_level_text, (SCREEN_WIDTH // 2 - next_level_text.get_width() // 2, 
                                        SCREEN_HEIGHT // 2 + 50))