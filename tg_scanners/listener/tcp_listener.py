import socket
from typing import Callable

from .base import MessageSource


class TCPListener(MessageSource):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def start(self, handler: Callable[[str], None]) -> None:
        """
        Listen on a TCP socket and pass received messages to the handler.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.host, self.port))
            server.listen()

            print(f"Listening on {self.host}:{self.port}")

            while True:
                conn, _ = server.accept()
                with conn:
                    data = conn.recv(4096)
                    if not data:
                        continue

                    m
