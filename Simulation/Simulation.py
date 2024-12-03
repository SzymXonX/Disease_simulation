import pygame
import numpy as np
from Dot import Dot
from Vector import Vector2D
from State import IState, Healthy, Resistant, NoSymptoms, Symptoms 
from CareTaker import CareTaker

class Simulation:

    def __init__(self, mWidth=20, mHeight=20, N=100, resistantFlag = True):
        self.colors = {"black": (0,0,0), "white":(255,255,255), "blue": (0,100,255)}
        self.FPS = 25
        self.width = 600
        self.height = 600
        self.resistantFlag = resistantFlag
        self.N = N
        self.all_container = pygame.sprite.Group()
        self.speedScale = min(self.width / mWidth, self.height / mHeight)
        self.running = True
        self.addButtons()

        self.addStartDots()

        self.start()


    def addButtons(self):
        self.buttonColor = (0, 128, 255)
        self.buttonHoverColor = (0, 200, 255)
        self.buttonTextColor = (0, 0, 0)
        self.buttons = {
            "Zapisz": pygame.Rect(50, 650, 150, 40),
            "Wczytaj": pygame.Rect(250, 650, 150, 40),
        }

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode([self.width, self.height+100])
        clock = pygame.time.Clock()

        while self.running:
            self.handle_events()
            
            if len(self.all_container) < self.N:
                for i in range(self.N - len(self.all_container)):
                    self.addDot()
                    
            for dot1 in self.all_container:
                for dot2 in self.all_container:
                    if dot1 == dot2:
                        continue
                    if self.inDistance(dot1.getPos(), dot2.getPos()):
                        if dot1.nearIll(dot2):
                            break
                dot1.checkTime()
                dot1.checkRecovery()

            self.all_container.update()
            self.screen.fill(self.colors["white"])
            self.draw()
            self.all_container.draw(self.screen)
            pygame.display.flip()
            clock.tick(self.FPS)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_button_click(event.pos)

    def handle_button_click(self, mousePos):
        for label, rect in self.buttons.items():
            if rect.collidepoint(mousePos):
                if label == "Zapisz":
                    self.zapiszButton()
                elif label == "Wczytaj":
                    self.wczytajButton()

    def zapiszButton(self):
        cTaker = CareTaker()
        cTaker.saveMementos(self.all_container)
        cTaker.saveData()
        

    def wczytajButton(self):
        cTaker = CareTaker()
        cTaker.loadData()
        for dot in self.all_container:
            dot.kill()
        self.all_container.empty()
        loadedDots = cTaker.loadData()
        for data in loadedDots:
            if data["status"] == "Healthy":
                status = Healthy()
            elif data["status"] == "Symptoms":
                status = Symptoms()
            elif data["status"] == "NoSymptoms":
                status = NoSymptoms()
            elif data["status"] == "Resistant":
                status = Resistant()

            vel = Vector2D(data["velX"], data["velY"])
            self.all_container.add(Dot(
                status=status,
                width=data["WIDTH"],
                height=data["HEIGHT"],
                x=data["posX"],
                y=data["posY"],
                velocity=vel,
                speedScale=data["speedScale"],
                nextToSymptoms=data["nextToSymptoms"],
                nextToNoSymptoms=data["nextToNoSymptoms"],
                myRecovery=data["myRecovery"]))
    
    
    def draw(self):
        self.screen.fill((255, 255, 255))  # Tło

        # Rysowanie przycisków
        for label, rect in self.buttons.items():
            color = self.buttonHoverColor if rect.collidepoint(pygame.mouse.get_pos()) else self.buttonColor
            pygame.draw.rect(self.screen, color, rect)
            self.draw_text(label, self.buttonTextColor, rect)


    def draw_text(self, text, color, rect):
        font = pygame.font.Font(None, 24)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
    
    def addStartDots(self):
        for i in range(self.N):
            x = np.random.randint(0, self.width+1)
            y = np.random.randint(0, self.height+1)

            if np.random.random() < 0.1:
                if np.random.random() < 0.5:
                    guy = Dot(Symptoms(),self.width, self.height, x, y, velocity=self.getVelocity(), speedScale=self.speedScale)
                else:
                    guy = Dot(NoSymptoms(),self.width, self.height, x, y, velocity=self.getVelocity(), speedScale=self.speedScale)
            else:
                guy = Dot(Healthy(),self.width, self.height, x, y, velocity=self.getVelocity(), speedScale=self.speedScale)
            self.all_container.add(guy)

    def addDot(self):
        side = np.random.choice(["top", "bottom", "left", "right"])

        if side == "top":
            x = np.random.randint(0, self.width + 1)
            y = 0 
        elif side == "bottom":
            x = np.random.randint(0, self.width + 1)
            y = self.height 
        elif side == "left":
            x = 0 
            y = np.random.randint(0, self.height + 1)
        elif side == "right":
            x = self.width 
            y = np.random.randint(0, self.height + 1)

        vel = self.getVelocity()

        if np.random.rand() < 0.1: #czy chory
            if np.random.rand() < 0.5: #czy objawy
                dot = Dot(Symptoms(),self.width, self.height, x, y, velocity=vel, speedScale=self.speedScale)
            else:
                dot = Dot(NoSymptoms(),self.width, self.height, x, y, velocity=vel, speedScale=self.speedScale)
        else:
            dot = Dot(Healthy(),self.width, self.height, x, y, velocity=vel, speedScale=self.speedScale)
        
        self.all_container.add(dot)
        
    def getVelocity(self):
        while True:
            vel_x = np.random.choice([x / 2 for x in range(-5, 6)])
            vel_y = np.random.choice([x / 2 for x in range(-5, 6)])
            vel = np.array([vel_x, vel_y])

            if np.linalg.norm(vel) > 0:
                break

        vel = vel / np.linalg.norm(vel) * np.random.uniform(1.0, 2.5) * self.speedScale / self.FPS

        return Vector2D(vel[0], vel[1])

    def inDistance(self, pos1: Vector2D, pos2: Vector2D) -> bool:
        distance_px = pos1.distance(pos2)  # Odległość w pikselach
        distance_m = distance_px / self.speedScale  # na metry
        return distance_m < 2

