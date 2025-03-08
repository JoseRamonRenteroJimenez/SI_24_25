from BaseAgent import BaseAgent
from StateMachine import StateMachine

from Explorer_mode import Explorer_mode
from Combat_mode import Combat_mode


class ReactiveAgent(BaseAgent):
    def __init__(self, id, name):
        super().__init__(id, name)
        dictionary = {
        "Explorer_mode": Explorer_mode("Explorer_mode"),
        "Combat_mode": Combat_mode("Combat_mode")
        }
        self.stateMachine = StateMachine("ReactiveBehavior",dictionary,"Explorer_mode")

    #Metodo que se llama al iniciar el agente. No devuelve nada y sirve para contruir el agente
    def Start(self):
        print("Inicio del agente ")
        self.stateMachine.Start()

    #Metodo que se llama en cada actualización del agente, y se proporciona le vector de percepciones
    #Devuelve la acción u el disparo si o no
    def Update(self, perception):

        action, shot = self.stateMachine.Update(perception)

        return action, shot
    
    #Metodo que se llama al finalizar el agente, se pasa el estado de terminacion
    def End(self, win):
        super().End(win)
        self.stateMachine.End()