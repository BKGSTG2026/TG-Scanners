from tg_scanners.listener.tcp_listener import TCPListener
from tg_scanners.listener.mock_source import MockMessageSource
from tg_scanners.config.settings import (
    MESSAGE_SOURCE,
    LISTEN_HOST,
    LISTEN_PORT,
)

def build_message_source():
    if MESSAGE_SOURCE == "mock":
        return MockMessageSource(
            messages=[
                "400180004000290E34004E201914DB92C00000000000",
            ],
            interval_seconds=0.1,
        )

    return TCPListener(
        host=LISTEN_HOST,
        port=LISTEN_PORT,
    )
