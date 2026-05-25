import pygame
from model.maze import Maze
from model.player import Player
from model.items import ItemManager, ItemType
from view.game_view import GameView

class GameState:
    PLAYING = 'playing'
    PAUSED = 'paused'
    GAME_OVER = 'game_over'

class GameController:
    def __init__(self, screen):
        self.screen = screen
        self.level = 1
        self.total_steps = 0
        self.state = GameState.PLAYING
        self.maze = Maze(self.level)
        self.player = Player(self.maze)
        self.item_manager = ItemManager(self.maze)
        self.view = GameView(screen)
        self.move_cooldown = 0
        self.max_steps = 500

    def reset_game(self):
        self.level = 1
        self.total_steps = 0
        self.state = GameState.PLAYING
        self.maze = Maze(self.level)
        self.player = Player(self.maze)
        self.item_manager = ItemManager(self.maze)

    def next_level(self):
        self.level += 1
        self.maze = Maze(self.level)
        self.player = Player(self.maze)
        self.item_manager = ItemManager(self.maze)
        self.view.show_message(f"第 {self.level} 关")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if event.key == pygame.K_p:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                        self.view.show_message("游戏暂停")
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                
                if event.key == pygame.K_r:
                    self.reset_game()
                    self.view.show_message("重新开始")

        return True

    def update(self):
        if self.state != GameState.PLAYING:
            return
        
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        
        if current_time > self.move_cooldown:
            dx, dy = 0, 0
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -1
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = 1
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -1
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = 1
            
            if dx != 0 or dy != 0:
                moved = self.player.move(dx, dy)
                if moved:
                    self.total_steps += 1
                    self.check_item_collision()
                    self.check_game_status()
                    self.move_cooldown = current_time + 150

    def check_item_collision(self):
        item = self.item_manager.check_collision(self.player)
        if item:
            if item.type == ItemType.HEALTH:
                self.player.heal()
                self.view.show_message("+1 生命")
            elif item.type == ItemType.TRAP:
                self.player.take_damage()
                self.view.show_message("-1 生命")

    def check_game_status(self):
        if self.player.has_reached_end():
            self.next_level()
            return
        
        if not self.player.is_alive:
            self.state = GameState.GAME_OVER
            self.view.show_message("生命值耗尽")
            return
        
        if self.player.steps >= self.max_steps + self.level * 100:
            self.state = GameState.GAME_OVER
            self.view.show_message("步数超限")

    def render(self):
        if self.state == GameState.GAME_OVER:
            self.view.draw_background()
            self.view.draw_maze(self.maze)
            self.view.draw_items(self.item_manager, self.maze)
            self.view.draw_player(self.player)
            self.view.draw_ui(self.player, self.level)
            self.view.draw_game_over(self.level, self.total_steps)
        elif self.state == GameState.PAUSED:
            self.view.render(self.maze, self.player, self.item_manager, self.level)
            self.view.draw_pause_screen()
        else:
            self.view.render(self.maze, self.player, self.item_manager, self.level)
        
        pygame.display.flip()