import json
import os

class Settings:
    def __init__(self):
        self.themes = {
            "classic": {
                "name": "经典",
                "bg_color": (30, 30, 40),
                "cell_on": (255, 255, 0),
                "cell_off": (128, 128, 128),
                "cell_hover": (255, 165, 0),
                "cell_border": (0, 0, 0),
                "button_color": (50, 150, 255),
                "button_hover": (70, 170, 255),
                "text_color": (255, 255, 255),
                "stats_bg": (200, 200, 200),
                "stats_text": (0, 0, 0),
                "glow_color": (255, 255, 100)
            },
            "neon": {
                "name": "霓虹",
                "bg_color": (10, 10, 30),
                "cell_on": (0, 255, 255),
                "cell_off": (50, 50, 80),
                "cell_hover": (255, 0, 255),
                "cell_border": (0, 255, 255),
                "button_color": (0, 200, 200),
                "button_hover": (0, 255, 255),
                "text_color": (0, 255, 255),
                "stats_bg": (20, 20, 50),
                "stats_text": (0, 255, 255),
                "glow_color": (0, 255, 255)
            },
            "candy": {
                "name": "糖果",
                "bg_color": (255, 200, 220),
                "cell_on": (255, 100, 150),
                "cell_off": (200, 150, 180),
                "cell_hover": (255, 150, 200),
                "cell_border": (255, 50, 100),
                "button_color": (255, 100, 150),
                "button_hover": (255, 150, 200),
                "text_color": (255, 255, 255),
                "stats_bg": (255, 150, 180),
                "stats_text": (255, 50, 100),
                "glow_color": (255, 150, 200)
            },
            "night": {
                "name": "夜间",
                "bg_color": (5, 5, 10),
                "cell_on": (255, 255, 150),
                "cell_off": (30, 30, 50),
                "cell_hover": (255, 200, 100),
                "cell_border": (60, 60, 80),
                "button_color": (80, 80, 120),
                "button_hover": (100, 100, 140),
                "text_color": (200, 200, 220),
                "stats_bg": (20, 20, 40),
                "stats_text": (200, 200, 220),
                "glow_color": (255, 255, 100)
            }
        }
        
        self.difficulties = {
            "easy": {"name": "简单", "time_limit": 0, "step_limit": 0, "hint_count": 5},
            "normal": {"name": "普通", "time_limit": 120, "step_limit": 30, "hint_count": 3},
            "hard": {"name": "困难", "time_limit": 60, "step_limit": 20, "hint_count": 2},
            "expert": {"name": "专家", "time_limit": 30, "step_limit": 15, "hint_count": 1}
        }
        
        self.game_modes = ["classic", "timed", "limited_steps"]
        
        self.current_theme = "classic"
        self.current_difficulty = "normal"
        self.current_mode = "classic"
        self.sound_enabled = True
        self.music_enabled = True
        self.animation_enabled = True
        
        self.load_settings()
    
    def load_settings(self):
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.current_theme = data.get("theme", "classic")
                    self.current_difficulty = data.get("difficulty", "normal")
                    self.current_mode = data.get("mode", "classic")
                    self.sound_enabled = data.get("sound_enabled", True)
                    self.music_enabled = data.get("music_enabled", True)
                    self.animation_enabled = data.get("animation_enabled", True)
        except:
            pass
    
    def save_settings(self):
        try:
            data = {
                "theme": self.current_theme,
                "difficulty": self.current_difficulty,
                "mode": self.current_mode,
                "sound_enabled": self.sound_enabled,
                "music_enabled": self.music_enabled,
                "animation_enabled": self.animation_enabled
            }
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
        except:
            pass
    
    def set_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.save_settings()
    
    def get_theme(self):
        return self.themes.get(self.current_theme, self.themes["classic"])
    
    def set_difficulty(self, difficulty):
        if difficulty in self.difficulties:
            self.current_difficulty = difficulty
            self.save_settings()
    
    def get_difficulty(self):
        return self.difficulties.get(self.current_difficulty, self.difficulties["normal"])
    
    def set_mode(self, mode):
        if mode in self.game_modes:
            self.current_mode = mode
            self.save_settings()
    
    def get_mode(self):
        return self.current_mode
    
    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.save_settings()
    
    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        self.save_settings()
    
    def toggle_animation(self):
        self.animation_enabled = not self.animation_enabled
        self.save_settings()
    
    def get_theme_names(self):
        return list(self.themes.keys())
    
    def get_difficulty_names(self):
        return list(self.difficulties.keys())
    
    def get_mode_names(self):
        return self.game_modes

    def get_time_limit(self):
        return self.get_difficulty()["time_limit"]
    
    def get_step_limit(self):
        return self.get_difficulty()["step_limit"]
    
    def get_hint_count(self):
        return self.get_difficulty()["hint_count"]