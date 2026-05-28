import customtkinter as ctk
import tkinter as tk
from config import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, COLORS, LEVELS, QUESTIONS, KNOWLEDGE_EXPLANATIONS
from progress import ProgressManager
from levels import GravityScene, FrictionScene, InclineScene, LeverScene, SpringScene, InertiaScene

class GameWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        self.center_window()
        
        self.current_theme = "light"
        self.current_level = 1
        self.progress_manager = ProgressManager()
        self.current_scene = None
        self.question_index = 0
        self.showing_question = False
        
        self.setup_ui()
        self.update_data_display()
        self.start_animation()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - WINDOW_WIDTH) // 2
        y = (screen_height - WINDOW_HEIGHT) // 2
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.create_top_bar()
        self.create_canvas_area()
        self.create_control_panel()
        self.create_status_bar()

    def create_top_bar(self):
        self.top_bar = ctk.CTkFrame(self, height=60, corner_radius=10)
        self.top_bar.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.top_bar.grid_columnconfigure(1, weight=1)
        
        self.title_label = ctk.CTkLabel(self.top_bar, text=APP_TITLE, font=("Arial", 18, "bold"))
        self.title_label.grid(row=0, column=0, padx=15, pady=10)
        
        self.level_info = ctk.CTkLabel(self.top_bar, text=f"关卡 {self.current_level}: {LEVELS[self.current_level-1]['name']}", 
                                      font=("Arial", 14))
        self.level_info.grid(row=0, column=1, padx=10)
        
        self.knowledge_label = ctk.CTkLabel(self.top_bar, text=f"知识点: {LEVELS[self.current_level-1]['knowledge']}",
                                           font=("Arial", 12), text_color="#4a90d9")
        self.knowledge_label.grid(row=1, column=1, padx=10)
        
        self.theme_button = ctk.CTkButton(self.top_bar, text="切换主题", command=self.toggle_theme,
                                         width=100, height=30)
        self.theme_button.grid(row=0, column=2, padx=15, pady=10, rowspan=2)

    def create_canvas_area(self):
        self.canvas_frame = ctk.CTkFrame(self, corner_radius=10)
        self.canvas_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        
        self.canvas = tk.Canvas(self.canvas_frame, width=600, height=450, 
                               bg=COLORS[self.current_theme]["canvas_bg"],
                               highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=10, pady=10)
        
        self.instruction_label = ctk.CTkLabel(self.canvas_frame, text=self.get_instruction(),
                                             font=("Arial", 12))
        self.instruction_label.grid(row=1, column=0, padx=10, pady=5)

    def create_control_panel(self):
        self.control_frame = ctk.CTkFrame(self, height=120, corner_radius=10)
        self.control_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.control_frame.grid_columnconfigure(0, weight=1)
        
        self.operation_buttons = ctk.CTkFrame(self.control_frame)
        self.operation_buttons.grid(row=0, column=0, padx=10, pady=10)
        
        self.action_button = ctk.CTkButton(self.operation_buttons, text=self.get_action_button_text(),
                                          command=self.perform_action, width=120, height=40,
                                          font=("Arial", 14))
        self.action_button.grid(row=0, column=0, padx=10)
        
        self.reset_button = ctk.CTkButton(self.operation_buttons, text="重置",
                                         command=self.reset_scene, width=100, height=40)
        self.reset_button.grid(row=0, column=1, padx=10)
        
        self.next_button = ctk.CTkButton(self.operation_buttons, text="下一关",
                                         command=self.next_level, width=100, height=40)
        self.next_button.grid(row=0, column=2, padx=10)
        
        self.question_button = ctk.CTkButton(self.operation_buttons, text="答题",
                                            command=self.show_question, width=100, height=40)
        self.question_button.grid(row=0, column=3, padx=10)
        
        self.knowledge_button = ctk.CTkButton(self.operation_buttons, text="查看知识点",
                                             command=self.show_knowledge, width=120, height=40)
        self.knowledge_button.grid(row=0, column=4, padx=10)
        
        self.create_parameter_sliders()

    def create_parameter_sliders(self):
        self.slider_frame = ctk.CTkFrame(self.control_frame)
        self.slider_frame.grid(row=1, column=0, padx=10, pady=5)
        
        self.sliders = {}
        
        if self.current_level == 2:
            self.create_slider("摩擦力", 0.1, 1.0, 0.5, self.on_friction_change)
        elif self.current_level == 3:
            self.create_slider("斜面角度", 10, 60, 30, self.on_angle_change)
        elif self.current_level == 4:
            self.create_slider("支点位置", 0.2, 0.8, 0.5, self.on_pivot_change)
            self.create_slider("左侧重量", 1, 10, 2, self.on_left_weight_change)
            self.create_slider("右侧重量", 1, 10, 2, self.on_right_weight_change)
        elif self.current_level == 5:
            self.create_slider("压缩距离", 0, 80, 0, self.on_compression_change)

    def create_slider(self, label, min_val, max_val, default, command):
        frame = ctk.CTkFrame(self.slider_frame)
        frame.pack(side="left", padx=15)
        
        label = ctk.CTkLabel(frame, text=label, font=("Arial", 12))
        label.pack(pady=2)
        
        slider = ctk.CTkSlider(frame, from_=min_val, to=max_val, 
                               command=command, width=150)
        slider.set(default)
        slider.pack(pady=5)
        
        value_label = ctk.CTkLabel(frame, text=f"{default:.1f}", font=("Arial", 12))
        value_label.pack(pady=2)
        
        self.sliders[label] = {"slider": slider, "label": value_label}

    def create_status_bar(self):
        self.status_frame = ctk.CTkFrame(self, height=50, corner_radius=10)
        self.status_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.status_frame.grid_columnconfigure(1, weight=1)
        
        self.data_display = ctk.CTkLabel(self.status_frame, text="", font=("Arial", 11))
        self.data_display.grid(row=0, column=0, padx=15, pady=10)
        
        self.progress_display = ctk.CTkLabel(self.status_frame, text=self.get_progress_text(), 
                                            font=("Arial", 11), text_color="#5cb85c")
        self.progress_display.grid(row=0, column=1, padx=15)

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        ctk.set_appearance_mode(self.current_theme)
        
        colors = COLORS[self.current_theme]
        self.canvas.config(bg=colors["canvas_bg"])
        self.data_display.configure(text_color=colors["text"])
        
        self.load_scene()

    def load_scene(self):
        if self.current_scene:
            self.current_scene.reset()
        
        colors = COLORS[self.current_theme]
        
        if self.current_level == 1:
            self.current_scene = GravityScene(self.canvas, colors)
        elif self.current_level == 2:
            self.current_scene = FrictionScene(self.canvas, colors)
        elif self.current_level == 3:
            self.current_scene = InclineScene(self.canvas, colors)
        elif self.current_level == 4:
            self.current_scene = LeverScene(self.canvas, colors)
        elif self.current_level == 5:
            self.current_scene = SpringScene(self.canvas, colors)
        elif self.current_level == 6:
            self.current_scene = InertiaScene(self.canvas, colors)
        
        self.level_info.configure(text=f"关卡 {self.current_level}: {LEVELS[self.current_level-1]['name']}")
        self.knowledge_label.configure(text=f"知识点: {LEVELS[self.current_level-1]['knowledge']}")
        self.instruction_label.configure(text=self.get_instruction())
        self.action_button.configure(text=self.get_action_button_text())
        
        self.slider_frame.destroy()
        self.create_parameter_sliders()

    def get_instruction(self):
        instructions = {
            1: "点击「释放小球」按钮，观察小球下落过程，感受重力的作用",
            2: "调节摩擦力系数后，点击「推动滑块」，观察滑行距离的变化",
            3: "调节斜面角度后，点击「释放物体」，观察下滑速度的变化",
            4: "调节支点位置和配重后，观察杠杆的平衡状态",
            5: "拖动滑块压缩弹簧后，点击「释放」，观察弹力作用",
            6: "点击「抽走书本」，观察鸡蛋保持静止的惯性现象"
        }
        return instructions.get(self.current_level, "")

    def get_action_button_text(self):
        texts = {
            1: "释放小球",
            2: "推动滑块",
            3: "释放物体",
            4: "释放杠杆",
            5: "释放弹簧",
            6: "抽走书本"
        }
        return texts.get(self.current_level, "开始")

    def perform_action(self):
        if self.current_scene:
            if self.current_level == 1:
                self.current_scene.drop()
            elif self.current_level == 2:
                self.current_scene.push()
            elif self.current_level == 3:
                self.current_scene.release()
            elif self.current_level == 4:
                self.current_scene.release()
            elif self.current_level == 5:
                self.current_scene.release()
            elif self.current_level == 6:
                self.current_scene.pull()

    def reset_scene(self):
        if self.current_scene:
            self.current_scene.reset()
            self.update_data_display()

    def next_level(self):
        if self.current_level < 6:
            self.current_level += 1
            self.progress_manager.set_current_level(self.current_level)
            self.load_scene()
            self.update_data_display()
            self.progress_display.configure(text=self.get_progress_text())

    def get_progress_text(self):
        completed = self.progress_manager.get_completed_count()
        total = len(LEVELS)
        return f"学习进度: {completed}/{total} 关卡"

    def show_question(self):
        if self.showing_question:
            return
        
        questions = QUESTIONS.get(self.current_level, [])
        if self.question_index >= len(questions):
            self.question_index = 0
        
        question_data = questions[self.question_index]
        self.showing_question = True
        
        self.question_dialog = ctk.CTkToplevel(self)
        self.question_dialog.title("随堂小测验")
        self.question_dialog.geometry("400x350")
        self.question_dialog.transient(self)
        self.question_dialog.grab_set()
        
        ctk.CTkLabel(self.question_dialog, text=question_data["question"], 
                     font=("Arial", 14), wraplength=350).pack(pady=20)
        
        self.selected_answer = tk.IntVar(value=-1)
        for i, option in enumerate(question_data["options"]):
            ctk.CTkRadioButton(self.question_dialog, text=option, variable=self.selected_answer,
                              value=i, font=("Arial", 12)).pack(pady=5, anchor="w", padx=20)
        
        ctk.CTkButton(self.question_dialog, text="提交答案", 
                      command=lambda: self.check_answer(question_data)).pack(pady=20)
        
        ctk.CTkButton(self.question_dialog, text="查看提示", 
                      command=lambda: self.show_hint(question_data),
                      text_color="#f0ad4e").pack(pady=5)

    def show_hint(self, question_data):
        hint_dialog = ctk.CTkToplevel(self)
        hint_dialog.title("提示")
        hint_dialog.geometry("300x150")
        hint_dialog.transient(self)
        hint_dialog.grab_set()
        
        ctk.CTkLabel(hint_dialog, text=question_data["hint"], 
                     font=("Arial", 12), wraplength=250).pack(pady=30)
        
        ctk.CTkButton(hint_dialog, text="知道了", command=hint_dialog.destroy).pack(pady=10)

    def check_answer(self, question_data):
        selected = self.selected_answer.get()
        is_correct = selected == question_data["answer"]
        
        self.progress_manager.record_answer(self.current_level, is_correct)
        
        result_dialog = ctk.CTkToplevel(self)
        result_dialog.title("答题结果")
        result_dialog.geometry("350x200")
        result_dialog.transient(self)
        result_dialog.grab_set()
        
        if is_correct:
            ctk.CTkLabel(result_dialog, text="🎉 回答正确！太棒了！", 
                         font=("Arial", 16, "bold"), text_color="#5cb85c").pack(pady=30)
            self.progress_manager.complete_level(self.current_level)
        else:
            ctk.CTkLabel(result_dialog, text="😅 回答错误，再想想吧！", 
                         font=("Arial", 14), text_color="#d9534f").pack(pady=20)
            ctk.CTkLabel(result_dialog, text=question_data["hint"], 
                         font=("Arial", 12), wraplength=300).pack(pady=10)
        
        ctk.CTkButton(result_dialog, text="确定", 
                      command=lambda: self.close_dialogs(result_dialog)).pack(pady=20)
        
        self.question_index += 1
        self.update_data_display()
        self.progress_display.configure(text=self.get_progress_text())

    def close_dialogs(self, result_dialog):
        result_dialog.destroy()
        self.question_dialog.destroy()
        self.showing_question = False

    def show_knowledge(self):
        explanation = KNOWLEDGE_EXPLANATIONS.get(self.current_level, "")
        
        knowledge_dialog = ctk.CTkToplevel(self)
        knowledge_dialog.title(f"{LEVELS[self.current_level-1]['knowledge']} - 知识点讲解")
        knowledge_dialog.geometry("500x350")
        knowledge_dialog.transient(self)
        knowledge_dialog.grab_set()
        
        ctk.CTkLabel(knowledge_dialog, text=LEVELS[self.current_level-1]['name'], 
                     font=("Arial", 16, "bold")).pack(pady=15)
        
        ctk.CTkLabel(knowledge_dialog, text=explanation, 
                     font=("Arial", 12), wraplength=450, justify="left").pack(pady=20, padx=20)
        
        ctk.CTkButton(knowledge_dialog, text="知道了", 
                      command=knowledge_dialog.destroy).pack(pady=20)

    def on_friction_change(self, value):
        if self.current_scene:
            self.current_scene.set_friction(value)
            self.sliders["摩擦力"]["label"].configure(text=f"{value:.2f}")
            self.update_data_display()

    def on_angle_change(self, value):
        if self.current_scene:
            self.current_scene.set_angle(int(value))
            self.sliders["斜面角度"]["label"].configure(text=f"{int(value)}°")
            self.update_data_display()

    def on_pivot_change(self, value):
        if self.current_scene:
            self.current_scene.set_pivot(value)
            self.sliders["支点位置"]["label"].configure(text=f"{int(value*100)}%")

    def on_left_weight_change(self, value):
        if self.current_scene:
            self.current_scene.set_weights(int(value), self.current_scene.right_weight)
            self.sliders["左侧重量"]["label"].configure(text=f"{int(value)}kg")

    def on_right_weight_change(self, value):
        if self.current_scene:
            self.current_scene.set_weights(self.current_scene.left_weight, int(value))
            self.sliders["右侧重量"]["label"].configure(text=f"{int(value)}kg")

    def on_compression_change(self, value):
        if self.current_scene:
            self.current_scene.compress(value)
            self.sliders["压缩距离"]["label"].configure(text=f"{int(value)}px")

    def update_data_display(self):
        if self.current_scene:
            data = self.current_scene.get_data()
            text = " | ".join([f"{k}: {v}" for k, v in data.items()])
            self.data_display.configure(text=text)

    def start_animation(self):
        if self.current_scene:
            self.current_scene.update()
            self.update_data_display()
        self.after(16, self.start_animation)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    app = GameWindow()
    app.mainloop()