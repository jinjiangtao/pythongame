import pygame
import sys
import math
import random
import numpy as np
from config import *
from game_area import GameArea
from score_timer import ScoreTimer


class Cloud:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(TOP_BAR_HEIGHT + 20, SCREEN_HEIGHT - 50)
        self.size = random.randint(40, 80)
        self.speed = CLOUD_SPEED_BASE + random.random() * 0.5
        self.opacity = random.randint(150, 220)
    
    def update(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH + self.size:
            self.x = -self.size * 2
            self.y = random.randint(TOP_BAR_HEIGHT + 20, SCREEN_HEIGHT - 50)
    
    def draw(self, screen):
        cloud_surface = pygame.Surface((self.size * 4, self.size * 2), pygame.SRCALPHA)
        
        base_color = (255, 255, 255)
        
        pygame.draw.circle(cloud_surface, (*base_color, self.opacity), 
                         (self.size, self.size), self.size // 2)
        pygame.draw.circle(cloud_surface, (*base_color, self.opacity), 
                         (self.size * 2, self.size // 2), self.size // 2)
        pygame.draw.circle(cloud_surface, (*base_color, self.opacity), 
                         (self.size * 2.5, self.size), self.size // 2.5)
        pygame.draw.circle(cloud_surface, (*base_color, self.opacity), 
                         (self.size * 0.8, self.size * 1.2), self.size // 3)
        
        screen.blit(cloud_surface, (self.x - self.size, self.y - self.size // 2))


class SoundManager:
    def __init__(self):
        self.enabled = True
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.enabled = True
        except:
            self.enabled = False
        
        self.sounds = {}
        if self.enabled:
            self.generate_sounds()
    
    def generate_sounds(self):
        sample_rate = 22050
        duration = 0.15
        
        for sound_type in ['catch', 'miss', 'combo', 'levelup', 'prop', 'gameover']:
            n_samples = int(sample_rate * duration)
            samples = np.zeros(n_samples, dtype=np.int16)
            
            if sound_type == 'catch':
                freq = 880
                for i in range(n_samples):
                    t = i / sample_rate
                    envelope = 1.0 - (i / n_samples)
                    freq_mod = freq * (1 + t * 0.5)
                    samples[i] = int(8000 * envelope * math.sin(2 * math.pi * freq_mod * t))
                
                duration2 = 0.1
                n_samples2 = int(sample_rate * duration2)
                samples2 = np.zeros(n_samples2, dtype=np.int16)
                for i in range(n_samples2):
                    t = i / sample_rate
                    envelope = 1.0 - (i / n_samples2)
                    samples2[i] = int(6000 * envelope * math.sin(2 * math.pi * 1320 * t))
                
                samples = np.concatenate([samples, samples2])
            
            elif sound_type == 'miss':
                freq = 200
                for i in range(n_samples):
                    t = i / sample_rate
                    envelope = 1.0 - (i / n_samples)
                    samples[i] = int(5000 * envelope * math.sin(2 * math.pi * freq * t * (1 - t * 2)))
            
            elif sound_type == 'combo':
                freq = 660
                for i in range(n_samples):
                    t = i / sample_rate
                    envelope = 1.0 - (i / n_samples)
                    samples[i] = int(6000 * envelope * math.sin(2 * math.pi * freq * t))
                
                duration2 = 0.12
                n_samples2 = int(sample_rate * duration2)
                samples2 = np.zeros(n_samples2, dtype=np.int16)
                for i in range(n_samples2):
                    t = i / sample_rate
                    envelope = 1.0 - (i / n_samples2)
                    samples2[i] = int(6000 * envelope * math.sin(2 * math.pi * 880 * t))
                
                samples = np.concatenate([samples, samples2])
            
            elif sound_type == 'levelup':
                duration = 0.4
                n_samples = int(sample_rate * duration)
                samples = np.zeros(n_samples, dtype=np.int16)
                for i in range(n_samples):
                    t = i / sample_rate
                    envelope = 1.0 - (i / n_samples)
                    freq = 440 + (i / n_samples) * 440
                    samples[i] = int(7000 * envelope * math.sin(2 * math.pi * freq * t))
            
            elif sound_type == 'prop':
                freq = 1200
                for i in range(n_samples):
                    t = i / sample_rate
                    envelope = 1.0 - (i / n_samples)
                    samples[i] = int(5000 * envelope * math.sin(2 * math.pi * freq * t))
                
                duration2 = 0.1
                n_samples2 = int(sample_rate * duration2)
                samples2 = np.zeros(n_samples2, dtype=np.int16)
                for i in range(n_samples2):
                    t = i / sample_rate
                    envelope = 1.0 - (i / n_samples2)
                    samples2[i] = int(5000 * envelope * math.sin(2 * math.pi * 1500 * t))
                
                samples = np.concatenate([samples, samples2])
            
            elif sound_type == 'gameover':
                duration = 0.6
                n_samples = int(sample_rate * duration)
                samples = np.zeros(n_samples, dtype=np.int16)
                for i in range(n_samples):
                    t = i / sample_rate
                    envelope = 1.0 - (i / n_samples)
                    freq = 440 - (i / n_samples) * 200
                    samples[i] = int(6000 * envelope * math.sin(2 * math.pi * freq * t))
            
            sound_array = np.array(samples, dtype=np.int16)
            sound_array = np.column_stack([sound_array, sound_array])
            self.sounds[sound_type] = pygame.sndarray.make_sound(sound_array)
    
    def play(self, sound_type):
        if self.enabled and sound_type in self.sounds:
            try:
                self.sounds[sound_type].play()
            except:
                pass


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('抓萌宠小游戏')
        
        self.game_area = GameArea()
        self.score_timer = ScoreTimer()
        self.sound_manager = SoundManager()
        
        self.clouds = [Cloud() for _ in range(CLOUD_COUNT)]
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.font_large = self.get_chinese_font(48)
        self.font_medium = self.get_chinese_font(32)
        
        self.click_effect = None
        self.last_level = 1
        
        self.bg_gradient_cache = None
    
    def get_chinese_font(self, size):
        font_paths = [
            'C:/Windows/Fonts/simhei.ttf',
            'C:/Windows/Fonts/msyh.ttc',
            'C:/Windows/Fonts/simsun.ttc',
        ]
        for path in font_paths:
            try:
                return pygame.font.Font(path, size)
            except:
                continue
        return pygame.font.Font(None, size)
    
    def create_gradient_background(self):
        if self.bg_gradient_cache is None:
            surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            
            colors = [
                (135, 206, 235),
                (176, 224, 230),
                (255, 182, 193),
                (255, 218, 185)
            ]
            
            num_stripes = len(colors)
            stripe_height = SCREEN_HEIGHT // (num_stripes - 1)
            
            for i in range(num_stripes - 1):
                start_color = colors[i]
                end_color = colors[i + 1]
                
                for y in range(i * stripe_height, (i + 1) * stripe_height):
                    if y >= SCREEN_HEIGHT:
                        break
                    
                    progress = (y - i * stripe_height) / stripe_height
                    
                    r = int(start_color[0] + (end_color[0] - start_color[0]) * progress)
                    g = int(start_color[1] + (end_color[1] - start_color[1]) * progress)
                    b = int(start_color[2] + (end_color[2] - start_color[2]) * progress)
                    
                    pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
            
            self.bg_gradient_cache = surface
        
        return self.bg_gradient_cache
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.score_timer.game_over:
                    self.reset_game()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.score_timer.game_started:
                    self.score_timer.game_started = True
                    self.score_timer.start_time = pygame.time.get_ticks()
                elif not self.score_timer.game_over:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.process_click(mouse_x, mouse_y)
    
    def process_click(self, mouse_x, mouse_y):
        result = self.game_area.handle_click(mouse_x, mouse_y, self.score_timer)
        
        if result['success']:
            if result['prop_type']:
                self.sound_manager.play('prop')
                self.score_timer.collect_prop(result['prop_type'])
                
                if result['prop_type'] == 'time' and 'time_bonus' in result:
                    self.score_timer.add_time(result['time_bonus'])
                elif result['prop_type'] == 'score':
                    pass
            else:
                points = result['points']
                special_type = result.get('special_type')
                combo_bonus = self.score_timer.add_score(points, special_type)
                
                if combo_bonus > 0:
                    self.sound_manager.play('combo')
                else:
                    self.sound_manager.play('catch')
        
        if self.score_timer.level > self.last_level:
            self.last_level = self.score_timer.level
            self.game_area.set_level(self.score_timer.level)
            self.sound_manager.play('levelup')
    
    def reset_game(self):
        self.score_timer.reset()
        self.game_area.clear_pets()
        self.game_area.set_level(1)
        self.last_level = 1
    
    def update(self):
        if self.score_timer.game_started and not self.score_timer.game_over:
            self.score_timer.update()
            self.game_area.update(pygame.time.get_ticks())
            
            if self.score_timer.level > self.last_level:
                self.last_level = self.score_timer.level
                self.game_area.set_level(self.score_timer.level)
                self.sound_manager.play('levelup')
        
        for cloud in self.clouds:
            cloud.update()
    
    def draw(self):
        background = self.create_gradient_background()
        self.screen.blit(background, (0, 0))
        
        for cloud in self.clouds:
            cloud.draw(self.screen)
        
        if self.score_timer.game_started:
            self.score_timer.draw(self.screen)
            self.game_area.draw(self.screen)
            
            if self.game_area.catch_all_active:
                catch_all_text = self.get_chinese_font(24).render('全屏捕捉模式!', True, ACCEL_PET_COLOR)
                catch_all_rect = catch_all_text.get_rect(center=(SCREEN_WIDTH // 2, TOP_BAR_HEIGHT + 30))
                self.screen.blit(catch_all_text, catch_all_rect)
            
            if self.game_area.score_multiplier > 1:
                multiplier_text = self.get_chinese_font(24).render(f'分数×{self.game_area.score_multiplier}!', True, GOLD_COLOR)
                multiplier_rect = multiplier_text.get_rect(center=(SCREEN_WIDTH // 2, TOP_BAR_HEIGHT + 55))
                self.screen.blit(multiplier_text, multiplier_rect)
            
            if self.score_timer.game_over:
                self.sound_manager.play('gameover')
                self.score_timer.draw_game_over_screen(self.screen)
        else:
            self.score_timer.draw_start_screen(self.screen)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
