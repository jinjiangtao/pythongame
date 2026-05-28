import random
import customtkinter as ctk
from models.question_generator import QuestionGenerator, Question
from models.level_manager import LevelManager
from models.statistics import Statistics
from views.main_window import MainWindow
from config import Config

class GameController:
    def __init__(self, master):
        self.master = master
        self.view = MainWindow(master)
        self.question_generator = QuestionGenerator()
        self.level_manager = LevelManager()
        self.statistics = Statistics()
        
        self.current_question = None
        self.current_answer = None
        self.is_answered = False
        self.is_dark_theme = False
        self.time_left = 0
        self.timer = None
        self.score = 0
        
        self._bind_events()
        self._start_new_game()
    
    def _bind_events(self):
        self.view.bind_number_click(self._on_number_click)
        self.view.bind_submit(self._on_submit)
        self.view.bind_next(self._on_next)
        self.view.bind_restart(self._on_restart)
        self.view.bind_theme_switch(self._on_theme_switch)
    
    def _start_new_game(self):
        self.level_manager.reset()
        self.statistics.reset()
        self.score = 0
        self._update_header()
        self._generate_new_question()
    
    def _update_header(self):
        current_q, total_q = self.level_manager.get_progress()
        question_type_name = Config.QUESTION_TYPES.get(
            self.current_question.question_type if self.current_question else "counting",
            {"name": "数数"}
        )["name"]
        
        self.view.set_header_info(
            self.level_manager.current_level,
            self.level_manager.level_name,
            self.level_manager.grade,
            question_type_name,
            self.score,
            self.statistics.accuracy,
            current_q,
            total_q
        )
    
    def _generate_new_question(self):
        self.current_question = self.question_generator.generate_question(
            self.level_manager.current_level
        )
        self.current_answer = self.current_question.correct_answer
        
        self.view.clear_selection()
        self.view.set_options(self.current_question.options)
        
        if self.current_question.question_type == "counting":
            pattern = self.current_question.content.split()[0]
            count = self.current_question.correct_answer
            
            self.master.update_idletasks()
            self.view.game_panel.update_idletasks()
            panel_width = self.view.game_panel.winfo_width()
            panel_height = self.view.game_panel.winfo_height()
            
            if panel_width < 100 or panel_height < 100:
                panel_width, panel_height = 760, 250
            
            positions = self.question_generator.generate_positions(
                count, panel_width, panel_height, 50
            )
            self.view.display_patterns(pattern, positions)
            self.view.set_status_text("数一数有几个图案？")
        else:
            self.view.display_question(self.current_question.content)
            self.view.set_status_text("请选择正确的答案")
        
        self.view.set_hint(self.current_question.hint)
        self.view.set_feedback("", False)
        self.view.enable_next(False)
        
        self.time_left = self.level_manager.time_limit
        self._start_timer()
        
        self.is_answered = False
    
    def _start_timer(self):
        if self.timer:
            self.master.after_cancel(self.timer)
        
        self.view.set_time(self.time_left)
        
        def countdown():
            if self.time_left > 0 and not self.is_answered:
                self.time_left -= 1
                self.view.set_time(self.time_left)
                
                if self.time_left <= 10:
                    self.view.set_status_text(f"⏰ 时间不多了，还有{self.time_left}秒！", False)
                
                self.timer = self.master.after(1000, countdown)
            elif self.time_left == 0 and not self.is_answered:
                self._handle_timeout()
        
        self.timer = self.master.after(1000, countdown)
    
    def _handle_timeout(self):
        if not self.is_answered:
            self.is_answered = True
            self.view.enable_submit(False)
            
            self.statistics.record_wrong(self.current_question, self.level_manager.time_limit)
            
            feedback = "⏰ 时间到！"
            self.view.set_feedback(feedback, False)
            self.view.set_status_text(f"正确答案是 {self.current_answer}", False)
            self.view.set_hint(self.current_question.hint)
            
            self.level_manager.next_question()
            self._update_header()
            self.view.enable_next(True)
    
    def _on_number_click(self, number: int):
        if self.is_answered:
            self.view.clear_selection()
            self.is_answered = False
            self.view.set_feedback("", False)
    
    def _on_submit(self, answer: int):
        if self.is_answered:
            return
        
        self.is_answered = True
        self.view.enable_submit(False)
        
        if self.timer:
            self.master.after_cancel(self.timer)
        
        time_spent = self.level_manager.time_limit - self.time_left
        
        if answer == self.current_answer:
            self._handle_correct_answer(time_spent)
        else:
            self._handle_wrong_answer(answer, time_spent)
    
    def _handle_correct_answer(self, time_spent: float):
        self.statistics.record_correct(
            self.current_question.question_type,
            self.level_manager.current_level,
            time_spent
        )
        
        base_score = 100
        time_bonus = max(0, int((self.level_manager.time_limit - time_spent) * 2))
        self.score += base_score + time_bonus
        
        feedback = random.choice(Config.ENCOURAGEMENTS)
        self.view.set_feedback(feedback, True)
        self.view.set_status_text("回答正确！点击下一题继续挑战", True)
        
        self.level_manager.next_question()
        self._update_header()
        self.view.enable_next(True)
        
        if self.level_manager.check_level_up(self.statistics.correct_answers):
            self._show_level_up_message()
    
    def _handle_wrong_answer(self, answer: int, time_spent: float):
        self.current_question.user_answer = answer
        self.statistics.record_wrong(self.current_question, time_spent)
        
        feedback = random.choice(Config.HINTS)
        self.view.set_feedback(feedback, False)
        self.view.set_status_text("答案不对，请重新选择", False)
        
        self.view.clear_selection()
        self.is_answered = False
        self.time_left = self.level_manager.time_limit
        self._start_timer()
    
    def _show_level_up_message(self):
        level_name = self.level_manager.level_name
        badge = Config.BADGES.get(self.level_manager.current_level)
        
        if badge:
            message = f"{badge['icon']} 恭喜晋级！\n现在是 {level_name}！\n获得徽章：{badge['name']}"
        else:
            message = f"🎊 恭喜晋级！\n现在是 {level_name}！"
        
        popup = ctk.CTkToplevel(self.master)
        popup.title("恭喜升级！")
        popup.geometry("350x200")
        popup.resizable(False, False)
        popup.grab_set()
        
        label = ctk.CTkLabel(
            popup,
            text=message,
            font=("Microsoft YaHei", 18, "bold"),
            text_color="#FF6B6B",
            justify="center"
        )
        label.pack(pady=30)
        
        ok_btn = ctk.CTkButton(
            popup,
            text="确定",
            font=("Microsoft YaHei", 16, "bold"),
            command=popup.destroy
        )
        ok_btn.pack(pady=10)
    
    def _on_next(self):
        self._generate_new_question()
    
    def _on_restart(self):
        confirm = ctk.CTkToplevel(self.master)
        confirm.title("确认重新开始")
        confirm.geometry("300x150")
        confirm.resizable(False, False)
        confirm.grab_set()
        
        label = ctk.CTkLabel(
            confirm,
            text="确定要重新开始游戏吗？",
            font=("Microsoft YaHei", 14)
        )
        label.pack(pady=20)
        
        btn_frame = ctk.CTkFrame(confirm)
        btn_frame.pack(pady=10)
        
        yes_btn = ctk.CTkButton(
            btn_frame,
            text="确定",
            font=("Microsoft YaHei", 14),
            fg_color="#FF6B6B",
            hover_color="#E55555",
            command=lambda: [confirm.destroy(), self._start_new_game()]
        )
        yes_btn.pack(side="left", padx=10)
        
        no_btn = ctk.CTkButton(
            btn_frame,
            text="取消",
            font=("Microsoft YaHei", 14),
            command=confirm.destroy
        )
        no_btn.pack(side="right", padx=10)
    
    def _on_theme_switch(self):
        self.is_dark_theme = not self.is_dark_theme
        mode = "dark" if self.is_dark_theme else "light"
        ctk.set_appearance_mode(mode)