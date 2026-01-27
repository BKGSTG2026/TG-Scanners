"""
Contains the logic for capturing TCP IP messages
"""

import socket
from typing import Callable
from .base import MessageSource


class TCPListener(MessageSource):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
    
    def start(self):
        pass

    def listen(self):
        """
        Listen on a TCP socket and pass received messages to the handler.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.host, self.port))
            server.listen()

            print(f"Listening on {self.host}:{self.port}")

            while True:
                data = server.recv(1024)  # Receive data
                if data:
                    barcode = data.decode('utf-8').strip()
                    print(f"Scanned barcode: {barcode}")
