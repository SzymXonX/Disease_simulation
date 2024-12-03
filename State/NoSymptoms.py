from .IState import IState

class NoSymptoms(IState):
    def getColor(self):
        return "yellow"
    