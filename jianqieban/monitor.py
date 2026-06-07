import threading
import time
from utils import get_clipboard_content, get_current_time
from database import add_record
from settings import POLL_INTERVAL

class ClipboardMonitor(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.running = True
        self.last_content = ""
    
    def run(self):
        while self.running:
            try:
                current_content = get_clipboard_content()
                if current_content and current_content != self.last_content:
                    self.last_content = current_content
                    copy_time = get_current_time()
                    add_record(current_content, copy_time)
            except Exception as e:
                pass
            time.sleep(POLL_INTERVAL)
    
    def stop(self):
        self.running = False