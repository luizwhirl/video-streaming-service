# observer.py

from abc import ABC, abstractmethod

class Subject(ABC):
    """
    A interface do Sujeito (Observável) declara um conjunto de métodos para
    gerenciar assinantes (observadores).
    """
    def __init__(self):
        self._observers = []

    def attach(self, observer: 'Observer') -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: 'Observer') -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        """
        Dispara uma atualização em cada assinante.
        """
        for observer in self._observers:
            observer.update(self)

class Observer(ABC):
    """
    A interface do Observador declara o método de atualização, usado pelos sujeitos.
    """
    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Recebe a atualização do sujeito.
        """
        pass