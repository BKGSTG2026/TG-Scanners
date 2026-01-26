from abc import ABC, abstractmethod
from typing import Callable


class MessageSource(ABC):
    @abstractmethod
    def start(self, handler: Callable[[str], None]) -> None:
        """
        Start producing messages and pass each message to the handler.
        """
        pass
