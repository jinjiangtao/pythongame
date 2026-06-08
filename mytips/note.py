import customtkinter as ctk
from tkinter import Menu, messagebox
from utils import NOTE_COLORS
from reminder import ReminderWindow


class NoteWindow(ctk.CTkToplevel):
    def __init__(self, parent, db, note_id=None, content="", x=100, y=100, width=300, height=300,
                 color='yellow', opacity=0.95, font_size=14, is_topmost=False, reminder_time=None):
        super().__init__(parent)
        self.db = db
        self.note_id = note_id
        self._drag_data = {'x': 0, 'y': 0}
        self.color = color
        self.opacity = opacity
        self.font_size = font_size
        self.is_topmost = is_topmost
        self.reminder_time = reminder_time
        self.content = content
        self.on_close_callback = None
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.overrideredirect(True)
        self.attributes('-alpha', opacity)
        self.attributes('-topmost', is_topmost)
        
        self._create_widgets()
        self._setup_bindings()
        self._create_context_menu()
        
        if note_id is None:
            self._save_to_db()
        
    def _create_widgets(self):
        bg_color, _, _ = NOTE_COLORS[self.color]
        
        self.title_bar = ctk.CTkFrame(self, height=30, fg_color=bg_color)
        self.title_bar.pack(fill="x", side="top")
        self.title_bar.bind('<Button-1>', self._on_drag_start)
        self.title_bar.bind('<B1-Motion>', self._on_drag_motion)
        
        self.minimize_btn = ctk.CTkButton(self.title_bar, text="−", width=30, height=25,
                                          fg_color="transparent", hover_color="#aaaaaa",
                                          text_color="#333333", command=self._on_minimize)
        self.minimize_btn.pack(side="right", padx=5, pady=2)
        
        self.close_btn = ctk.CTkButton(self.title_bar, text="✕", width=30, height=25,
                                       fg_color="transparent", hover_color="#ff6666",
                                       text_color="#333333", command=self._on_close)
        self.close_btn.pack(side="right", padx=0, pady=2)
        
        self.content_frame = ctk.CTkFrame(self, fg_color=bg_color)
        self.content_frame.pack(fill="both", expand=True)
        
        self.text_box = ctk.CTkTextbox(self.content_frame, fg_color=bg_color,
                                       text_color="#333333", font=("Microsoft YaHei", self.font_size))
        self.text_box.pack(fill="both", expand=True, padx=5, pady=5)
        self.text_box.insert("0.0", self.content)
        self.text_box.bind('<FocusOut>', self._on_text_change)
        
        self.reminder_label = ctk.CTkLabel(self, text="", fg_color=bg_color, text_color="#666666",
                                           font=("Microsoft YaHei", 10))
        self.reminder_label.pack(fill="x", padx=5, pady=2)
        if self.reminder_time:
            self.reminder_label.configure(text=f"📅 {self.reminder_time}")
        
    def _setup_bindings(self):
        self.text_box.bind('<Double-Button-1>', lambda e: None)
        self.bind('<Configure>', self._on_configure)
        
    def _create_context_menu(self):
        self.context_menu = Menu(self, tearoff=0)
        
        color_menu = Menu(self.context_menu, tearoff=0)
        color_menu.add_command(label="黄色", command=lambda: self._set_color('yellow'))
        color_menu.add_command(label="蓝色", command=lambda: self._set_color('blue'))
        color_menu.add_command(label="绿色", command=lambda: self._set_color('green'))
        color_menu.add_command(label="粉色", command=lambda: self._set_color('pink'))
        color_menu.add_command(label="紫色", command=lambda: self._set_color('purple'))
        self.context_menu.add_cascade(label="换颜色", menu=color_menu)
        
        self.context_menu.add_command(label="添加复选框", command=self._add_checkbox)
        
        self.opacity_menu = Menu(self.context_menu, tearoff=0)
        self.opacity_var = ctk.DoubleVar(value=self.opacity)
        self.opacity_menu.add_command(label="调整透明度...", command=self._show_opacity_dialog)
        self.context_menu.add_cascade(label="透明度", menu=self.opacity_menu)
        
        self.font_menu = Menu(self.context_menu, tearoff=0)
        for size in [10, 12, 14, 16, 18, 20, 24]:
            self.font_menu.add_command(label=f"{size} 号", command=lambda s=size: self._set_font_size(s))
        self.context_menu.add_cascade(label="字体大小", menu=self.font_menu)
        
        self.topmost_var = ctk.BooleanVar(value=self.is_topmost)
        self.context_menu.add_checkbutton(label="置顶", variable=self.topmost_var, command=self._toggle_topmost)
        
        self.context_menu.add_command(label="设置提醒...", command=self._show_reminder_dialog)
        
        self.content_frame.bind('<Button-3>', self._show_context_menu)
        self.text_box.bind('<Button-3>', self._show_context_menu)
        self.title_bar.bind('<Button-3>', self._show_context_menu)
        
    def _show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
            
    def _set_color(self, color):
        self.color = color
        bg_color, _, _ = NOTE_COLORS[color]
        self.title_bar.configure(fg_color=bg_color)
        self.content_frame.configure(fg_color=bg_color)
        self.text_box.configure(fg_color=bg_color)
        self.reminder_label.configure(fg_color=bg_color)
        self._update_db()
        
    def _add_checkbox(self):
        self.text_box.insert("insert", "□ ")
        
    def _show_opacity_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("调整透明度")
        dialog.geometry("300x150")
        
        slider = ctk.CTkSlider(dialog, from_=0.3, to=1.0, number_of_steps=70)
        slider.set(self.opacity)
        slider.pack(pady=30, padx=20, fill="x")
        
        def apply():
            self.opacity = slider.get()
            self.attributes('-alpha', self.opacity)
            self._update_db()
            dialog.destroy()
            
        ctk.CTkButton(dialog, text="确定", command=apply).pack(pady=10)
        
    def _set_font_size(self, size):
        self.font_size = size
        self.text_box.configure(font=("Microsoft YaHei", size))
        self._update_db()
        
    def _toggle_topmost(self):
        self.is_topmost = self.topmost_var.get()
        self.attributes('-topmost', self.is_topmost)
        self._update_db()
        
    def _show_reminder_dialog(self):
        ReminderWindow(self, self.note_id, self.db, self._on_reminder_set)
        
    def _on_reminder_set(self, reminder_time):
        self.reminder_time = reminder_time
        if reminder_time:
            self.reminder_label.configure(text=f"📅 {reminder_time}")
        else:
            self.reminder_label.configure(text="")
        self._update_db()
        
    def _on_drag_start(self, event):
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y
        
    def _on_drag_motion(self, event):
        x = self.winfo_x() + (event.x - self._drag_data['x'])
        y = self.winfo_y() + (event.y - self._drag_data['y'])
        self.geometry(f"+{x}+{y}")
        self._update_db()
        
    def _on_configure(self, event):
        if self.note_id:
            self._update_db()
            
    def _on_text_change(self, event=None):
        self.content = self.text_box.get("0.0", "end-1c")
        if self.note_id:
            self._update_db()
            
    def _save_to_db(self):
        self.note_id = self.db.create_note(
            content=self.content,
            x=self.winfo_x(),
            y=self.winfo_y(),
            width=self.winfo_width(),
            height=self.winfo_height(),
            color=self.color,
            opacity=self.opacity,
            font_size=self.font_size,
            is_topmost=self.is_topmost,
            reminder_time=self.reminder_time
        )
        
    def _update_db(self):
        if self.note_id:
            self.db.update_note(
                self.note_id,
                content=self.content,
                x=self.winfo_x(),
                y=self.winfo_y(),
                width=self.winfo_width(),
                height=self.winfo_height(),
                color=self.color,
                opacity=self.opacity,
                font_size=self.font_size,
                is_topmost=self.is_topmost,
                reminder_time=self.reminder_time
            )
            
    def _on_close(self):
        if self.note_id:
            self.db.delete_note(self.note_id)
        if self.on_close_callback:
            self.on_close_callback(self)
        self.destroy()
        
    def _on_minimize(self):
        self.withdraw()
        
    def set_on_close(self, callback):
        self.on_close_callback = callback
