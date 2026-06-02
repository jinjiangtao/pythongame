import sounddevice as sd
import soundfile as sf
import threading
import queue
import time
import os
import json


class AudioCapturer:
    def __init__(self, settings_path="settings.json"):
        self.settings_path = settings_path
        self.load_settings()
        
        self.is_recording = False
        self.is_paused = False
        
        self.audio_queue = queue.Queue(maxsize=100)
        self.recording_thread = None
        
        self.audio_path = ""
        
        self.CHANNELS = 2
        self.RATE = 44100
        self.CHUNK = 1024
    
    def load_settings(self):
        if os.path.exists(self.settings_path):
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                self.settings = json.load(f)
        else:
            self.settings = {
                'record_microphone': True,
                'record_system_audio': False,
                'save_path': ''
            }
        
        self.record_microphone = self.settings.get('record_microphone', True)
        self.record_system_audio = self.settings.get('record_system_audio', False)
    
    def audio_recording_loop(self):
        def callback(indata, frames, time_info, status):
            if self.is_recording and not self.is_paused:
                if not self.audio_queue.full():
                    self.audio_queue.put(indata.copy())
        
        with sd.InputStream(samplerate=self.RATE, channels=self.CHANNELS, 
                           blocksize=self.CHUNK, callback=callback):
            while self.is_recording:
                time.sleep(0.01)
    
    def audio_writing_loop(self):
        with sf.SoundFile(self.audio_path, mode='w', samplerate=self.RATE, 
                         channels=self.CHANNELS, format='WAV') as f:
            while self.is_recording or not self.audio_queue.empty():
                try:
                    data = self.audio_queue.get(timeout=1)
                    if not self.is_paused:
                        f.write(data)
                    self.audio_queue.task_done()
                except queue.Empty:
                    continue
    
    def start_recording(self, audio_path=None):
        if not self.record_microphone:
            return
        
        if self.is_recording:
            return
        
        self.is_recording = True
        self.is_paused = False
        
        if audio_path:
            self.audio_path = audio_path
        else:
            self.audio_path = os.path.join(
                self.settings.get('save_path', os.path.expanduser('~')),
                "recording_audio.wav"
            )
        
        self.recording_thread = threading.Thread(target=self.audio_recording_loop)
        self.writing_thread = threading.Thread(target=self.audio_writing_loop)
        
        self.recording_thread.start()
        self.writing_thread.start()
    
    def pause_recording(self):
        self.is_paused = True
    
    def resume_recording(self):
        self.is_paused = False
    
    def stop_recording(self):
        if not self.record_microphone:
            return ""
        
        self.is_recording = False
        
        if self.recording_thread:
            self.recording_thread.join()
        if hasattr(self, 'writing_thread') and self.writing_thread:
            self.writing_thread.join()
        
        return self.audio_path
    
    def close(self):
        if self.is_recording:
            self.stop_recording()