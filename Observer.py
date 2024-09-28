from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

class Subject(ABC):
    @abstractmethod
    def add_observer(self, observer: Observer):
        pass
    
    @abstractmethod
    def remove_observer(self, observer: Observer):
        pass
    
    @abstractmethod
    def notify_observers(self, message: str):
        pass
