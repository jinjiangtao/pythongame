
import customtkinter as ctk
from watermark import create_text_watermark, create_image_watermark, apply_watermark
from utils import load_image, image_to_tk


class PreviewPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.current_image = None
        self.settings = None
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.original_label = ctk.CTkLabel(self, text='原图')
        self.original_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.result_label = ctk.CTkLabel(self, text='效果')
        self.result_label.grid(row=0, column=1, padx=5, pady=5)
        
        self.original_canvas = ctk.CTkLabel(self, text='请选择图片预览', width=200, height=200)
        self.original_canvas.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        
        self.result_canvas = ctk.CTkLabel(self, text='请选择图片预览', width=200, height=200)
        self.result_canvas.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
    
    def set_image(self, image_path):
        self.current_image = image_path
        self.update_preview()
    
    def set_settings(self, settings):
        self.settings = settings
        self.update_preview()
    
    def update_preview(self):
        if not self.current_image or not self.settings:
            return
        
        try:
            base_img = load_image(self.current_image, (300, 300))
            if not base_img:
                return
            
            orig_display = base_img.copy()
            orig_display.thumbnail((280, 280))
            self.orig_tk = image_to_tk(orig_display)
            self.original_canvas.configure(image=self.orig_tk, text='')
            
            if self.settings['mode'] == 'text':
                wm_img = create_text_watermark(
                    self.settings['text'],
                    self.settings['font'],
                    self.settings['font_size'],
                    self.settings['color'],
                    self.settings['opacity'],
                    self.settings['rotation']
                )
            else:
                if self.settings.get('watermark_image'):
                    wm_img = create_image_watermark(
                        self.settings['watermark_image'],
                        self.settings['image_scale'],
                        self.settings['opacity']
                    )
                else:
                    wm_img = None
            
            if wm_img:
                result = apply_watermark(base_img, wm_img, self.settings['position'], self.settings['margin'])
                result.thumbnail((280, 280))
                self.result_tk = image_to_tk(result)
                self.result_canvas.configure(image=self.result_tk, text='')
            else:
                self.result_canvas.configure(image='', text='请选择水印图片')
        
        except Exception as e:
            print(f'预览更新失败: {e}')
            self.result_canvas.configure(image='', text=f'预览失败: {str(e)}')
