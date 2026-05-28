import json
import os
from datetime import datetime
from typing import List, Dict, Any

class Statistics:
    def __init__(self):
        self.total_questions = 0
        self.correct_answers = 0
        self.wrong_attempts = 0
        self.total_time = 0
        self.wrong_questions = []
        
        self.by_type = {
            "counting": {"total": 0, "correct": 0},
            "addition": {"total": 0, "correct": 0},
            "subtraction": {"total": 0, "correct": 0},
            "multiplication": {"total": 0, "correct": 0},
            "division": {"total": 0, "correct": 0},
            "compare": {"total": 0, "correct": 0},
            "mixed": {"total": 0, "correct": 0},
        }
        
        self.by_level = {}
        
        self.load_data()
    
    @property
    def accuracy(self):
        if self.total_questions == 0:
            return 0
        return round((self.correct_answers / self.total_questions) * 100, 1)
    
    @property
    def avg_time(self):
        if self.total_questions == 0:
            return 0
        return round(self.total_time / self.total_questions, 1)
    
    def record_correct(self, question_type: str, level: int, time_spent: float = 0):
        self.total_questions += 1
        self.correct_answers += 1
        self.total_time += time_spent
        
        if question_type in self.by_type:
            self.by_type[question_type]["total"] += 1
            self.by_type[question_type]["correct"] += 1
        
        if level not in self.by_level:
            self.by_level[level] = {"total": 0, "correct": 0}
        self.by_level[level]["total"] += 1
        self.by_level[level]["correct"] += 1
    
    def record_wrong(self, question: Any, time_spent: float = 0):
        self.wrong_attempts += 1
        self.total_time += time_spent
        
        question_type = question.question_type
        if question_type in self.by_type:
            self.by_type[question_type]["total"] += 1
        
        level = question.difficulty if hasattr(question, 'difficulty') else 1
        if level not in self.by_level:
            self.by_level[level] = {"total": 0, "correct": 0}
        self.by_level[level]["total"] += 1
        
        wrong_record = {
            "qid": question.qid,
            "type": question_type,
            "content": question.content,
            "options": question.options,
            "correct_answer": question.correct_answer,
            "user_answer": question.user_answer,
            "hint": question.hint,
            "timestamp": datetime.now().isoformat(),
            "time_spent": time_spent,
        }
        self.wrong_questions.append(wrong_record)
    
    def reset(self):
        self.total_questions = 0
        self.correct_answers = 0
        self.wrong_attempts = 0
        self.total_time = 0
        self.wrong_questions.clear()
        
        for key in self.by_type:
            self.by_type[key] = {"total": 0, "correct": 0}
        
        self.by_level.clear()
        
        self.save_data()
    
    def get_summary(self):
        return {
            "total": self.total_questions,
            "correct": self.correct_answers,
            "wrong_attempts": self.wrong_attempts,
            "accuracy": self.accuracy,
            "avg_time": self.avg_time,
        }
    
    def get_type_stats(self):
        result = {}
        for qtype, stats in self.by_type.items():
            if stats["total"] > 0:
                accuracy = round((stats["correct"] / stats["total"]) * 100, 1)
            else:
                accuracy = 0
            result[qtype] = {
                "total": stats["total"],
                "correct": stats["correct"],
                "accuracy": accuracy,
            }
        return result
    
    def get_level_stats(self):
        result = {}
        for level, stats in self.by_level.items():
            if stats["total"] > 0:
                accuracy = round((stats["correct"] / stats["total"]) * 100, 1)
            else:
                accuracy = 0
            result[level] = {
                "total": stats["total"],
                "correct": stats["correct"],
                "accuracy": accuracy,
            }
        return result
    
    def save_data(self):
        data = {
            "total_questions": self.total_questions,
            "correct_answers": self.correct_answers,
            "wrong_attempts": self.wrong_attempts,
            "total_time": self.total_time,
            "by_type": self.by_type,
            "by_level": self.by_level,
            "saved_at": datetime.now().isoformat(),
        }
        
        try:
            os.makedirs("data", exist_ok=True)
            with open("data/statistics.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存统计数据失败: {e}")
    
    def load_data(self):
        try:
            with open("data/statistics.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                
                self.total_questions = data.get("total_questions", 0)
                self.correct_answers = data.get("correct_answers", 0)
                self.wrong_attempts = data.get("wrong_attempts", 0)
                self.total_time = data.get("total_time", 0)
                
                if "by_type" in data:
                    for key in self.by_type:
                        if key in data["by_type"]:
                            self.by_type[key] = data["by_type"][key]
                
                if "by_level" in data:
                    self.by_level = data["by_level"]
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"加载统计数据失败: {e}")
    
    def save_wrong_questions(self):
        try:
            os.makedirs("data", exist_ok=True)
            with open("data/wrong_questions.json", "w", encoding="utf-8") as f:
                json.dump(self.wrong_questions, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存错题数据失败: {e}")
    
    def load_wrong_questions(self):
        try:
            with open("data/wrong_questions.json", "r", encoding="utf-8") as f:
                self.wrong_questions = json.load(f)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"加载错题数据失败: {e}")