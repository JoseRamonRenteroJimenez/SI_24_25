from BaseAgent import BaseAgent

from State_Combat import State_Combat
from State_Exploration import State_Exploration

class ReactiveAgent(BaseAgent):
    def __init__(self, id, name):
        super().__init__(id, name)
    
    def Name(self):
        super().Name()
    
    def Id(self):
        super().Id()
        
    def Start(self):
        super().Start()
        self.state = State_Exploration(self)
        
    def End(self, win):
        return super().End(win)
    