from math import sqrt
from .IVector import IVector

class Vector2D(IVector):
    def __init__(self, x : float, y : float):
        self.x = x
        self.y = y
        
    def getComponents(self) -> list[float]:
        return [self.getX(), self.getY()]
    
    def abs(self) -> float:
        return sqrt(self.getX()**2 + self.getY()**2)
    
    def cdot(self, vect: 'Vector2D') -> float:
        return self.getX()*vect.getX() + self.getY()*vect.getY()
    
    def __add__(self, vect: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.getX() + vect.getX(), self.getY() + vect.getY())
    
    def distance(self, vect: 'Vector2D') -> float:
        return sqrt((self.getX() - vect.getX())**2 + (self.getY() - vect.getY())**2)

    def getX(self) -> float:
        return self.x
    
    def getY(self) -> float:
        return self.y
    
    def setX(self, x: float):
        self.x = x
        
    def setY(self, y: float):
        self.y = y