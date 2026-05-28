import json
import os

PROGRESS_FILE = "progress.json"

class ProgressManager:
    def __init__(self):
        self.progress = {
            "completed_levels": [],
            "correct_answers": {},
            "total_answers": {},
            "current_level": 1
        }
        self.load_progress()

    def load_progress(self):
        if os.path.exists(PROGRESS_FILE):
            try:
                with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    self.progress.update(saved)
            except:
                pass

    def save_progress(self):
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.progress, f, ensure_ascii=False)

    def complete_level(self, level_id):
        if level_id not in self.progress["completed_levels"]:
            self.progress["completed_levels"].append(level_id)
        self.save_progress()

    def record_answer(self, level_id, is_correct):
        if level_id not in self.progress["correct_answers"]:
            self.progress["correct_answers"][level_id] = 0
            self.progress["total_answers"][level_id] = 0
        
        self.progress["total_answers"][level_id] += 1
        if is_correct:
            self.progress["correct_answers"][level_id] += 1
        self.save_progress()

    def get_accuracy(self, level_id):
        total = self.progress["total_answers"].get(level_id, 0)
        correct = self.progress["correct_answers"].get(level_id, 0)
        if total == 0:
            return 0
        return round((correct / total) * 100)

    def set_current_level(self, level_id):
        self.progress["current_level"] = level_id
        self.save_progress()

    def get_current_level(self):
        return self.progress["current_level"]

    def get_completed_count(self):
        return len(self.progress["completed_levels"])

    def reset_progress(self):
        self.progress = {
            "completed_levels": [],
            "correct_answers": {},
            "total_answers": {},
            "current_level": 1
        }
        self.save_progress()