import json
import os

class SaveManager:
    def __init__(self):
        self.save_data = {
            "unlocked_levels": 1,
            "completed_levels": [],
            "level_stars": {},
            "high_scores": {},
            "best_times": {},
            "best_steps": {}
        }
        self.load_save()
    
    def load_save(self):
        try:
            if os.path.exists("save.json"):
                with open("save.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.save_data["unlocked_levels"] = data.get("unlocked_levels", 1)
                    self.save_data["completed_levels"] = data.get("completed_levels", [])
                    self.save_data["level_stars"] = data.get("level_stars", {})
                    self.save_data["high_scores"] = data.get("high_scores", {})
                    self.save_data["best_times"] = data.get("best_times", {})
                    self.save_data["best_steps"] = data.get("best_steps", {})
        except:
            pass
    
    def save_game(self):
        try:
            with open("save.json", "w", encoding="utf-8") as f:
                json.dump(self.save_data, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def unlock_level(self, level_index):
        if level_index >= self.save_data["unlocked_levels"]:
            self.save_data["unlocked_levels"] = level_index + 1
            self.save_game()
    
    def is_level_unlocked(self, level_index):
        return level_index < self.save_data["unlocked_levels"]
    
    def get_unlocked_levels(self):
        return self.save_data["unlocked_levels"]
    
    def complete_level(self, level_index):
        if level_index not in self.save_data["completed_levels"]:
            self.save_data["completed_levels"].append(level_index)
            self.save_game()
    
    def is_level_completed(self, level_index):
        return level_index in self.save_data["completed_levels"]
    
    def set_stars(self, level_index, stars):
        current = self.save_data["level_stars"].get(str(level_index), 0)
        if stars > current:
            self.save_data["level_stars"][str(level_index)] = stars
            self.save_game()
    
    def get_stars(self, level_index):
        return self.save_data["level_stars"].get(str(level_index), 0)
    
    def set_high_score(self, level_index, score):
        current = self.save_data["high_scores"].get(str(level_index), 0)
        if score > current:
            self.save_data["high_scores"][str(level_index)] = score
            self.save_game()
    
    def get_high_score(self, level_index):
        return self.save_data["high_scores"].get(str(level_index), 0)
    
    def set_best_time(self, level_index, time):
        current = self.save_data["best_times"].get(str(level_index), float('inf'))
        if time < current:
            self.save_data["best_times"][str(level_index)] = time
            self.save_game()
    
    def get_best_time(self, level_index):
        return self.save_data["best_times"].get(str(level_index), 0)
    
    def set_best_steps(self, level_index, steps):
        current = self.save_data["best_steps"].get(str(level_index), float('inf'))
        if steps < current:
            self.save_data["best_steps"][str(level_index)] = steps
            self.save_game()
    
    def get_best_steps(self, level_index):
        return self.save_data["best_steps"].get(str(level_index), 0)
    
    def clear_save(self):
        self.save_data = {
            "unlocked_levels": 1,
            "completed_levels": [],
            "level_stars": {},
            "high_scores": {},
            "best_times": {},
            "best_steps": {}
        }
        if os.path.exists("save.json"):
            os.remove("save.json")
    
    def get_total_completed(self):
        return len(self.save_data["completed_levels"])