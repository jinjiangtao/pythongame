import cv2
import numpy as np
import mss
import mss.tools
from PIL import Image, ImageDraw
import threading
import queue
import time
import os
import json
from pynput import mouse
from datetime import datetime


class ScreenRecorder:
    def __init__(self, settings_path="settings.json"):
        self.settings_path = settings_path
        self.load_settings()
        
        self.is_recording = False
        self.is_paused = False
        self.is_stopped = False
        
        self.sct = mss.mss()
        self.monitor = None
        self.record_area = None
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = None
        
        self.frame_queue = queue.Queue(maxsize=60)
        self.audio_queue = queue.Queue(maxsize=100)
        
        self.recording_thread = None
        self.writing_thread = None
        self.cursor_thread = None
        
        self.cursor_position = (0, 0)
        self.cursor_visible = True
        
        self.start_time = 0
        self.recorded_frames = 0
        
        self.video_path = ""
        
        self.cursor_listener = mouse.Listener(on_move=self.on_cursor_move)
        self.cursor_listener.start()
    
    def load_settings(self):
        if os.path.exists(self.settings_path):
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                self.settings = json.load(f)
        else:
            self.settings = {
                'fps': 30,
                'quality': 'high',
                'record_cursor': True,
                'record_microphone': True,
                'save_path': ''
            }
        
        self.fps = self.settings.get('fps', 30)
        self.quality = self.settings.get('quality', 'high')
        self.record_cursor = self.settings.get('record_cursor', True)
        
        quality_map = {'low': 500000, 'medium': 1500000, 'high': 3000000}
        self.bitrate = quality_map.get(self.quality, 3000000)
    
    def on_cursor_move(self, x, y):
        self.cursor_position = (x, y)
    
    def set_record_area(self, mode, area=None, window_handle=None):
        if mode == 'fullscreen':
            self.monitor = self.sct.monitors[1]
            self.record_area = (0, 0, self.monitor['width'], self.monitor['height'])
        elif mode == 'window':
            if window_handle:
                pass
            self.monitor = self.sct.monitors[1]
            if area:
                self.record_area = area
            else:
                self.record_area = (0, 0, self.monitor['width'], self.monitor['height'])
        elif mode == 'custom':
            if area:
                x, y, w, h = area
                self.record_area = (x, y, x + w, y + h)
                self.monitor = {'top': y, 'left': x, 'width': w, 'height': h}
            else:
                self.monitor = self.sct.monitors[1]
                self.record_area = (0, 0, self.monitor['width'], self.monitor['height'])
    
    def create_cursor_image(self, frame):
        if not self.record_cursor:
            return frame
        
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        
        x, y = self.cursor_position
        rx, ry = self.record_area[0], self.record_area[1]
        cx, cy = x - rx, y - ry
        
        frame_w, frame_h = frame.shape[1], frame.shape[0]
        
        if 0 <= cx < frame_w and 0 <= cy < frame_h:
            cursor_size = 20
            draw.ellipse([cx - cursor_size//2, cy - cursor_size//2,
                         cx + cursor_size//2, cy + cursor_size//2],
                        outline='red', width=2)
            draw.line([cx, cy - cursor_size//2 - 5, cx, cy + cursor_size//2 + 5],
                     fill='red', width=2)
            draw.line([cx - cursor_size//2 - 5, cy, cx + cursor_size//2 + 5, cy],
                     fill='red', width=2)
        
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    def capture_frame(self):
        try:
            sct_img = self.sct.grab(self.monitor)
            frame = np.array(sct_img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            return frame
        except Exception as e:
            print(f"Frame capture error: {e}")
            return None
    
    def recording_loop(self):
        frame_interval = 1.0 / self.fps
        last_time = time.time()
        
        while not self.is_stopped:
            if self.is_paused:
                time.sleep(0.01)
                continue
            
            current_time = time.time()
            elapsed = current_time - last_time
            
            if elapsed >= frame_interval:
                frame = self.capture_frame()
                if frame is not None:
                    frame = self.create_cursor_image(frame)
                    if not self.frame_queue.full():
                        self.frame_queue.put(frame)
                        self.recorded_frames += 1
                
                last_time = current_time
            
            time.sleep(0.001)
    
    def writing_loop(self):
        while not self.is_stopped or not self.frame_queue.empty():
            try:
                frame = self.frame_queue.get(timeout=1)
                if self.writer and not self.is_paused:
                    self.writer.write(frame)
                self.frame_queue.task_done()
            except queue.Empty:
                continue
    
    def start_recording(self, save_path=None):
        if self.is_recording:
            return
        
        self.is_recording = True
        self.is_paused = False
        self.is_stopped = False
        self.recorded_frames = 0
        self.start_time = time.time()
        
        if save_path:
            self.video_path = save_path
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            folder = self.settings.get('save_path', os.path.expanduser('~'))
            self.video_path = os.path.join(folder, f"recording_{timestamp}.mp4")
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        w, h = self.record_area[2] - self.record_area[0], self.record_area[3] - self.record_area[1]
        self.writer = cv2.VideoWriter(self.video_path, fourcc, self.fps, (w, h))
        
        self.recording_thread = threading.Thread(target=self.recording_loop)
        self.writing_thread = threading.Thread(target=self.writing_loop)
        
        self.recording_thread.start()
        self.writing_thread.start()
    
    def pause_recording(self):
        self.is_paused = True
    
    def resume_recording(self):
        self.is_paused = False
    
    def stop_recording(self):
        self.is_stopped = True
        
        if self.recording_thread:
            self.recording_thread.join()
        if self.writing_thread:
            self.writing_thread.join()
        
        if self.writer:
            self.writer.release()
            self.writer = None
        
        self.is_recording = False
        return self.video_path
    
    def get_recorded_duration(self):
        if not self.is_recording:
            return 0
        return int(time.time() - self.start_time)
    
    def get_frame_count(self):
        return self.recorded_frames
    
    def get_queue_size(self):
        return self.frame_queue.qsize()
    
    def close(self):
        if self.is_recording:
            self.stop_recording()
        self.cursor_listener.stop()
        self.sct.close()