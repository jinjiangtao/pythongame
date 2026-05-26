import pygame
import math
import random

class AnimationManager:
    def __init__(self):
        self.animations = []
        self.particles = []
        self.screen = None
    
    def set_screen(self, screen):
        self.screen = screen
    
    def add_animation(self, animation):
        self.animations.append(animation)
    
    def update(self):
        active_animations = []
        for anim in self.animations:
            if anim.update():
                active_animations.append(anim)
        self.animations = active_animations
        
        active_particles = []
        for p in self.particles:
            p.update()
            if p.life > 0:
                active_particles.append(p)
        self.particles = active_particles
    
    def draw(self):
        for anim in self.animations:
            anim.draw(self.screen)
        
        for p in self.particles:
            p.draw(self.screen)
    
    def clear(self):
        self.animations = []
        self.particles = []
    
    def create_cell_click(self, x, y, size, color):
        self.animations.append(CellClickAnimation(x, y, size, color))
    
    def create_cell_glow(self, x, y, size, color):
        self.animations.append(CellGlowAnimation(x, y, size, color))
    
    def create_victory(self, center_x, center_y):
        self.animations.append(VictoryAnimation(center_x, center_y))
        for _ in range(50):
            self.particles.append(VictoryParticle(center_x, center_y))
    
    def create_failure(self, center_x, center_y):
        self.animations.append(FailureAnimation(center_x, center_y))
    
    def create_transition(self, type="fade"):
        self.animations.append(ScreenTransition(type))

class CellClickAnimation:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.progress = 0
        self.duration = 150
        self.start_time = pygame.time.get_ticks()
    
    def update(self):
        current_time = pygame.time.get_ticks()
        self.progress = (current_time - self.start_time) / self.duration
        return self.progress < 1
    
    def draw(self, screen):
        if self.progress >= 1:
            return
        
        alpha = int(255 * (1 - self.progress))
        scale = 1 + self.progress * 0.5
        current_size = self.size * scale
        x = self.x + self.size // 2 - current_size // 2
        y = self.y + self.size // 2 - current_size // 2
        
        surface = pygame.Surface((current_size, current_size), pygame.SRCALPHA)
        pygame.draw.rect(surface, (self.color[0], self.color[1], self.color[2], alpha), 
                        (0, 0, current_size, current_size), border_radius=8)
        screen.blit(surface, (x, y))

class CellGlowAnimation:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.phase = 0
        self.is_active = True
    
    def update(self):
        self.phase += 0.15
        return self.is_active
    
    def set_inactive(self):
        self.is_active = False
    
    def draw(self, screen):
        glow_size = self.size + math.sin(self.phase) * 8
        x = self.x + self.size // 2 - glow_size // 2
        y = self.y + self.size // 2 - glow_size // 2
        
        surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        alpha = int(50 + math.sin(self.phase) * 30)
        pygame.draw.rect(surface, (self.color[0], self.color[1], self.color[2], alpha),
                        (0, 0, glow_size, glow_size), border_radius=8)
        screen.blit(surface, (x, y))

class VictoryAnimation:
    def __init__(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
        self.progress = 0
        self.duration = 2000
        self.start_time = pygame.time.get_ticks()
        self.rings = []
        
        for i in range(3):
            self.rings.append({"radius": 50 + i * 30, "progress": 0, "delay": i * 200})
    
    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        
        for ring in self.rings:
            if elapsed > ring["delay"]:
                ring["progress"] = min(1, (elapsed - ring["delay"]) / 500)
        
        self.progress = elapsed / self.duration
        return self.progress < 1
    
    def draw(self, screen):
        for ring in self.rings:
            progress = ring["progress"]
            if progress <= 0:
                continue
            
            radius = ring["radius"] * progress
            alpha = int(255 * (1 - progress))
            
            surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 255, 0, alpha), (radius, radius), radius, 3)
            screen.blit(surface, (self.center_x - radius, self.center_y - radius))

class FailureAnimation:
    def __init__(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
        self.progress = 0
        self.duration = 1500
        self.start_time = pygame.time.get_ticks()
        self.shake_offset = 0
    
    def update(self):
        current_time = pygame.time.get_ticks()
        self.progress = (current_time - self.start_time) / self.duration
        
        if self.progress < 0.3:
            self.shake_offset = math.sin(self.progress * 50) * 10
        else:
            self.shake_offset = 0
        
        return self.progress < 1
    
    def draw(self, screen):
        pass
    
    def get_shake_offset(self):
        return self.shake_offset

class ScreenTransition:
    def __init__(self, type="fade"):
        self.type = type
        self.progress = 0
        self.duration = 500
        self.start_time = pygame.time.get_ticks()
        self.direction = "in"
    
    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        
        if elapsed >= self.duration:
            if self.direction == "in":
                self.direction = "out"
                self.start_time = current_time
                elapsed = 0
        
        self.progress = elapsed / self.duration
        return self.direction == "out" or self.progress < 1
    
    def draw(self, screen):
        alpha = int(255 * self.progress) if self.direction == "in" else int(255 * (1 - self.progress))
        surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        surface.fill((0, 0, 0, alpha))
        screen.blit(surface, (0, 0))

class VictoryParticle:
    def __init__(self, center_x, center_y):
        self.x = center_x
        self.y = center_y
        self.vx = (random.random() - 0.5) * 8
        self.vy = (random.random() - 0.5) * 8 - 2
        self.life = 1
        self.decay = 0.02 + random.random() * 0.02
        self.size = 4 + random.random() * 4
        self.color = (255, 200 + random.randint(0, 55), 0)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.life -= self.decay
    
    def draw(self, screen):
        if self.life <= 0:
            return
        
        alpha = int(255 * self.life)
        surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (self.color[0], self.color[1], self.color[2], alpha),
                         (self.size, self.size), self.size)
        screen.blit(surface, (self.x - self.size, self.y - self.size))

class GradientEffect:
    @staticmethod
    def lerp_color(color1, color2, t):
        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)
        return (r, g, b)
    
    @staticmethod
    def draw_gradient_rect(screen, rect, color1, color2, vertical=True):
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        width, height = rect.size
        
        for i in range(height if vertical else width):
            t = i / (height if vertical else width)
            color = GradientEffect.lerp_color(color1, color2, t)
            
            if vertical:
                pygame.draw.line(surface, color, (0, i), (width, i))
            else:
                pygame.draw.line(surface, color, (i, 0), (i, height))
        
        screen.blit(surface, rect.topleft)

class TextAnimation:
    def __init__(self, text, font, color, x, y, duration=1000):
        self.text = text
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
        self.progress = 0
    
    def update(self):
        current_time = pygame.time.get_ticks()
        self.progress = min(1, (current_time - self.start_time) / self.duration)
        return self.progress < 1
    
    def draw(self, screen):
        alpha = int(255 * self.progress)
        scale = 0.5 + self.progress * 0.5
        offset_y = -30 * (1 - self.progress)
        
        text_surface = self.font.render(self.text, True, self.color)
        text_surface.set_alpha(alpha)
        
        scaled_surface = pygame.transform.scale(text_surface, 
            (int(text_surface.get_width() * scale), int(text_surface.get_height() * scale)))
        
        rect = scaled_surface.get_rect(center=(self.x, self.y + offset_y))
        screen.blit(scaled_surface, rect)