"""
Define the mock service that sends mock messages - just sends the messages defined 'forever'
"""


import time
from typing import Callable
from .base import MessageSource

class MockMessageSource(MessageSource):
    def __init__(self, messages=None, interval_seconds: float = 1.0):
        self.interval = interval_seconds
        self.messages = messages
    def start(self):
        pass

    def listen(self):
        while(True):
            for msg in self.messages:
                yield msg
                time.sleep(self.interval)
                print(f"Mock sending message: {msg}")  
