import json

from CareTaker import Memento

class CareTaker:
    mementos : list[Memento]
    def __init__(self):
        self.mementos = []

    def saveMementos(self, dotList):
        self.mementos = []
        for dot in dotList:
            self.mementos.append(dot.save())

    def saveData(self):
        data = []
        for memento in self.mementos:
            data.append(memento.toDict())

        with open("simulationSave.json", "w") as file:
            json.dump(data, file, indent=4)

    def loadData(self):
        with open("simulationSave.json", "r") as file:
            data = json.load(file)
        return data