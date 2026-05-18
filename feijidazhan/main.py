import pygame
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_COLORS, FONT_SIZE
from src.player import Player
from src.enemy import EnemyManager
from src.bullet import BulletManager
from src.props import PropManager
from src.game_map import GameMap
from src.game_core import GameCore

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('飞机大战')
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('SimHei', FONT_SIZE)
        
        self.game_state = 'start'
        self.game_map = GameMap()
        self.game_core = GameCore('normal')
        self.player = None
        self.enemy_manager = EnemyManager()
        self.bullet_manager = BulletManager()
        self.prop_manager = PropManager()
        
        self.boss_pattern = 0
        self.boss_pattern_timer = 0
        
    def reset_game(self):
        self.game_core.reset()
        self.enemy_manager.clear_all()
        self.bullet_manager.clear_all()
        self.prop_manager.clear_all()
        spawn_pos = self.game_map.get_player_spawn_position()
        self.player = Player(spawn_pos[0], spawn_pos[1])
        self.boss_pattern = 0
        self.boss_pattern_timer = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if self.game_state == 'start':
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.game_state = 'playing'
                        
                elif self.game_state == 'playing':
                    self.player.handle_key_down(event.key)
                    
                    if event.key == pygame.K_SPACE:
                        if self.player.fire(pygame.time.get_ticks()):
                            x, y = self.player.get_position()
                            self.bullet_manager.add_player_bullets(x, y, self.player.get_power_level())
                            
                    elif event.key == pygame.K_b:
                        if self.player.use_bomb():
                            self.enemy_manager.clear_all()
                            self.bullet_manager.clear_all()
                            
                    elif event.key == pygame.K_p:
                        self.game_core.toggle_pause()
                        
                elif self.game_state == 'game_over':
                    if event.key == pygame.K_SPACE:
                        self.game_state = 'start'
                        
            elif event.type == pygame.KEYUP:
                if self.game_state == 'playing':
                    self.player.handle_key_up(event.key)
                    
    def update(self):
        if self.game_state != 'playing' or self.game_core.is_paused():
            return
            
        current_time = pygame.time.get_ticks()
        
        self.game_map.update()
        self.player.update(current_time)
        
        self.spawn_enemies(current_time)
        
        firing_enemies = self.enemy_manager.update(current_time)
        for enemy in firing_enemies:
            self.handle_enemy_fire(enemy)
            
        self.bullet_manager.update()
        self.prop_manager.update()
        
        self.check_collisions()
        
        if not self.player.is_active():
            self.game_core.set_game_over()
            self.game_state = 'game_over'
            
    def spawn_enemies(self, current_time):
        if self.enemy_manager.has_boss():
            return
            
        if self.game_core.check_boss_spawn():
            self.enemy_manager.add_boss()
            return
            
        spawn_rate = self.game_core.get_spawn_rate()
        if current_time - self.game_core.last_spawn_time > spawn_rate:
            enemy_type = self.game_core.get_enemy_type()
            x = self.game_core.get_enemy_spawn_x(enemy_type)
            self.enemy_manager.add_enemy(x, -50, enemy_type)
            self.game_core.last_spawn_time = current_time
            
    def handle_enemy_fire(self, enemy):
        if enemy.is_boss():
            self.boss_pattern_timer += 1
            if self.boss_pattern_timer > 60:
                self.boss_pattern = (self.boss_pattern + 1) % 3
                self.boss_pattern_timer = 0
                
            patterns = ['normal', 'fan', 'spread']
            self.bullet_manager.add_boss_bullets(enemy.x, enemy.y, patterns[self.boss_pattern])
        else:
            self.bullet_manager.add_enemy_bullet(enemy.x, enemy.y, enemy.type)
            
    def check_collisions(self):
        player_rect = self.player.get_rect()
        
        for bullet in self.bullet_manager.get_bullets()[:]:
            if bullet.type.startswith('enemy') or bullet.type.startswith('boss'):
                if player_rect.colliderect(bullet.get_rect()):
                    bullet.deactivate()
                    self.player.take_damage(bullet.get_damage())
                    
        for enemy in self.enemy_manager.get_enemies()[:]:
            if player_rect.colliderect(enemy.get_rect()):
                self.player.take_damage(30)
                
        for prop in self.prop_manager.get_props()[:]:
            if player_rect.colliderect(prop.get_rect()):
                self.apply_prop(prop)
                prop.active = False
                
        player_bullets = [b for b in self.bullet_manager.get_bullets() if b.type.startswith('player')]
        for bullet in player_bullets[:]:
            for enemy in self.enemy_manager.get_enemies()[:]:
                if bullet.get_rect().colliderect(enemy.get_rect()):
                    bullet.deactivate()
                    if enemy.take_damage(bullet.get_damage()):
                        self.game_core.add_score(enemy.get_score())
                        self.prop_manager.try_spawn(enemy.x, enemy.y)
                        if enemy.is_boss():
                            self.game_core.boss_defeated = True
                            self.game_state = 'game_over'
                            
    def apply_prop(self, prop):
        prop_type = prop.get_type()
        
        if prop_type == 'power_up':
            self.player.power_up()
        elif prop_type == 'shield':
            self.player.activate_shield(prop.get_config()['duration'])
        elif prop_type == 'health':
            self.player.heal(prop.get_config()['heal_amount'])
        elif prop_type == 'bomb':
            self.player.add_bomb()
            self.game_core.add_bomb()
            
    def draw(self):
        self.game_map.draw(self.screen)
        
        if self.game_state == 'start':
            self.draw_start_screen()
        elif self.game_state == 'playing':
            self.draw_game_screen()
            if self.game_core.is_paused():
                self.draw_pause_screen()
        elif self.game_state == 'game_over':
            self.draw_game_screen()
            self.draw_game_over_screen()
            
        pygame.display.flip()
        
    def draw_start_screen(self):
        title_text = self.font.render('飞机大战', True, (255, 255, 255))
        start_text = self.font.render('按空格键开始', True, (255, 255, 255))
        controls_text = self.font.render('WASD/方向键移动 | 空格射击 | B炸弹 | P暂停', True, (150, 150, 150))
        
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*2//3))
        
        self.screen.blit(title_text, title_rect)
        self.screen.blit(start_text, start_rect)
        self.screen.blit(controls_text, controls_rect)
        
    def draw_game_screen(self):
        if self.player:
            self.player.draw(self.screen)
            
        self.enemy_manager.draw(self.screen)
        self.bullet_manager.draw(self.screen)
        self.prop_manager.draw(self.screen)
        
        self.draw_hud()
        
    def draw_hud(self):
        score_text = self.font.render(f'得分: {self.game_core.score}', True, (255, 255, 255))
        level_text = self.font.render(f'关卡: {self.game_core.level}', True, (255, 255, 255))
        health_text = self.font.render(f'血量: {self.player.get_health()}', True, (255, 255, 255))
        bomb_text = self.font.render(f'炸弹: {self.player.get_bomb_count()}', True, (255, 255, 255))
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 40))
        self.screen.blit(health_text, (SCREEN_WIDTH - 100, 10))
        self.screen.blit(bomb_text, (SCREEN_WIDTH - 100, 40))
        
    def draw_pause_screen(self):
        pause_text = self.font.render('游戏暂停', True, (255, 255, 255))
        resume_text = self.font.render('按P键继续', True, (200, 200, 200))
        
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
        
        self.screen.blit(pause_text, pause_rect)
        self.screen.blit(resume_text, resume_rect)
        
    def draw_game_over_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        if self.game_core.boss_defeated:
            title_text = self.font.render('恭喜通关！', True, (0, 255, 0))
        else:
            title_text = self.font.render('游戏结束', True, (255, 0, 0))
            
        score_text = self.font.render(f'最终得分: {self.game_core.score}', True, (255, 255, 255))
        restart_text = self.font.render('按空格键返回主菜单', True, (200, 200, 200))
        
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*2//3))
        
        self.screen.blit(title_text, title_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
        
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
if __name__ == '__main__':
    game = Game()
    game.run()