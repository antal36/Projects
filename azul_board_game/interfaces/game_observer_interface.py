from __future__ import annotations
from abc import ABC, abstractmethod
from azul.observer import Observer


class GameObserverInterface(ABC):
    """Interface for observers of the game"""
    @abstractmethod
    def register_observer(self, observer: Observer) -> None:
        pass
    
    @abstractmethod
    def cancel_observer(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify_everybody(self, state: str) -> None:
        pass
    