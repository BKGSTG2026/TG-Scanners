"""
Collect messages either by mocking them (running with --mode mock) or connecting to a TCP/IP connection (--mode server)
"""

import os
from tg_scanners.listener.tcp_listener import TCPListener
from tg_scanners.listener.mock_source import MockMessageSource
from tg_scanners.config.settings import (
    TCP_HOST_SCANNER1,
    TCP_SCANNER_PORT,
)

def build_message_source(mode: str):
    if mode == "mock":
        return MockMessageSource(
            messages=[
                "400180004000290E34004E201914DB92C00000000000",
                "900180004000290E34004E201914DB92C00000000000",
            ],
            # Update this interval to send more or fewer messages
            interval_seconds=1,
        )

    if mode == "server":
        return TCPListener(
            host=os.getenv("LISTEN_HOST", "0.0.0.0"),
            port=int(os.getenv("LISTEN_PORT", "7000")),
        )   
