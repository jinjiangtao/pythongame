import pygame
import sys
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE

from modules.game_logic import GameLogic
from modules.game_stats import GameStats
from modules.ui_manager import UIManager
from modules.settings import Settings
from modules.save import SaveManager
from modules.effects import AnimationManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        self.settings = Settings()
        self.save_manager = SaveManager()
        self.game_logic = GameLogic()
        self.game_stats = GameStats()
        self.ui_manager = UIManager()
        self.animation_manager = AnimationManager()
        
        self.game_logic.set_save_manager(self.save_manager)
        self.game_logic.set_settings(self.settings)
        self.animation_manager.set_screen(self.screen)
        
        self.hint_cell = None
        self.current_level = 0
        self.game_won = False
        self.game_failed = False
        self.failure_reason = ""
        
        self._generate_sounds()
        
        self.setup_callbacks()
        self.ui_manager.set_theme(self.settings.get_theme())
        self.game_stats.set_theme(self.settings.get_theme())
        self.ui_manager.show_menu()
        
        if self.settings.music_enabled:
            self._play_music()
    
    def _generate_sounds(self):
        self.sounds = {
            "click": pygame.mixer.Sound(self._generate_click_sound()),
            "toggle": pygame.mixer.Sound(self._generate_toggle_sound()),
            "win": pygame.mixer.Sound(self._generate_win_sound()),
            "fail": pygame.mixer.Sound(self._generate_fail_sound()),
            "hint": pygame.mixer.Sound(self._generate_hint_sound())
        }
        
        for sound in self.sounds.values():
            sound.set_volume(0.3 if self.settings.sound_enabled else 0)
    
    def _generate_click_sound(self):
        import numpy as np
        
        duration = 0.1
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
        
        frequency = 800
        envelope = np.exp(-t * 15)
        wave = np.sin(2 * np.pi * frequency * t) * envelope
        
        samples = (wave * 32767).astype(np.int16)
        sound_array = np.column_stack([samples, samples])
        
        return pygame.mixer.Sound(sound_array)
    
    def _generate_toggle_sound(self):
        import numpy as np
        
        duration = 0.15
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
        
        frequency = 600 + 400 * t
        envelope = np.exp(-t * 10)
        wave = np.sin(2 * np.pi * frequency * t) * envelope
        
        samples = (wave * 32767).astype(np.int16)
        sound_array = np.column_stack([samples, samples])
        
        return pygame.mixer.Sound(sound_array)
    
    def _generate_win_sound(self):
        import numpy as np
        
        duration = 0.8
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
        
        frequencies = [523.25, 659.25, 783.99, 1046.50]
        wave = np.zeros_like(t)
        
        for i, freq in enumerate(frequencies):
            start = i * duration / 4
            mask = (t >= start) & (t < start + duration / 4)
            wave[mask] += np.sin(2 * np.pi * freq * t[mask]) * np.exp(-(t[mask] - start) * 5)
        
        wave = wave / np.max(np.abs(wave)) * 0.5
        envelope = np.exp(-t * 2)
        wave = wave * envelope
        
        samples = (wave * 32767).astype(np.int16)
        sound_array = np.column_stack([samples, samples])
        
        return pygame.mixer.Sound(sound_array)
    
    def _generate_fail_sound(self):
        import numpy as np
        
        duration = 0.5
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
        
        frequency = 300 - 100 * t
        envelope = np.exp(-t * 8)
        wave = np.sin(2 * np.pi * frequency * t) * envelope
        
        samples = (wave * 32767).astype(np.int16)
        sound_array = np.column_stack([samples, samples])
        
        return pygame.mixer.Sound(sound_array)
    
    def _generate_hint_sound(self):
        import numpy as np
        
        duration = 0.3
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
        
        frequency = 400
        envelope = np.exp(-t * 12)
        wave = np.sin(2 * np.pi * frequency * t) * envelope
        
        samples = (wave * 32767).astype(np.int16)
        sound_array = np.column_stack([samples, samples])
        
        return pygame.mixer.Sound(sound_array)
    
    def _play_music(self):
        import numpy as np
        
        sample_rate = 44100
        duration = 10
        t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
        
        notes = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]
        wave = np.zeros_like(t)
        
        note_duration = 0.5
        for i, note in enumerate(notes):
            start = i * note_duration
            mask = (t >= start) & (t < start + note_duration * 0.8)
            wave[mask] += np.sin(2 * np.pi * note * t[mask]) * np.exp(-(t[mask] - start) * 10)
        
        wave = wave / np.max(np.abs(wave)) * 0.1
        envelope = np.concatenate([np.linspace(0, 1, int(sample_rate * 0.5)), 
                                   np.ones(int(sample_rate * (duration - 1))), 
                                   np.linspace(1, 0, int(sample_rate * 0.5))])
        wave = wave * envelope[:len(wave)]
        
        samples = (wave * 32767).astype(np.int16)
        sound_array = np.column_stack([samples, samples])
        
        music_sound = pygame.mixer.Sound(sound_array)
        music_sound.set_volume(0.1)
        music_sound.play(-1)
    
    def setup_callbacks(self):
        callbacks = {
            "start_game": self.start_game,
            "select_level": self.show_level_select,
            "show_rules": self.show_rules,
            "quit": self.quit_game,
            "back_to_menu": self.back_to_menu,
            "restart": self.restart_level,
            "hint": self.use_hint,
            "next_level": self.next_level,
            "show_settings": self.show_settings,
            "show_difficulty": self.show_difficulty_select,
            "show_mode": self.show_mode_select,
            "show_theme": self.show_theme_select,
            "select_difficulty": self.select_difficulty,
            "select_mode": self.select_mode,
            "select_theme": self.select_theme,
            "toggle_sound": self.toggle_sound,
            "toggle_music": self.toggle_music,
            "toggle_animation": self.toggle_animation,
            "clear_save": self.clear_save,
            "continue_game": self.continue_game
        }
        self.ui_manager.set_callbacks(callbacks)
    
    def start_game(self, level_index=0):
        self.current_level = level_index
        self.game_logic.init_board(SCREEN_WIDTH, SCREEN_HEIGHT, level_index)
        self.game_stats.reset()
        self.game_stats.start_timer()
        self.hint_cell = None
        self.game_won = False
        self.game_failed = False
        self.failure_reason = ""
        
        self.ui_manager.show_game_ui(self.settings.get_hint_count())
        self.animation_manager.clear()
    
    def continue_game(self):
        last_level = self.save_manager.get_unlocked_levels() - 1
        if last_level < 0:
            last_level = 0
        self.start_game(last_level)
    
    def show_level_select(self):
        self.ui_manager.show_level_select(self.game_logic)
    
    def show_rules(self):
        self.ui_manager.show_rules()
    
    def show_settings(self):
        self.ui_manager.show_settings()
    
    def show_difficulty_select(self):
        self.ui_manager.show_difficulty_select()
    
    def show_mode_select(self):
        self.ui_manager.show_mode_select()
    
    def show_theme_select(self):
        self.ui_manager.show_theme_select(self.settings.themes)
    
    def select_difficulty(self, difficulty):
        self.settings.set_difficulty(difficulty)
    
    def select_mode(self, mode):
        self.settings.set_mode(mode)
    
    def select_theme(self, theme_name):
        self.settings.set_theme(theme_name)
        theme = self.settings.get_theme()
        self.ui_manager.set_theme(theme)
        self.game_stats.set_theme(theme)
        self.game_logic.set_theme(theme)
    
    def toggle_sound(self, enabled):
        self.settings.toggle_sound()
        for sound in self.sounds.values():
            sound.set_volume(0.3 if enabled else 0)
        self.ui_manager.set_sound_enabled(enabled)
    
    def toggle_music(self, enabled):
        self.settings.toggle_music()
        pygame.mixer.stop()
        if enabled:
            self._play_music()
        self.ui_manager.set_music_enabled(enabled)
    
    def toggle_animation(self, enabled):
        self.settings.toggle_animation()
        self.ui_manager.set_animation_enabled(enabled)
    
    def clear_save(self):
        self.save_manager.clear_save()
        self.game_logic.unlocked_levels = 1
        self.ui_manager.show_menu()
    
    def quit_game(self):
        pygame.quit()
        sys.exit()
    
    def back_to_menu(self):
        self.game_stats.stop_timer()
        self.hint_cell = None
        self.game_won = False
        self.game_failed = False
        self.animation_manager.clear()
        self.ui_manager.show_menu()
    
    def restart_level(self):
        self.start_game(self.current_level)
    
    def use_hint(self):
        hint = self.game_logic.get_hint()
        if hint:
            self.hint_cell = hint
            self.game_stats.use_hint()
            self.ui_manager.update_hint_button(self.game_stats.get_hints_used())
            
            if self.settings.sound_enabled:
                self.sounds["hint"].play()
    
    def next_level(self):
        next_level = self.game_logic.current_level + 1
        if next_level < self.game_logic.get_total_levels():
            self.start_game(next_level)
        else:
            self.back_to_menu()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.ui_manager.get_current_screen() == "game":
                    if self.ui_manager.handle_click(mouse_pos):
                        if self.settings.sound_enabled:
                            self.sounds["click"].play()
                    elif self.game_logic.handle_click(mouse_pos):
                        if self.settings.sound_enabled:
                            self.sounds["toggle"].play()
                        
                        self.game_stats.increment_steps()
                        self.hint_cell = None
                        
                        if self.game_logic.check_win():
                            self._handle_win()
                        else:
                            failed, reason = self.game_logic.check_failure(
                                self.game_stats.get_steps(),
                                self.game_stats.get_time()
                            )
                            if failed:
                                self._handle_failure(reason)
                else:
                    if self.ui_manager.handle_click(mouse_pos):
                        if self.settings.sound_enabled:
                            self.sounds["click"].play()
    
    def _handle_win(self):
        self.game_stats.stop_timer()
        self.game_logic.unlock_next_level()
        
        stars = self.game_logic.calculate_stars(
            self.game_stats.get_steps(),
            self.game_stats.get_time()
        )
        self.game_stats.set_stars(stars)
        self.game_logic.set_level_stars(self.current_level, stars)
        self.game_logic.set_best_time(self.current_level, self.game_stats.get_time())
        self.game_logic.set_best_steps(self.current_level, self.game_stats.get_steps())
        
        self.game_won = True
        
        if self.settings.sound_enabled:
            self.sounds["win"].play()
        
        if self.settings.animation_enabled:
            center_x, center_y = self.game_logic.get_board_center()
            self.animation_manager.create_victory(center_x, center_y)
        
        self.ui_manager.show_win_dialog(stars)
    
    def _handle_failure(self, reason):
        self.game_stats.stop_timer()
        self.game_failed = True
        self.failure_reason = reason
        
        if self.settings.sound_enabled:
            self.sounds["fail"].play()
        
        self.ui_manager.show_failure_dialog(reason)
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.ui_manager.update(mouse_pos)
        
        if self.ui_manager.get_current_screen() == "game":
            self.game_logic.update_hover(mouse_pos)
            self.game_stats.update()
        
        if self.settings.animation_enabled:
            self.animation_manager.update()
    
    def draw(self):
        current_screen = self.ui_manager.get_current_screen()
        
        if current_screen == "game":
            theme = self.settings.get_theme()
            self.screen.fill(theme["bg_color"])
            
            self.game_stats.draw(
                self.screen,
                self.game_logic.get_level_info(self.current_level)["name"],
                self.settings.get_mode(),
                self.settings.get_time_limit(),
                self.settings.get_step_limit()
            )
            
            self.game_logic.draw(self.screen)
            
            if self.hint_cell:
                row, col = self.hint_cell
                cell = self.game_logic.get_hint_cell(row, col)
                if cell:
                    hint_color = (255, 0, 0)
                    pygame.draw.rect(self.screen, hint_color, cell.rect, 4, border_radius=8)
            
            self.ui_manager.draw(self.screen)
            
            if self.settings.animation_enabled:
                self.animation_manager.draw()
        
        elif current_screen == "win_dialog":
            self.screen.fill(self.settings.get_theme()["bg_color"])
            self.game_logic.draw(self.screen)
            self.game_stats.draw_win_screen(
                self.screen,
                self.game_logic.get_level_info(self.current_level)["name"]
            )
            if self.settings.animation_enabled:
                self.animation_manager.draw()
            self.ui_manager.draw(self.screen)
        
        elif current_screen == "failure_dialog":
            self.screen.fill(self.settings.get_theme()["bg_color"])
            self.game_logic.draw(self.screen)
            self.game_stats.draw_failure_screen(
                self.screen,
                self.game_logic.get_level_info(self.current_level)["name"],
                self.failure_reason
            )
            self.ui_manager.draw(self.screen)
        
        else:
            self.ui_manager.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    game = Game()
    game.run()