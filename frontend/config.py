from dataclasses import dataclass
import os

@dataclass
class Config:
    API_BASE_URL: str
    API_TIMEOUT_SECONDS: int = 5

    @staticmethod
    def from_env():
        base = os.getenv("API_BASE_URL", "http://localhost:8000")
        timeout = int(os.getenv("API_TIMEOUT_SECONDS", "5"))
        return Config(API_BASE_URL=base, API_TIMEOUT_SECONDS=timeout)
