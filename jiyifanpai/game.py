import pygame
import random
import config
import card
import ui

class GameState:
    PLAYING = "playing"
    PREVIEW = "preview"
    FLIPPING_BACK = "flipping_back"
    GAME_OVER = "game_over"
    WIN = "win"
    WAITING = "waiting"

class Game:
    def __init__(self):
        self.cards = []
        self.flipped_cards = []
        self.steps = 0
        self.time_left = config.GAME_TIME
        self.state = GameState.PREVIEW
        self.state_timer = config.PREVIEW_TIME
        self.wait_timer = 0
        self.pairs_left = config.TOTAL_PAIRS
        self.ui = ui.UI()
        self.matched_pairs = 0
        
    def initialize_cards(self):
        """初始化并洗牌"""
        self.cards = []
        shape_list = []
        
        pairs_per_shape = config.TOTAL_PAIRS // len(config.SHAPE_TYPES)
        cards_per_shape = pairs_per_shape * 2
        
        for shape_type in config.SHAPE_TYPES:
            for _ in range(cards_per_shape):
                shape_list.append(shape_type)
        
        random.shuffle(shape_list)
        
        for i in range(config.TOTAL_CARDS):
            new_card = card.Card(i, shape_list[i])
            self.cards.append(new_card)
    
    def reset(self):
        """重置游戏"""
        self.cards = []
        self.flipped_cards = []
        self.steps = 0
        self.time_left = config.GAME_TIME
        self.state = GameState.PREVIEW
        self.state_timer = config.PREVIEW_TIME
        self.wait_timer = 0
        self.pairs_left = config.TOTAL_PAIRS
        self.matched_pairs = 0
        self.initialize_cards()
    
    def handle_events(self, event):
        """处理事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_r:
                self.reset()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == GameState.PLAYING:
                self.handle_card_click(event.pos)
        
        return True
    
    def handle_card_click(self, pos):
        """处理卡片点击"""
        if len(self.flipped_cards) >= 2:
            return
        
        for card_obj in self.cards:
            if card_obj.contains_point(pos) and not card_obj.is_flipped and not card_obj.is_matched:
                card_obj.flip()
                self.flipped_cards.append(card_obj)
                self.steps += 1
                
                if len(self.flipped_cards) == 2:
                    self.check_match()
                break
    
    def check_match(self):
        """检查配对"""
        card1, card2 = self.flipped_cards
        
        if card1.shape_type == card2.shape_type:
            card1.match()
            card2.match()
            self.pairs_left -= 1
            self.matched_pairs += 1
            self.flipped_cards = []
            
            if self.pairs_left == 0:
                self.state = GameState.WIN
            else:
                self.state = GameState.WAITING
                self.wait_timer = 200
        else:
            self.state = GameState.FLIPPING_BACK
            self.wait_timer = config.FLIP_DELAY
    
    def update(self, dt):
        """更新游戏状态"""
        for card_obj in self.cards:
            card_obj.update(dt)
        
        if self.state == GameState.PREVIEW:
            self.state_timer -= dt
            if self.state_timer <= 0:
                for card_obj in self.cards:
                    card_obj.is_flipped = False
                self.state = GameState.PLAYING
        
        elif self.state == GameState.FLIPPING_BACK:
            self.wait_timer -= dt
            if self.wait_timer <= 0:
                for card_obj in self.flipped_cards:
                    card_obj.flip()
                self.flipped_cards = []
                self.state = GameState.PLAYING
        
        elif self.state == GameState.WAITING:
            self.wait_timer -= dt
            if self.wait_timer <= 0:
                self.state = GameState.PLAYING
        
        elif self.state == GameState.PLAYING:
            self.time_left -= dt / 1000.0
            if self.time_left <= 0:
                self.time_left = 0
                self.state = GameState.GAME_OVER
    
    def draw(self, surface):
        """绘制游戏画面"""
        surface.fill(config.BG_COLOR)
        
        for card_obj in self.cards:
            card_obj.draw(surface)
        
        self.ui.draw_stats(surface, self.time_left, self.steps, self.pairs_left)
        
        if self.state == GameState.PREVIEW:
            self.ui.draw_preview_message(surface)
        elif self.state == GameState.GAME_OVER:
            self.ui.draw_message(surface, "Game Over!", f"你翻了 {self.steps} 步")
        elif self.state == GameState.WIN:
            self.ui.draw_message(surface, "You Win!", f"总步数: {self.steps}")
        
        self.ui.draw_controls_hint(surface)
    
    def is_input_blocked(self):
        """检查输入是否被阻止"""
        return self.state in [GameState.PREVIEW, GameState.FLIPPING_BACK, GameState.GAME_OVER, GameState.WIN]
