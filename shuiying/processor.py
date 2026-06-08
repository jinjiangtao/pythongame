
import threading
import os
from queue import Queue
from watermark import process_image


class BatchProcessor:
    def __init__(self):
        self.queue = Queue()
        self.results = []
        self.running = False
        self.progress_callback = None
        self.finished_callback = None
        self.thread = None
    
    def start(self, image_list, settings, progress_callback, finished_callback):
        if self.running:
            return
        
        self.image_list = image_list
        self.settings = settings
        self.progress_callback = progress_callback
        self.finished_callback = finished_callback
        self.results = []
        self.running = True
        
        self.thread = threading.Thread(target=self._process_thread)
        self.thread.daemon = True
        self.thread.start()
    
    def _process_thread(self):
        total = len(self.image_list)
        success = 0
        failed = 0
        failed_images = []
        
        for i, img_info in enumerate(self.image_list):
            if not self.running:
                break
            
            input_path = img_info['path']
            try:
                output_path = self._get_output_path(input_path)
                process_image(input_path, output_path, self.settings)
                success += 1
                self.results.append((input_path, output_path, True, None))
            except Exception as e:
                failed += 1
                failed_images.append((input_path, str(e)))
                self.results.append((input_path, None, False, str(e)))
            
            if self.progress_callback:
                self.progress_callback(i + 1, total)
        
        self.running = False
        
        if self.finished_callback:
            self.finished_callback(success, failed, failed_images)
    
    def _get_output_path(self, input_path):
        dirname = os.path.dirname(input_path)
        basename = os.path.basename(input_path)
        name, ext = os.path.splitext(basename)
        
        if self.settings['filename_rule'] == '原文件名_watermarked':
            new_name = f'{name}_watermarked{ext}'
        else:
            new_name = f'{self.settings["custom_prefix"]}{basename}'
        
        if self.settings['output_mode'] == '新文件夹':
            output_dir = os.path.join(dirname, 'watermarked')
            os.makedirs(output_dir, exist_ok=True)
            return os.path.join(output_dir, new_name)
        else:
            return os.path.join(dirname, new_name)
    
    def stop(self):
        self.running = False
