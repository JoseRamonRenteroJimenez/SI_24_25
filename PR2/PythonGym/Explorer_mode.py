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
        
        if(perception[config.P_NEIGHBORHOOD_UP]==config.O_PLAYER or perception[config.P_NEIGHBORHOOD_UP]==config.O_SHELL or
            perception[config.P_NEIGHBORHOOD_LEFT]==config.O_PLAYER or perception[config.P_NEIGHBORHOOD_LEFT]==config.O_SHELL or
            perception[config.P_NEIGHBORHOOD_DOWN]==config.O_PLAYER or perception[config.P_NEIGHBORHOOD_DOWN]==config.O_SHELL or
            perception[config.P_NEIGHBORHOOD_RIGHT]==config.O_PLAYER or perception[config.P_NEIGHBORHOOD_RIGHT]==config.O_SHELL):
                return "Combat_mode"

        return self.id