import os
import time
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image

from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, PREVIEW_SIZE,
    DEFAULT_LANGUAGE, DEFAULT_MODE, AUTO_COPY_TO_CLIPBOARD
)
from utils import (
    resize_image, image_to_tkinter, copy_to_clipboard,
    export_to_txt, export_to_docx
)
from image_processor import ImageProcessor
from ocr_engine import OCREngine
from screenshot import ScreenshotSelector
from history_manager import HistoryManager
from batch_processor import BatchProcessor


class OCRApp:
    def __init__(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        self.current_image_path = None
        self.current_image_name = "截图"
        
        self.image_processor = ImageProcessor()
        self.ocr_engine = OCREngine()
        self.history_manager = HistoryManager()
        self.batch_processor = BatchProcessor()
        
        self.selected_language = ctk.StringVar(value=DEFAULT_LANGUAGE)
        self.selected_mode = ctk.StringVar(value=DEFAULT_MODE)
        self.auto_copy = ctk.BooleanVar(value=AUTO_COPY_TO_CLIPBOARD)
        
        self.setup_ui()
        self.load_history()
    
    def setup_ui(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        button_frame = ctk.CTkFrame(main_frame, height=60)
        button_frame.pack(fill=ctk.X, pady=(0, 10))
        button_frame.pack_propagate(False)
        
        self.btn_screenshot = ctk.CTkButton(
            button_frame, text="📷 截图识别", command=self.start_screenshot
        )
        self.btn_screenshot.pack(side=ctk.LEFT, padx=5, pady=10)
        
        self.btn_open = ctk.CTkButton(
            button_frame, text="📂 打开图片", command=self.open_image
        )
        self.btn_open.pack(side=ctk.LEFT, padx=5, pady=10)
        
        self.btn_batch = ctk.CTkButton(
            button_frame, text="📦 批量识别", command=self.start_batch
        )
        self.btn_batch.pack(side=ctk.LEFT, padx=5, pady=10)
        
        ctk.CTkLabel(button_frame, text="语言:").pack(side=ctk.LEFT, padx=(20, 5), pady=10)
        self.lang_menu = ctk.CTkOptionMenu(
            button_frame, values=["中文", "英文", "中英文混合"], variable=self.selected_language
        )
        self.lang_menu.pack(side=ctk.LEFT, padx=5, pady=10)
        
        ctk.CTkLabel(button_frame, text="模式:").pack(side=ctk.LEFT, padx=(20, 5), pady=10)
        self.mode_menu = ctk.CTkOptionMenu(
            button_frame, values=["快速模式", "精准模式"], variable=self.selected_mode
        )
        self.mode_menu.pack(side=ctk.LEFT, padx=5, pady=10)
        
        self.auto_copy_check = ctk.CTkCheckBox(
            button_frame, text="自动复制", variable=self.auto_copy
        )
        self.auto_copy_check.pack(side=ctk.LEFT, padx=(20, 5), pady=10)
        
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill=ctk.BOTH, expand=True)
        
        left_frame = ctk.CTkFrame(content_frame, width=450)
        left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=False, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        self.tabview = ctk.CTkTabview(left_frame)
        self.tabview.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)
        
        self.tab_image = self.tabview.add("图片")
        self.tab_preprocess = self.tabview.add("预处理")
        self.tab_history = self.tabview.add("历史")
        
        self.setup_image_tab()
        self.setup_preprocess_tab()
        self.setup_history_tab()
        
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)
        
        result_header = ctk.CTkFrame(right_frame, height=50)
        result_header.pack(fill=ctk.X, padx=5, pady=5)
        result_header.pack_propagate(False)
        
        ctk.CTkLabel(result_header, text="识别结果", font=ctk.CTkFont(size=16, weight="bold")).pack(side=ctk.LEFT, padx=10)
        
        self.btn_recognize = ctk.CTkButton(
            result_header, text="🔍 开始识别", command=self.recognize_text
        )
        self.btn_recognize.pack(side=ctk.RIGHT, padx=5)
        
        self.btn_copy = ctk.CTkButton(
            result_header, text="📋 复制", command=self.copy_result
        )
        self.btn_copy.pack(side=ctk.RIGHT, padx=5)
        
        self.btn_export = ctk.CTkButton(
            result_header, text="💾 导出", command=self.export_result
        )
        self.btn_export.pack(side=ctk.RIGHT, padx=5)
        
        self.result_text = ctk.CTkTextbox(right_frame)
        self.result_text.pack(fill=ctk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        self.status_bar = ctk.CTkLabel(
            main_frame, text="就绪", anchor="w", height=30
        )
        self.status_bar.pack(fill=ctk.X, pady=(10, 0))
    
    def setup_image_tab(self):
        self.image_label = ctk.CTkLabel(
            self.tab_image, text="请打开或截取图片"
        )
        self.image_label.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
    
    def setup_preprocess_tab(self):
        preprocess_frame = ctk.CTkScrollableFrame(self.tab_preprocess)
        preprocess_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        ctk.CTkButton(
            preprocess_frame, text="灰度化", command=self.preprocess_gray
        ).pack(fill=ctk.X, pady=5)
        
        ctk.CTkButton(
            preprocess_frame, text="二值化", command=self.preprocess_binary
        ).pack(fill=ctk.X, pady=5)
        
        ctk.CTkButton(
            preprocess_frame, text="去噪", command=self.preprocess_denoise
        ).pack(fill=ctk.X, pady=5)
        
        ctk.CTkButton(
            preprocess_frame, text="自动旋转", command=self.preprocess_rotate
        ).pack(fill=ctk.X, pady=5)
        
        ctk.CTkLabel(preprocess_frame, text="亮度调节").pack(pady=(10, 0))
        self.brightness_slider = ctk.CTkSlider(
            preprocess_frame, from_=-100, to=100, number_of_steps=200,
            command=lambda v: self.update_brightness_contrast()
        )
        self.brightness_slider.set(0)
        self.brightness_slider.pack(fill=ctk.X, pady=5)
        
        ctk.CTkLabel(preprocess_frame, text="对比度调节").pack(pady=(10, 0))
        self.contrast_slider = ctk.CTkSlider(
            preprocess_frame, from_=-100, to=100, number_of_steps=200,
            command=lambda v: self.update_brightness_contrast()
        )
        self.contrast_slider.set(0)
        self.contrast_slider.pack(fill=ctk.X, pady=5)
        
        ctk.CTkButton(
            preprocess_frame, text="重置", command=self.preprocess_reset
        ).pack(fill=ctk.X, pady=(20, 5))
    
    def setup_history_tab(self):
        self.history_list = ctk.CTkScrollableFrame(self.tab_history)
        self.history_list.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
    
    def load_history(self):
        records = self.history_manager.get_all_records()
        
        for widget in self.history_list.winfo_children():
            widget.destroy()
        
        for record in records:
            record_id, timestamp, image_name, _, _ = record
            btn = ctk.CTkButton(
                self.history_list,
                text=f"{timestamp} - {image_name}",
                command=lambda rid=record_id: self.load_history_record(rid)
            )
            btn.pack(fill=ctk.X, pady=2)
    
    def load_history_record(self, record_id):
        record = self.history_manager.get_record(record_id)
        if record:
            _, _, image_name, image_path, ocr_result = record
            
            if image_path and os.path.exists(image_path):
                self.open_image_file(image_path)
            
            self.result_text.delete("1.0", ctk.END)
            self.result_text.insert("1.0", ocr_result)
            self.current_image_name = image_name
    
    def start_screenshot(self):
        self.root.withdraw()
        time.sleep(0.2)
        
        ScreenshotSelector(self.on_screenshot_done)
    
    def on_screenshot_done(self, cv_image, pil_image):
        self.root.deiconify()
        
        if cv_image is not None and pil_image is not None:
            self.image_processor.set_image(cv_image)
            self.current_image_path = None
            self.current_image_name = "截图"
            self.display_image(pil_image)
            self.set_status("截图完成，点击识别开始OCR")
    
    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.bmp *.tiff"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.open_image_file(file_path)
    
    def open_image_file(self, file_path):
        if self.image_processor.load_image(file_path):
            self.current_image_path = file_path
            self.current_image_name = os.path.basename(file_path)
            pil_image = self.image_processor.to_pil(self.image_processor.get_original_image())
            self.display_image(pil_image)
            self.set_status(f"已加载: {self.current_image_name}")
    
    def display_image(self, pil_image):
        resized = resize_image(pil_image, PREVIEW_SIZE)
        tk_image = image_to_tkinter(resized)
        self.image_label.configure(image=tk_image, text="")
        self.image_label.image = tk_image
    
    def preprocess_gray(self):
        if self.image_processor.get_original_image() is not None:
            self.image_processor.to_gray()
            self.update_display()
    
    def preprocess_binary(self):
        if self.image_processor.get_original_image() is not None:
            self.image_processor.to_binary()
            self.update_display()
    
    def preprocess_denoise(self):
        if self.image_processor.get_original_image() is not None:
            self.image_processor.denoise()
            self.update_display()
    
    def preprocess_rotate(self):
        if self.image_processor.get_original_image() is not None:
            self.image_processor.auto_rotate()
            self.update_display()
    
    def update_brightness_contrast(self):
        if self.image_processor.get_original_image() is not None:
            brightness = self.brightness_slider.get()
            contrast = self.contrast_slider.get()
            self.image_processor.reset()
            self.image_processor.adjust_brightness_contrast(brightness, contrast)
            self.update_display()
    
    def preprocess_reset(self):
        if self.image_processor.get_original_image() is not None:
            self.image_processor.reset()
            self.brightness_slider.set(0)
            self.contrast_slider.set(0)
            self.update_display()
    
    def update_display(self):
        pil_image = self.image_processor.to_pil()
        self.display_image(pil_image)
    
    def recognize_text(self):
        if self.image_processor.get_original_image() is None:
            messagebox.showwarning("警告", "请先打开或截取图片")
            return
        
        self.set_status("识别中...")
        self.btn_recognize.configure(state="disabled")
        
        def recognize_thread():
            try:
                start_time = time.time()
                pil_image = self.image_processor.to_pil()
                result = self.ocr_engine.recognize(
                    pil_image,
                    self.selected_language.get(),
                    self.selected_mode.get()
                )
                elapsed = time.time() - start_time
                
                self.root.after(0, lambda: self.on_recognize_done(result, elapsed))
            except Exception as e:
                self.root.after(0, lambda: self.set_status(f"识别失败: {str(e)}"))
                self.root.after(0, lambda: self.btn_recognize.configure(state="normal"))
        
        threading.Thread(target=recognize_thread, daemon=True).start()
    
    def on_recognize_done(self, result, elapsed):
        self.result_text.delete("1.0", ctk.END)
        self.result_text.insert("1.0", result)
        
        if self.auto_copy.get() and result:
            copy_to_clipboard(result)
        
        self.history_manager.add_record(
            self.current_image_name,
            self.current_image_path,
            result
        )
        self.load_history()
        
        self.set_status(f"识别完成，耗时 {elapsed:.2f} 秒")
        self.btn_recognize.configure(state="normal")
    
    def copy_result(self):
        text = self.result_text.get("1.0", ctk.END).strip()
        if text:
            if copy_to_clipboard(text):
                self.set_status("已复制到剪贴板")
            else:
                self.set_status("复制失败")
    
    def export_result(self):
        text = self.result_text.get("1.0", ctk.END).strip()
        if not text:
            messagebox.showwarning("警告", "没有可导出的内容")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("文本文件", "*.txt"),
                ("Word文档", "*.docx"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            ext = os.path.splitext(file_path)[1].lower()
            if ext == '.docx':
                if export_to_docx(text, file_path):
                    self.set_status(f"已导出到: {file_path}")
                else:
                    self.set_status("导出失败，请确保已安装 python-docx")
            else:
                if export_to_txt(text, file_path):
                    self.set_status(f"已导出到: {file_path}")
                else:
                    self.set_status("导出失败")
    
    def start_batch(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.set_status("开始批量处理...")
            self.root.update()
            
            results = self.batch_processor.process_folder(
                folder_path,
                self.selected_language.get(),
                self.selected_mode.get(),
                lambda c, t: self.set_status(f"处理中: {c}/{t}")
            )
            
            success_count = sum(1 for r in results if r['status'] == '成功')
            self.set_status(f"批量处理完成: {success_count}/{len(results)} 成功")
            
            messagebox.showinfo(
                "完成",
                f"批量处理完成\n成功: {success_count}\n总数: {len(results)}"
            )
    
    def set_status(self, text):
        self.status_bar.configure(text=text)
    
    def run(self):
        self.root.mainloop()
    
    def close(self):
        self.history_manager.close()
