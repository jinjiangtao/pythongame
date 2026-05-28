import customtkinter as ctk
from models.question_generator import QuestionGenerator
from models.level_manager import LevelManager
from models.statistics import Statistics
from views.main_window import MainWindow

class GameController:
    """游戏控制器 - 协调视图与模型，管理游戏流程"""
    
    def __init__(self, master):
        self.master = master
        self.view = MainWindow(master)
        self.question_generator = QuestionGenerator()
        self.level_manager = LevelManager()
        self.statistics = Statistics()
        
        self.current_answer = None
        self.current_pattern = None
        self.is_answered = False
        self.is_dark_theme = False
        
        self._bind_events()
        self._start_new_game()
    
    def _bind_events(self):
        """绑定所有事件回调"""
        self.view.bind_number_click(self._on_number_click)
        self.view.bind_submit(self._on_submit)
        self.view.bind_next(self._on_next)
        self.view.bind_restart(self._on_restart)
        self.view.bind_theme_switch(self._on_theme_switch)
    
    def _start_new_game(self):
        """开始新游戏"""
        self.level_manager.reset()
        self.statistics.reset()
        self.question_generator.reset()
        self._update_header()
        self._generate_new_question()
    
    def _update_header(self):
        """更新头部信息"""
        current, total = self.level_manager.get_progress()
        progress = f"{current}/{total}"
        self.view.set_header_info(
            self.level_manager.current_level,
            self.level_manager.level_name,
            progress,
            self.statistics.accuracy
        )
    
    def _generate_new_question(self):
        """生成新题目"""
        min_count = self.level_manager.min_count
        max_count = self.level_manager.max_count
        
        self.current_answer, self.current_pattern = self.question_generator.generate_question(
            min_count, max_count
        )
        
        self.view.set_number_buttons_range(min_count, max_count)
        self.view.clear_selection()
        self.view.clear_panel()
        self.view.enable_next(False)
        
        self.master.update_idletasks()
        self.view.game_panel.update_idletasks()
        panel_width = self.view.game_panel.winfo_width()
        panel_height = self.view.game_panel.winfo_height()
        
        if panel_width < 100 or panel_height < 100:
            panel_width, panel_height = 560, 280
        
        positions = self.question_generator.generate_positions(
            self.current_answer, panel_width, panel_height, 50
        )
        
        self.view.display_patterns(self.current_pattern, positions)
        self.view.set_status_text("数一数有几个图案？")
        self.view.set_feedback("", False)
        
        self.is_answered = False
    
    def _on_number_click(self, number: int):
        """数字按钮点击处理"""
        if self.is_answered:
            self.view.clear_selection()
            self.is_answered = False
            self.view.set_feedback("", False)
    
    def _on_submit(self, answer: int):
        """提交答案处理"""
        if self.is_answered:
            return
        
        self.is_answered = True
        self.view.enable_submit(False)
        
        if answer == self.current_answer:
            self._handle_correct_answer()
        else:
            self._handle_wrong_answer()
    
    def _handle_correct_answer(self):
        """处理正确答案"""
        self.statistics.record_correct()
        self.level_manager.next_question()
        
        feedback_messages = [
            "🎉 太棒了！回答正确！",
            "👏 真聪明！答对了！",
            "🌟 完美！你真厉害！",
            "💯 正确！继续加油！",
            "🎊 答对啦！你真棒！"
        ]
        
        import random
        feedback = random.choice(feedback_messages)
        self.view.set_feedback(feedback, True)
        self.view.set_status_text("回答正确！点击下一题继续挑战", True)
        
        self._update_header()
        self.view.enable_next(True)
        
        if self.level_manager.check_level_up():
            self._show_level_up_message()
    
    def _handle_wrong_answer(self):
        """处理错误答案"""
        self.statistics.record_wrong()
        
        feedback_messages = [
            "😅 再试一次吧！",
            "🤔 不对哦，再数数看",
            "💪 别放弃，继续加油！",
            "🔢 再仔细数一数",
            "📝 答案不对，重新选择"
        ]
        
        import random
        feedback = random.choice(feedback_messages)
        self.view.set_feedback(feedback, False)
        self.view.set_status_text("答案不对，请重新选择", False)
        
        self.view.clear_selection()
        self.is_answered = False
    
    def _show_level_up_message(self):
        """显示升级提示"""
        level_name = self.level_manager.level_name
        message = f"🎊 恭喜晋级！现在是 {level_name}！"
        
        popup = ctk.CTkToplevel(self.master)
        popup.title("恭喜升级！")
        popup.geometry("300x150")
        popup.resizable(False, False)
        popup.grab_set()
        
        label = ctk.CTkLabel(
            popup,
            text=message,
            font=("Microsoft YaHei", 18, "bold"),
            text_color="#FF6B6B"
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
        """下一题处理"""
        self._generate_new_question()
    
    def _on_restart(self):
        """重新开始处理"""
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
        """主题切换处理"""
        self.is_dark_theme = not self.is_dark_theme
        mode = "dark" if self.is_dark_theme else "light"
        ctk.set_appearance_mode(mode)