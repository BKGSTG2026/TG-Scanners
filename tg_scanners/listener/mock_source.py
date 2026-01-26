import time
from typing import Callable
from .base import MessageSource

class MockMessageSource(MessageSource):
    def __init__(self, messages=None, interval_seconds: float = 1.0):
        self.interval = interval_seconds
        self.messages = messages or []

    def start(self, handler: Callable[[str], None]) -> None:
        test_messages = [
            "400180004000290E34004E201914DB92C00000000000",
        ]

        for message in test_messages:
            print(f"Mock sending message: {message}")  # add this line
            handler(message)
            time.sleep(self.interval)
