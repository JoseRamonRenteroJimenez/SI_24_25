from State import State
import config

class Explorer_mode(State):

    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception):
        print("-------Modo explorer")
        
        accion=0
        disparo=False




        return accion,disparo
    
    def Transit(self,perception):
        
        for i in range (config.P_NEIGHBORHOOD_UP,config.P_NEIGHBORHOOD_LEFT):
            if(perception[i]==config.O_PLAYER or perception[i]==config.O_SHELL):
                return "Combat_mode"

        return self.id