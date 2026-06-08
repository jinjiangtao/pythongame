
import customtkinter as ctk
from tkinter import filedialog, messagebox
from image_list import ImageList
from preview import PreviewPanel
from processor import BatchProcessor
from settings import DEFAULT_SETTINGS, COLOR_PRESETS, POSITION_MAP
from utils import get_image_files, get_available_fonts, get_default_chinese_font


class WatermarkApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('批量图片水印工具')
        self.geometry('1000x700')
        
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')
        
        self.settings = DEFAULT_SETTINGS.copy()
        self.settings['mode'] = 'text'
        self.settings['font'] = get_default_chinese_font()
        self.settings['output_mode'] = '新文件夹'
        self.settings['watermark_image'] = None
        
        self.processor = BatchProcessor()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._create_left_panel()
        self._create_right_panel()
        
        self._update_preview_settings()
    
    def _create_left_panel(self):
        left_frame = ctk.CTkFrame(self)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(0, weight=1)
        
        self.image_list = ImageList(left_frame, on_preview=self._on_preview_click)
        self.image_list.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        btn_frame = ctk.CTkFrame(left_frame, fg_color='transparent')
        btn_frame.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        
        ctk.CTkButton(btn_frame, text='添加图片', command=self._add_images, width=100, height=32).pack(side='left', padx=5, pady=5)
        ctk.CTkButton(btn_frame, text='添加文件夹', command=self._add_folder, width=100, height=32).pack(side='left', padx=5, pady=5)
        ctk.CTkButton(btn_frame, text='全选', command=self.image_list.select_all, width=80, height=32).pack(side='left', padx=5, pady=5)
        ctk.CTkButton(btn_frame, text='清空', command=self.image_list.clear, width=80, height=32).pack(side='left', padx=5, pady=5)
    
    def _create_right_panel(self):
        right_frame = ctk.CTkFrame(self)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(2, weight=1)
        
        watermark_frame = ctk.CTkFrame(right_frame)
        watermark_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        
        self.mode_var = ctk.StringVar(value='text')
        mode_frame = ctk.CTkFrame(watermark_frame, fg_color='transparent')
        mode_frame.pack(fill='x', padx=5, pady=5)
        ctk.CTkRadioButton(mode_frame, text='文字水印', variable=self.mode_var, value='text', command=self._switch_mode).pack(side='left', padx=5)
        ctk.CTkRadioButton(mode_frame, text='图片水印', variable=self.mode_var, value='image', command=self._switch_mode).pack(side='left', padx=5)
        
        self.text_frame = ctk.CTkFrame(watermark_frame, fg_color='transparent')
        self.text_frame.pack(fill='x', padx=5, pady=5)
        
        ctk.CTkLabel(self.text_frame, text='文字:').grid(row=0, column=0, padx=5, pady=5)
        self.text_entry = ctk.CTkEntry(self.text_frame)
        self.text_entry.insert(0, self.settings['text'])
        self.text_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.text_entry.bind('<KeyRelease>', self._on_setting_change)
        
        ctk.CTkLabel(self.text_frame, text='字体:').grid(row=1, column=0, padx=5, pady=5)
        self.font_combo = ctk.CTkComboBox(self.text_frame, values=get_available_fonts())
        self.font_combo.set(self.settings['font'])
        self.font_combo.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.font_combo.bind('<<ComboboxSelected>>', self._on_setting_change)
        
        ctk.CTkLabel(self.text_frame, text='字号:').grid(row=2, column=0, padx=5, pady=5)
        self.font_size_slider = ctk.CTkSlider(self.text_frame, from_=10, to=100, number_of_steps=90)
        self.font_size_slider.set(self.settings['font_size'])
        self.font_size_slider.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        self.font_size_slider.configure(command=self._on_setting_change)
        
        ctk.CTkLabel(self.text_frame, text='颜色:').grid(row=3, column=0, padx=5, pady=5)
        color_frame = ctk.CTkFrame(self.text_frame, fg_color='transparent')
        color_frame.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        self.color_combo = ctk.CTkComboBox(color_frame, values=[name for name, _ in COLOR_PRESETS])
        self.color_combo.set('白色')
        self.color_combo.pack(side='left', padx=2)
        self.color_combo.bind('<<ComboboxSelected>>', self._on_color_change)
        self.color_entry = ctk.CTkEntry(color_frame, width=80)
        self.color_entry.insert(0, self.settings['color'])
        self.color_entry.pack(side='left', padx=2)
        self.color_entry.bind('<KeyRelease>', self._on_setting_change)
        
        ctk.CTkLabel(self.text_frame, text='旋转:').grid(row=4, column=0, padx=5, pady=5)
        self.rotation_slider = ctk.CTkSlider(self.text_frame, from_=-45, to=45, number_of_steps=90)
        self.rotation_slider.set(self.settings['rotation'])
        self.rotation_slider.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        self.rotation_slider.configure(command=self._on_setting_change)
        
        self.text_frame.grid_columnconfigure(1, weight=1)
        
        self.image_frame = ctk.CTkFrame(watermark_frame, fg_color='transparent')
        
        ctk.CTkButton(self.image_frame, text='选择水印图片', command=self._select_watermark_image).pack(fill='x', padx=5, pady=5)
        self.watermark_path_label = ctk.CTkLabel(self.image_frame, text='未选择', anchor='w')
        self.watermark_path_label.pack(fill='x', padx=5, pady=2)
        
        ctk.CTkLabel(self.image_frame, text='缩放:').pack(anchor='w', padx=5, pady=2)
        self.scale_slider = ctk.CTkSlider(self.image_frame, from_=0.1, to=1.0, number_of_steps=90)
        self.scale_slider.set(self.settings['image_scale'])
        self.scale_slider.pack(fill='x', padx=5, pady=5)
        self.scale_slider.configure(command=self._on_setting_change)
        
        pos_style_frame = ctk.CTkFrame(right_frame)
        pos_style_frame.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        
        ctk.CTkLabel(pos_style_frame, text='位置:').grid(row=0, column=0, padx=5, pady=5)
        self.position_combo = ctk.CTkComboBox(pos_style_frame, values=list(POSITION_MAP.keys()))
        self.position_combo.set(self.settings['position'])
        self.position_combo.grid(row=0, column=1, padx=5, pady=5)
        self.position_combo.bind('<<ComboboxSelected>>', self._on_setting_change)
        
        ctk.CTkLabel(pos_style_frame, text='边距:').grid(row=0, column=2, padx=5, pady=5)
        self.margin_slider = ctk.CTkSlider(pos_style_frame, from_=0, to=100, number_of_steps=100)
        self.margin_slider.set(self.settings['margin'])
        self.margin_slider.grid(row=0, column=3, padx=5, pady=5)
        self.margin_slider.configure(command=self._on_setting_change)
        
        ctk.CTkLabel(pos_style_frame, text='透明度:').grid(row=1, column=0, padx=5, pady=5)
        self.opacity_slider = ctk.CTkSlider(pos_style_frame, from_=0, to=1, number_of_steps=100)
        self.opacity_slider.set(self.settings['opacity'])
        self.opacity_slider.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky='ew')
        self.opacity_slider.configure(command=self._on_setting_change)
        
        pos_style_frame.grid_columnconfigure(3, weight=1)
        
        self.preview_panel = PreviewPanel(right_frame)
        self.preview_panel.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        
        output_frame = ctk.CTkFrame(right_frame)
        output_frame.grid(row=3, column=0, padx=5, pady=5, sticky='ew')
        
        # 第一行：输出模式
        row1 = ctk.CTkFrame(output_frame, fg_color='transparent')
        row1.pack(fill='x', pady=3)
        self.output_mode_var = ctk.StringVar(value='新文件夹')
        ctk.CTkRadioButton(row1, text='输出到新文件夹', variable=self.output_mode_var, value='新文件夹').pack(side='left', padx=5)
        ctk.CTkRadioButton(row1, text='覆盖原图', variable=self.output_mode_var, value='覆盖').pack(side='left', padx=5)
        
        # 第二行：格式、质量、命名
        row2 = ctk.CTkFrame(output_frame, fg_color='transparent')
        row2.pack(fill='x', pady=3)
        
        ctk.CTkLabel(row2, text='格式:').pack(side='left', padx=5)
        self.format_combo = ctk.CTkComboBox(row2, values=['保持原格式', '统一转成JPG'], width=120)
        self.format_combo.set(self.settings['output_format'])
        self.format_combo.pack(side='left', padx=5)
        
        ctk.CTkLabel(row2, text='JPG质量:').pack(side='left', padx=5)
        self.quality_slider = ctk.CTkSlider(row2, from_=10, to=100, number_of_steps=90, width=100)
        self.quality_slider.set(self.settings['jpg_quality'])
        self.quality_slider.pack(side='left', padx=5)
        
        ctk.CTkLabel(row2, text='命名:').pack(side='left', padx=5)
        self.name_rule_combo = ctk.CTkComboBox(row2, values=['原文件名_watermarked', '自定义前缀'], width=150)
        self.name_rule_combo.set(self.settings['filename_rule'])
        self.name_rule_combo.pack(side='left', padx=5)
        self.name_rule_combo.bind('<<ComboboxSelected>>', self._on_name_rule_change)
        
        self.prefix_entry = ctk.CTkEntry(row2, width=80)
        self.prefix_entry.insert(0, self.settings['custom_prefix'])
        self.prefix_entry.pack(side='left', padx=5)
        self.prefix_entry.configure(state='disabled')
        
        action_frame = ctk.CTkFrame(right_frame)
        action_frame.grid(row=4, column=0, padx=5, pady=5, sticky='ew')
        
        self.start_btn = ctk.CTkButton(action_frame, text='开始处理', command=self._start_processing, height=36)
        self.start_btn.pack(side='left', padx=5, fill='x', expand=True)
        
        self.progress = ctk.CTkProgressBar(action_frame, height=12)
        self.progress.pack(side='left', padx=5, fill='x', expand=True)
        self.progress.set(0)
        
        self.progress_label = ctk.CTkLabel(action_frame, text='0/0', width=50)
        self.progress_label.pack(side='left', padx=5)
    
    def _add_images(self):
        files = filedialog.askopenfilenames(
            title='选择图片',
            filetypes=[('图片文件', '*.jpg *.jpeg *.png *.webp'), ('所有文件', '*.*')]
        )
        if files:
            self.image_list.add_images(list(files))
    
    def _add_folder(self):
        folder = filedialog.askdirectory(title='选择文件夹')
        if folder:
            files = get_image_files(folder)
            self.image_list.add_images(files)
    
    def _switch_mode(self):
        mode = self.mode_var.get()
        self.settings['mode'] = mode
        if mode == 'text':
            self.image_frame.pack_forget()
            self.text_frame.pack(fill='x', padx=5, pady=5)
        else:
            self.text_frame.pack_forget()
            self.image_frame.pack(fill='x', padx=5, pady=5)
        self._update_preview_settings()
    
    def _select_watermark_image(self):
        file = filedialog.askopenfilename(
            title='选择水印图片',
            filetypes=[('PNG图片', '*.png'), ('所有文件', '*.*')]
        )
        if file:
            self.settings['watermark_image'] = file
            self.watermark_path_label.configure(text=file)
            self._update_preview_settings()
    
    def _on_setting_change(self, *args):
        self._update_preview_settings()
    
    def _on_color_change(self, *args):
        color_name = self.color_combo.get()
        for name, hex_val in COLOR_PRESETS:
            if name == color_name:
                self.color_entry.delete(0, 'end')
                self.color_entry.insert(0, hex_val)
                break
        self._update_preview_settings()
    
    def _on_name_rule_change(self, *args):
        rule = self.name_rule_combo.get()
        if rule == '自定义前缀':
            self.prefix_entry.configure(state='normal')
        else:
            self.prefix_entry.configure(state='disabled')
    
    def _on_preview_click(self, img_info):
        self.preview_panel.set_image(img_info['path'])
    
    def _update_preview_settings(self):
        self.settings['text'] = self.text_entry.get()
        self.settings['font'] = self.font_combo.get()
        self.settings['font_size'] = int(self.font_size_slider.get())
        self.settings['color'] = self.color_entry.get()
        self.settings['rotation'] = int(self.rotation_slider.get())
        self.settings['opacity'] = self.opacity_slider.get()
        self.settings['position'] = self.position_combo.get()
        self.settings['margin'] = int(self.margin_slider.get())
        self.settings['image_scale'] = self.scale_slider.get()
        self.settings['output_format'] = self.format_combo.get()
        self.settings['jpg_quality'] = int(self.quality_slider.get())
        self.settings['filename_rule'] = self.name_rule_combo.get()
        self.settings['custom_prefix'] = self.prefix_entry.get()
        self.settings['output_mode'] = self.output_mode_var.get()
        
        self.preview_panel.set_settings(self.settings)
    
    def _start_processing(self):
        selected = self.image_list.get_selected()
        if not selected:
            messagebox.showwarning('提示', '请先选择要处理的图片')
            return
        
        if self.settings['mode'] == 'image' and not self.settings.get('watermark_image'):
            messagebox.showwarning('提示', '请先选择水印图片')
            return
        
        self._update_preview_settings()
        
        self.start_btn.configure(state='disabled')
        self.processor.start(
            selected,
            self.settings,
            self._on_progress,
            self._on_finished
        )
    
    def _on_progress(self, current, total):
        self.after(0, lambda: self._update_progress(current, total))
    
    def _update_progress(self, current, total):
        self.progress.set(current / total)
        self.progress_label.configure(text=f'{current}/{total}')
        
        if current <= len(self.image_list.get_selected()):
            img = self.image_list.get_selected()[current - 1]
            self.image_list.update_image_status(img['path'], '处理中')
    
    def _on_finished(self, success, failed, failed_images):
        self.after(0, lambda: self._show_result(success, failed, failed_images))
    
    def _show_result(self, success, failed, failed_images):
        self.start_btn.configure(state='normal')
        
        selected = self.image_list.get_selected()
        for img in selected:
            is_failed = any(f[0] == img['path'] for f in failed_images)
            self.image_list.update_image_status(img['path'], '失败' if is_failed else '已完成')
        
        msg = f'处理完成！\n成功: {success} 张\n失败: {failed} 张'
        if failed > 0:
            msg += '\n\n失败列表:\n'
            for path, error in failed_images[:5]:
                msg += f'{path}: {error}\n'
            if len(failed_images) > 5:
                msg += '...'
        
        messagebox.showinfo('完成', msg)


def run():
    app = WatermarkApp()
    app.mainloop()

