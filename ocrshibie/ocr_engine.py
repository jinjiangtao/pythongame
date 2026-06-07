import pytesseract
import platform
import os
from settings import LANGUAGES, MODES


class OCREngine:
    def __init__(self):
        self.tesseract_path = self._find_tesseract()
        if self.tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
    
    def _find_tesseract(self):
        if platform.system() == 'Windows':
            possible_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    return path
        return None
    
    def recognize(self, image, language="中英文混合", mode="精准模式"):
        try:
            lang_code = LANGUAGES.get(language, "chi_sim+eng")
            config = MODES.get(mode, "--oem 3 --psm 6")
            
            result = pytesseract.image_to_string(image, lang=lang_code, config=config)
            return result.strip()
        except Exception as e:
            print(f"OCR 识别失败: {e}")
            return ""
