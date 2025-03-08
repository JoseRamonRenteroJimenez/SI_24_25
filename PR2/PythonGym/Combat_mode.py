from State import State
import config

class Combat_mode(State):
    
    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception):
        print("-------Modo combat")

        accion=0
        disparo=False

        direccion_peligro=-1
        dis_peligro=-1
        for i in range (config.P_NEIGHBORHOOD_UP,config.P_NEIGHBORHOOD_LEFT):
            if(perception[i]==config.O_PLAYER or perception[i]==config.O_SHELL):
                if(dis_peligro==-1 or perception[i+4]<dis_peligro):
                    dis_peligro=perception[i+4]
                    direccion_peligro=i
        
        print("-------Peligro mas cercano en ",direccion_peligro, "a distancia ",dis_peligro)

        if(dis_peligro!=-1):
            if(perception[config.P_CAN_FIRE]==1):
                accion=direccion_peligro
                disparo=True
            else:
                #hay sitio para quitarse de la trayectoria
                if(perception[(direccion_peligro+1)%4+4] >1):
                    accion=(direccion_peligro+1)%4
                elif(perception[(direccion_peligro+3)%4+4]>1):
                    accion=(direccion_peligro+3)%4
                else:
                    accion=(direccion_peligro+2)%4

        print("-------movemos a ",accion)
        print("--------------pos agente",perception[config.P_AGENT_Y],perception[config.P_AGENT_X])
        return accion+1,disparo
    
    def Transit(self,perception):
        


        if(perception[config.P_NEIGHBORHOOD_UP]==config.O_PLAYER or perception[config.P_NEIGHBORHOOD_UP]==config.O_SHELL or
            perception[config.P_NEIGHBORHOOD_LEFT]==config.O_PLAYER or perception[config.P_NEIGHBORHOOD_LEFT]==config.O_SHELL or
            perception[config.P_NEIGHBORHOOD_DOWN]==config.O_PLAYER or perception[config.P_NEIGHBORHOOD_DOWN]==config.O_SHELL or
            perception[config.P_NEIGHBORHOOD_RIGHT]==config.O_PLAYER or perception[config.P_NEIGHBORHOOD_RIGHT]==config.O_SHELL):
            return self.id
        
        return "Explorer_mode"