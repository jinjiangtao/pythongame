import json
import os
from typing import Dict, Any, List


class RequestConfig:
    def __init__(self):
        self.method: str = "GET"
        self.url: str = ""
        self.headers: Dict[str, str] = {}
        self.body_type: str = "none"
        self.body: Any = {}
        self.timeout: int = 30

    def to_dict(self) -> Dict[str, Any]:
        return {
            "method": self.method,
            "url": self.url,
            "headers": self.headers,
            "body_type": self.body_type,
            "body": self.body,
            "timeout": self.timeout
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RequestConfig':
        config = cls()
        config.method = data.get("method", "GET")
        config.url = data.get("url", "")
        config.headers = data.get("headers", {})
        config.body_type = data.get("body_type", "none")
        config.body = data.get("body", {})
        config.timeout = data.get("timeout", 30)
        return config


class ConfigManager:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        os.makedirs(config_dir, exist_ok=True)
        self.history_file = os.path.join(config_dir, "history.json")
        self.environments_file = os.path.join(config_dir, "environments.json")
        self.collections_file = os.path.join(config_dir, "collections.json")

    def save_request(self, config: RequestConfig, filename: str) -> bool:
        try:
            filepath = os.path.join(self.config_dir, f"{filename}.json")
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def load_request(self, filename: str) -> RequestConfig:
        try:
            filepath = os.path.join(self.config_dir, f"{filename}.json")
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return RequestConfig.from_dict(data)
        except Exception:
            return RequestConfig()

    def export_request(self, config: RequestConfig, filepath: str) -> bool:
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def import_request(self, filepath: str) -> RequestConfig:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return RequestConfig.from_dict(data)
        except Exception:
            return RequestConfig()

    def save_history(self, history: List[Dict[str, Any]]) -> bool:
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def load_history(self) -> List[Dict[str, Any]]:
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_environments(self, environments: Dict[str, Dict[str, str]]) -> bool:
        try:
            with open(self.environments_file, "w", encoding="utf-8") as f:
                json.dump(environments, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def load_environments(self) -> Dict[str, Dict[str, str]]:
        try:
            with open(self.environments_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def save_collections(self, collections: Dict[str, List[Dict[str, Any]]]) -> bool:
        try:
            with open(self.collections_file, "w", encoding="utf-8") as f:
                json.dump(collections, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def load_collections(self) -> Dict[str, List[Dict[str, Any]]]:
        try:
            with open(self.collections_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
