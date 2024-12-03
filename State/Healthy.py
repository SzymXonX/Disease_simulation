from .IState import IState

class Healthy(IState):
    def getColor(self):
        return "green"
    