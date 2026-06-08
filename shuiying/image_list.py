
import customtkinter as ctk
from PIL import Image
import os
from utils import load_image, image_to_tk


class ImageItem(ctk.CTkFrame):
    def __init__(self, master, image_info, on_select, on_preview, **kwargs):
        super().__init__(master, **kwargs)
        self.image_info = image_info
        self.on_select = on_select
        self.on_preview = on_preview
        self.selected = True
        
        self.grid_columnconfigure(1, weight=1)
        
        self.checkbox = ctk.CTkCheckBox(self, text='', command=self._on_check, width=20)
        self.checkbox.grid(row=0, column=0, padx=5, pady=5)
        self.checkbox.select()
        
        self.thumbnail_label = ctk.CTkLabel(self, text='', width=60, height=60)
        self.thumbnail_label.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        self.info_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.info_frame.grid(row=0, column=2, padx=5, pady=5, sticky='ew')
        
        self.name_label = ctk.CTkLabel(self.info_frame, text=os.path.basename(image_info['path']), anchor='w')
        self.name_label.pack(fill='x')
        
        size_text = f'{image_info["width"]} x {image_info["height"]}'
        self.size_label = ctk.CTkLabel(self.info_frame, text=size_text, anchor='w', font=('Arial', 10))
        self.size_label.pack(fill='x')
        
        self.status_label = ctk.CTkLabel(self, text='待处理', width=80)
        self.status_label.grid(row=0, column=3, padx=5, pady=5)
        
        self.preview_btn = ctk.CTkButton(self, text='预览', width=60, command=self._on_preview_click)
        self.preview_btn.grid(row=0, column=4, padx=5, pady=5)
        
        self._load_thumbnail()
    
    def _load_thumbnail(self):
        try:
            img = load_image(self.image_info['path'], (60, 60))
            if img:
                self.thumbnail = image_to_tk(img)
                self.thumbnail_label.configure(image=self.thumbnail)
        except Exception as e:
            pass
    
    def _on_check(self):
        self.selected = self.checkbox.get() == 1
        self.on_select(self.image_info, self.selected)
    
    def _on_preview_click(self):
        self.on_preview(self.image_info)
    
    def update_status(self, status):
        colors = {
            '待处理': ('gray', 'gray'),
            '处理中': ('blue', 'blue'),
            '已完成': ('green', 'green'),
            '失败': ('red', 'red')
        }
        self.status_label.configure(text=status)


class ImageList(ctk.CTkScrollableFrame):
    def __init__(self, master, on_preview, **kwargs):
        super().__init__(master, **kwargs)
        self.on_preview = on_preview
        self.images = []
        self.items = []
        self.selected_images = set()
    
    def add_images(self, image_files):
        for file_path in image_files:
            if any(img['path'] == file_path for img in self.images):
                continue
            
            try:
                img = Image.open(file_path)
                width, height = img.size
                img_info = {
                    'path': file_path,
                    'width': width,
                    'height': height,
                    'status': '待处理'
                }
                self.images.append(img_info)
                self.selected_images.add(file_path)
                
                item = ImageItem(
                    self,
                    img_info,
                    self._on_item_select,
                    self.on_preview
                )
                item.pack(fill='x', padx=5, pady=2)
                self.items.append(item)
            except Exception as e:
                print(f'无法加载图片 {file_path}: {e}')
    
    def _on_item_select(self, img_info, selected):
        if selected:
            self.selected_images.add(img_info['path'])
        else:
            self.selected_images.discard(img_info['path'])
    
    def get_selected(self):
        return [img for img in self.images if img['path'] in self.selected_images]
    
    def select_all(self):
        for item in self.items:
            item.checkbox.select()
            item.selected = True
            self.selected_images.add(item.image_info['path'])
    
    def deselect_all(self):
        for item in self.items:
            item.checkbox.deselect()
            item.selected = False
        self.selected_images.clear()
    
    def clear(self):
        for item in self.items:
            item.destroy()
        self.items.clear()
        self.images.clear()
        self.selected_images.clear()
    
    def update_image_status(self, path, status):
        for item in self.items:
            if item.image_info['path'] == path:
                item.update_status(status)
                break
