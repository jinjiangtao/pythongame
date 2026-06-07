import os
from utils import is_image_file, export_to_txt
from image_processor import ImageProcessor
from ocr_engine import OCREngine


class BatchProcessor:
    def __init__(self):
        self.ocr_engine = OCREngine()
        self.image_processor = ImageProcessor()
    
    def process_folder(self, folder_path, language="中英文混合", mode="精准模式", progress_callback=None):
        if not os.path.isdir(folder_path):
            return []
        
        image_files = []
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if is_image_file(filepath):
                image_files.append(filepath)
        
        results = []
        total = len(image_files)
        
        for i, image_path in enumerate(image_files):
            filename = os.path.basename(image_path)
            
            try:
                self.image_processor.load_image(image_path)
                pil_image = self.image_processor.to_pil()
                text = self.ocr_engine.recognize(pil_image, language, mode)
                
                txt_path = os.path.splitext(image_path)[0] + '.txt'
                export_to_txt(text, txt_path)
                
                results.append({
                    'image': filename,
                    'status': '成功',
                    'text': text
                })
            except Exception as e:
                results.append({
                    'image': filename,
                    'status': f'失败: {str(e)}',
                    'text': ''
                })
            
            if progress_callback:
                progress_callback(i + 1, total)
        
        return results
