import pygame
import numpy as np

from State import IState, Healthy, Resistant, NoSymptoms, Symptoms 
from Vector import Vector2D
from CareTaker import Memento

class Dot(pygame.sprite.Sprite):
    status: IState
    def __init__(self, status, width, height, x, y, velocity=Vector2D(0,0), speedScale = 1,\
                 nextToSymptoms=0, nextToNoSymptoms=0,myRecovery=0):
        self.colors = {"black": (0,0,0), "white":(255,255,255), "blue": (0,100,255), "red": (255,0,0), "yellow": (204, 204, 0), "green": (0, 153, 51)}
        super().__init__()

        self.radius = 5
        self.status = status
        self.color = self.status.getColor()
        self.image = pygame.Surface([self.radius * 2, self.radius * 2], pygame.SRCALPHA)

        pygame.draw.circle(self.image, self.colors[self.color], (self.radius, self.radius), self.radius)

        self.rect = self.image.get_rect()
        self.pos = Vector2D(x,y)
        self.vel = velocity
        self.WIDTH = width
        self.HEIGHT = height
        self.speedScale = speedScale
        self.nextToSymptoms = nextToSymptoms
        self.nextToNoSymptoms = nextToNoSymptoms
        self.recoveryTime = (np.random.randint(10) + 20)*25
        self.myRecovery = myRecovery

    def isNextTo(self, other):
        distance_px = self.pos.distance(other.getPos())  # Odległość w pikselach
        distance_m = distance_px / self.speedScale  # Przelicz na metry
        return distance_m < 2


    def nearIll(self, other: 'Dot'):
        if isinstance(self.status, Healthy) and (isinstance(other.status, Symptoms) or isinstance(other.status, NoSymptoms)):
            if isinstance(other.status, Symptoms):
                self.nextToSymptoms += 1
            if isinstance(other.status, NoSymptoms):
                self.nextToNoSymptoms += 1
            return True
        
    def checkTime(self):
        if isinstance(self.status, Healthy) :
            if self.nextToSymptoms > 75:
                if np.random.random() < 0.5:
                    self.setStatus(Symptoms())
                    return
                else:
                    self.setStatus(NoSymptoms())
                    return
            elif self.nextToNoSymptoms > 75:
                if np.random.random() < 0.5:
                    if np.random.random() < 0.5:
                        self.setStatus(Symptoms())
                        return
                    else:
                        self.setStatus(NoSymptoms())
                        return
                else:
                    self.setStatus(Healthy())
                    self.nextToNoSymptoms = 0
    
    def checkRecovery(self):
        if isinstance(self.status, Symptoms) or isinstance(self.status, NoSymptoms):
            self.myRecovery += 1
        if self.recoveryTime <= self.myRecovery:
            self.setStatus(Resistant())


    def getPos(self):
        return self.pos
    def getStatus(self):
        return self.status
    def getNextToIll(self):
        return self.nextToIll
    
    def setStatus(self, status: IState):
        self.status = status
        self.color = self.status.getColor()
        self.updateColor()
    
    def setNextToIll(self, nextToIll):
        self.nextToIll = nextToIll

    def isNextTo(self):
        pass

    def updateColor(self):
        self.image = pygame.Surface([self.radius * 2, self.radius * 2], pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.colors[self.color], (self.radius, self.radius), self.radius)

    #def getVelocity(self):
        #vel = np.random.choice([x / 2 for x in range(-5, 6)])
        #vel = vel / np.linalg.norm(vel) * np.random.uniform(0, 2.5) * self.speedScale / 25

        #return vel

    def update(self):
        tempPos = self.pos + self.vel
        #self.pos += self.vel
        x,y = tempPos.getComponents()

        # warunki brzegów
        if x < 0 or x > self.WIDTH:
            if np.random.rand() < 0.5:  # 50% szans na opuszczenie obszaru
                self.kill()  # Usuwamy obiekt z grupy
            else:  # Odbicie się od ściany
                self.vel.setX(-self.vel.getX())  # Zmiana kierunku poziomego
                self.vel.setY((np.random.rand() - 0.5) * 5 ) # Losowy kierunek pionowy
                tempVel = self.vel.getComponents() / np.linalg.norm(self.vel.getComponents()) * np.random.uniform(0, 2.5)  # Normalizacja prędkości
                self.vel.setX(tempVel[0])
                self.vel.setY(tempVel[1])

        if y < 0 or y > self.HEIGHT:
            if np.random.rand() < 0.5:  # 50% szans na opuszczenie obszaru
                self.kill()  # Usuwamy obiekt z grupy
            else:  # Odbicie się od ściany
                self.vel.setY(-self.vel.getY())  # Zmiana kierunku pionowego
                self.vel.setX((np.random.rand() - 0.5) * 5 )  # Losowy kierunek poziomy
                tempVel = self.vel.getComponents() / np.linalg.norm(self.vel.getComponents()) * np.random.uniform(0, 2.5)  # Normalizacja prędkości
                self.vel.setX(tempVel[0])
                self.vel.setY(tempVel[1])

        self.pos = tempPos

        self.rect.x = x
        self.rect.y = y


    def save(self):
        return Memento(
            status=self.status,
            WIDTH=self.WIDTH,
            HEIGHT=self.HEIGHT,
            posX=self.pos.getX(),  # Wywołanie metody
            posY=self.pos.getY(),  # Wywołanie metody
            vel=self.vel,  # `vel` przekazujemy jako obiekt Vector2D, `Memento` zajmie się konwersją na float
            speedScale=self.speedScale,
            nextToSymptoms=self.nextToSymptoms,
            nextToNoSymptoms=self.nextToNoSymptoms,
            myRecovery=self.myRecovery
        )
    