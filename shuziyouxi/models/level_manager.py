from config import Config

class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.current_question = 0
        self.unlocked_levels = {1}
        self.questions_per_level = Config.GAME_CONFIG["questions_per_level"]
        self.pass_rate = Config.GAME_CONFIG["pass_rate"]
    
    @property
    def current_config(self):
        return Config.DIFFICULTY_LEVELS.get(self.current_level, Config.DIFFICULTY_LEVELS[1])
    
    @property
    def level_name(self):
        return self.current_config["name"]
    
    @property
    def grade(self):
        return self.current_config["grade"]
    
    @property
    def description(self):
        return self.current_config["description"]
    
    @property
    def time_limit(self):
        return Config.TIME_LIMITS.get(self.current_level, 60)
    
    def next_question(self):
        self.current_question += 1
    
    def check_level_up(self, correct_count: int) -> bool:
        if self.current_question >= self.questions_per_level:
            accuracy = correct_count / self.questions_per_level
            if accuracy >= self.pass_rate:
                self.unlock_next_level()
                self.level_up()
                return True
            return False
        return False
    
    def level_up(self):
        if self.current_level < max(Config.DIFFICULTY_LEVELS.keys()):
            self.current_level += 1
        self.current_question = 0
    
    def unlock_next_level(self):
        next_level = self.current_level + 1
        if next_level <= max(Config.DIFFICULTY_LEVELS.keys()):
            self.unlocked_levels.add(next_level)
    
    def select_level(self, level: int):
        if level in self.unlocked_levels:
            self.current_level = level
            self.current_question = 0
    
    def reset(self):
        self.current_level = 1
        self.current_question = 0
    
    def get_progress(self):
        return (self.current_question, self.questions_per_level)
    
    def get_level_progress(self):
        return (self.current_level, max(Config.DIFFICULTY_LEVELS.keys()))