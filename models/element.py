from abc import ABCMeta, abstractmethod

class Element(object):
    ___metaclass__ = ABCMeta

    @abstractmethod
    def center(self):
        pass

    @abstractmethod
    def draw(self):
        pass
		
    @abstractmethod
    def add_move(self, x, y):
        pass
		
    @abstractmethod
    def add_rotate(self, alpha):
        pass
		
    @abstractmethod
    def translate(self):
        pass
		
    @abstractmethod
    def move(self):
        pass