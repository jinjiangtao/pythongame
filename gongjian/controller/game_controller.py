import pygame
import random
import math
from model.game_objects import Archer, Arrow, Target, FlyingTarget, PowerUp, GameState

class GameController:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.archer = Archer(screen_width // 2, screen_height - 120)
        self.arrows = []
        self.targets = []
        self.flying_targets = []
        self.power_ups = []
        self.game_state = GameState()
        self.clock = pygame.time.Clock()
        self.last_target_spawn = pygame.time.get_ticks()
        self.last_flying_spawn = pygame.time.get_ticks()
        self.last_power_up_spawn = pygame.time.get_ticks()
        self.target_spawn_interval = 2000
        self.flying_spawn_interval = 4000
        self.power_up_spawn_interval = 8000

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_p:
                    self.game_state.paused = not self.game_state.paused
                if event.key == pygame.K_r and self.game_state.game_over:
                    self.reset_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.game_state.paused and not self.game_state.game_over:
                    self.archer.start_charging()
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.archer.is_charging:
                    self.shoot_arrow()
        
        keys = pygame.key.get_pressed()
        if not self.game_state.paused and not self.game_state.game_over:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.archer.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.archer.move_right()
        
        return True

    def shoot_arrow(self):
        power = self.archer.stop_charging()
        if power > 0 and self.game_state.arrows > 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.archer.x
            dy = mouse_y - self.archer.y
            angle = math.degrees(math.atan2(dy, dx))
            
            new_arrow = Arrow(self.archer.x + 20, self.archer.y - 20, angle, power)
            self.arrows.append(new_arrow)
            self.game_state.remove_arrow()
            self.game_state.set_message(f"发射! 力度: {power}%")

    def spawn_targets(self):
        current_time = pygame.time.get_ticks()
        
        level_multiplier = 1 - (self.game_state.level - 1) * 0.1
        level_multiplier = max(0.5, level_multiplier)
        
        if current_time - self.last_target_spawn > self.target_spawn_interval * level_multiplier:
            self.targets.append(Target(self.screen_width, self.screen_height))
            self.last_target_spawn = current_time
        
        if current_time - self.last_flying_spawn > self.flying_spawn_interval * level_multiplier:
            if random.random() < 0.5:
                self.flying_targets.append(FlyingTarget(self.screen_width, self.screen_height))
            self.last_flying_spawn = current_time
        
        if current_time - self.last_power_up_spawn > self.power_up_spawn_interval:
            if random.random() < 0.3:
                self.power_ups.append(PowerUp(self.screen_width, self.screen_height))
            self.last_power_up_spawn = current_time

    def update_objects(self):
        if self.archer.is_charging:
            self.archer.charge()
        
        for arrow in self.arrows[:]:
            arrow.update()
            if not arrow.active:
                self.arrows.remove(arrow)
        
        for target in self.targets[:]:
            target.update()
            if not target.active:
                self.targets.remove(target)
                self.game_state.remove_life()
                self.game_state.set_message("脱靶! 生命值-1")
        
        for target in self.flying_targets[:]:
            target.update()
            if not target.active:
                self.flying_targets.remove(target)
        
        for power_up in self.power_ups[:]:
            power_up.update()
            if not power_up.active:
                self.power_ups.remove(power_up)

    def check_collisions(self):
        for arrow in self.arrows[:]:
            arrow_rect = pygame.Rect(
                arrow.x - arrow.width // 2,
                arrow.y - arrow.height // 2,
                arrow.width,
                arrow.height
            )
            
            for target in self.targets[:]:
                target_rect = pygame.Rect(
                    target.x - target.width // 2,
                    target.y - target.height // 2,
                    target.width,
                    target.height
                )
                
                if arrow_rect.colliderect(target_rect):
                    score = target.get_score()
                    self.game_state.add_score(score)
                    self.targets.remove(target)
                    self.arrows.remove(arrow)
                    self.game_state.set_message(f"命中! +{score}分")
                    self.check_level_up()
                    break
            
            for target in self.flying_targets[:]:
                target_rect = pygame.Rect(
                    target.x - target.width // 2,
                    target.y - target.height // 2,
                    target.width,
                    target.height
                )
                
                if arrow_rect.colliderect(target_rect):
                    score = target.get_score()
                    self.game_state.add_score(score)
                    self.flying_targets.remove(target)
                    self.arrows.remove(arrow)
                    self.game_state.set_message(f"命中飞鸟! +{score}分")
                    self.check_level_up()
                    break
            
            for power_up in self.power_ups[:]:
                power_up_rect = pygame.Rect(
                    power_up.x - power_up.width // 2,
                    power_up.y - power_up.height // 2,
                    power_up.width,
                    power_up.height
                )
                
                if arrow_rect.colliderect(power_up_rect):
                    self.arrows.remove(arrow)
                    self.power_ups.remove(power_up)
                    
                    if power_up.type == 'arrow':
                        self.game_state.add_arrow()
                        self.game_state.set_message("获得箭矢+2!")
                    elif power_up.type == 'score':
                        self.game_state.add_score(50)
                        self.game_state.set_message("额外+50分!")
                    elif power_up.type == 'health':
                        self.game_state.add_life()
                        self.game_state.set_message("获得生命+1!")
                    break

    def check_level_up(self):
        if self.game_state.score >= self.game_state.level * 100:
            self.game_state.update_level()
            self.game_state.set_message(f"升级! 第{self.game_state.level}关")

    def reset_game(self):
        self.game_state.reset()
        self.archer = Archer(self.screen_width // 2, self.screen_height - 120)
        self.arrows = []
        self.targets = []
        self.flying_targets = []
        self.power_ups = []
        self.last_target_spawn = pygame.time.get_ticks()
        self.last_flying_spawn = pygame.time.get_ticks()
        self.last_power_up_spawn = pygame.time.get_ticks()

    def run(self, view):
        running = True
        while running:
            running = self.handle_events()
            
            if not self.game_state.paused and not self.game_state.game_over:
                self.spawn_targets()
                self.update_objects()
                self.check_collisions()
            
            view.draw_background()
            
            for power_up in self.power_ups:
                view.draw_power_up(power_up)
            
            for target in self.targets:
                view.draw_target(target)
            
            for target in self.flying_targets:
                view.draw_flying_target(target)
            
            for arrow in self.arrows:
                view.draw_arrow(arrow)
            
            view.draw_archer(self.archer)
            view.draw_power_bar(self.archer)
            view.draw_ui(self.game_state)
            view.draw_message(self.game_state)
            view.draw_instructions()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()