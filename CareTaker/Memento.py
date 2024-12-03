from State import IState
from Vector import Vector2D

class Memento:
    status: IState
    WIDTH = int
    HEIGHT = int
    posX = float
    posY = float
    velX = float
    velY = float
    speedScale = float
    nextToSymptoms = int
    nextToNoSymptoms = int
    myRecovery = int

    def __init__(self, status, WIDTH, HEIGHT, posX, posY, vel: Vector2D, speedScale,
             nextToSymptoms, nextToNoSymptoms, myRecovery):
        self.status = status
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.posX = posX
        self.posY = posY
        self.velX = vel.getX()
        self.velY = vel.getY()
        self.speedScale = speedScale
        self.nextToSymptoms = nextToSymptoms
        self.nextToNoSymptoms = nextToNoSymptoms
        self.myRecovery = myRecovery

    def toDict(self):
        return {
            "status": type(self.status).__name__, 
            "WIDTH": self.WIDTH,
            "HEIGHT": self.HEIGHT,
            "posX": self.posX,
            "posY": self.posY,
            "velX": self.velX,
            "velY": self.velY,
            "speedScale": self.speedScale,
            "nextToSymptoms": self.nextToSymptoms,
            "nextToNoSymptoms": self.nextToNoSymptoms,
            "myRecovery": self.myRecovery
        }