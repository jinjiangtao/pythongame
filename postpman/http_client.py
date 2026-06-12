import threading
import requests
import time
from typing import Dict, Any, Optional


class ResponseData:
    def __init__(self):
        self.status_code: int = 0
        self.headers: Dict[str, str] = {}
        self.body: str = ""
        self.response_time: float = 0
        self.error: str = ""
        self.success: bool = False


class HttpClient:
    def __init__(self):
        self.session = requests.Session()
        self.current_thread: Optional[threading.Thread] = None
        self.cancel_event = threading.Event()

    def cancel_request(self):
        self.cancel_event.set()

    def _send_request(self, method: str, url: str, headers: Dict[str, str], 
                      body: Any, body_type: str, timeout: int,
                      callback) -> None:
        response_data = ResponseData()
        start_time = time.time()
        
        try:
            if self.cancel_event.is_set():
                response_data.error = "Request cancelled"
                callback(response_data)
                return

            data = None
            files = None
            
            if body_type == "form-data":
                files = {}
                data = {}
                for key, value in body.items():
                    if isinstance(value, tuple):
                        files[key] = value
                    else:
                        data[key] = value
            elif body_type == "x-www-form-urlencoded":
                data = body
            elif body_type == "raw":
                data = body
            
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                files=files if files else None,
                json=body if body_type == "raw" and isinstance(body, dict) else None,
                timeout=timeout,
                stream=True
            )
            
            if self.cancel_event.is_set():
                response_data.error = "Request cancelled"
                callback(response_data)
                return

            response_data.status_code = response.status_code
            response_data.headers = dict(response.headers)
            
            try:
                response_data.body = response.json()
                response_data.body = str(response_data.body)
            except:
                response_data.body = response.text

        except requests.exceptions.RequestException as e:
            response_data.error = str(e)
        finally:
            response_data.response_time = time.time() - start_time
            response_data.success = not response_data.error
            callback(response_data)

    def send_request(self, method: str, url: str, headers: Dict[str, str] = None,
                     body: Any = None, body_type: str = "none", 
                     timeout: int = 30, callback=None) -> None:
        self.cancel_event.clear()
        headers = headers or {}
        body = body or {}
        
        self.current_thread = threading.Thread(
            target=self._send_request,
            args=(method, url, headers, body, body_type, timeout, callback),
            daemon=True
        )
        self.current_thread.start()
