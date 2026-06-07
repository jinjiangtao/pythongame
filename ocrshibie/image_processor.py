import cv2
import numpy as np
from PIL import Image


class ImageProcessor:
    def __init__(self):
        self.original_image = None
        self.processed_image = None
    
    def load_image(self, image_path):
        self.original_image = cv2.imread(image_path)
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()
        return self.original_image is not None
    
    def set_image(self, image):
        self.original_image = image
        self.processed_image = image.copy()
    
    def to_gray(self):
        if len(self.processed_image.shape) == 3:
            self.processed_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        return self.processed_image
    
    def to_binary(self, threshold=127):
        if len(self.processed_image.shape) == 3:
            gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = self.processed_image
        _, self.processed_image = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        return self.processed_image
    
    def denoise(self):
        if len(self.processed_image.shape) == 3:
            self.processed_image = cv2.fastNlMeansDenoisingColored(self.processed_image, None, 10, 10, 7, 21)
        else:
            self.processed_image = cv2.fastNlMeansDenoising(self.processed_image, None, 10, 7, 21)
        return self.processed_image
    
    def auto_rotate(self):
        try:
            if len(self.processed_image.shape) == 3:
                gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            else:
                gray = self.processed_image
            
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
            
            if lines is not None:
                angles = []
                for line in lines:
                    rho, theta = line[0]
                    angle = np.rad2deg(theta) - 90
                    angles.append(angle)
                
                if angles:
                    median_angle = np.median(angles)
                    if abs(median_angle) > 1:
                        (h, w) = self.processed_image.shape[:2]
                        center = (w // 2, h // 2)
                        M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
                        self.processed_image = cv2.warpAffine(
                            self.processed_image, M, (w, h),
                            flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
                        )
        except Exception as e:
            print(f"自动旋转失败: {e}")
        
        return self.processed_image
    
    def adjust_brightness_contrast(self, brightness=0, contrast=0):
        alpha = 1 + contrast / 100.0
        beta = brightness
        
        self.processed_image = cv2.convertScaleAbs(self.processed_image, alpha=alpha, beta=beta)
        return self.processed_image
    
    def reset(self):
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()
        return self.processed_image
    
    def get_processed_image(self):
        return self.processed_image
    
    def get_original_image(self):
        return self.original_image
    
    def to_pil(self, image=None):
        if image is None:
            image = self.processed_image
        
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            return Image.fromarray(image)
        else:
            return Image.fromarray(image)
