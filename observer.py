# observer.py

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

class Subject(ABC):

    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        try:
            self._observers.remove(observer)
        except ValueError:
            pass  

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

class Observer(ABC):
    @abstractmethod
    def update(self, subject: Subject) -> None:
        pass