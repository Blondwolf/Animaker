from abc import ABC, abstractmethod
class Element(ABC):
    @abstractmethod
    def center(self):
        pass