from abc import ABC, abstractmethod

class IState(ABC):
    @abstractmethod
    def getColor(self):
        pass