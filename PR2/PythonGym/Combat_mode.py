from State import State
import config
from math import sqrt
class Combat_mode(State):

    def __init__(self, id):
        super().__init__(id)
        

    def Update(self, perception):
        print("-------Modo combat")


        disparo_disponible = perception[config.P_CAN_FIRE]==1
        
        disparar=False
        accion=-1

        if(disparo_disponible):
            self.dir_shot = -1

        print("-------Inicio mirando a ",self.facing_dir," y mi último disparo fue hacia ",self.dir_shot)

        direccion_peligro=-1
        dis_peligro=100

        for i in range (4):
            if(perception[i]==config.O_PLAYER or (perception[i]==config.O_SHELL and (disparo_disponible or (not disparo_disponible and i!=self.dir_shot)))):
                if(perception[i+4]<dis_peligro):
                    dis_peligro=perception[i+4]
                    direccion_peligro=i
        
        if(dis_peligro>-1 and direccion_peligro != self.facing_dir and disparo_disponible ):
            print("-------No posicionados")
            self.dir_shot=direccion_peligro
            self.facing_dir=direccion_peligro
            self.last_move=direccion_peligro+1
            print("-------Reposicionando a",direccion_peligro+1)
            accion=direccion_peligro
            disparar=True

        elif (dis_peligro>-1 and direccion_peligro == self.facing_dir and disparo_disponible):
            print("-------Bien posicionados")
            accion=-1
            disparar = True

        else:
            print("-------Modo huida")
            if(direccion_peligro%2 ==0):
                if(perception[(direccion_peligro+2)%4+4] >=2):
                    accion=(direccion_peligro+2)%4+1
                elif(perception[(direccion_peligro+3)%4+4]>=2):
                    accion=(direccion_peligro+3)%4+1
                else:
                    accion=((direccion_peligro+1)%4)
            else:
                if(perception[(direccion_peligro+1)%4+4] >=2):
                    accion=(direccion_peligro+1)%4+1
                elif(perception[(direccion_peligro+2)%4+4]>=2):
                    accion=(direccion_peligro+2)%4+1
                else:
                    accion=((direccion_peligro+3)%4)+1
            self.facing_dir=accion-1
            self.last_move=accion+1

        print("-------movemos a ",accion+1)

        self.CC_dist= sqrt((perception[config.P_AGENT_X] - perception[config.P_COMMAND_CENTER_X])**2 +(perception[config.P_AGENT_Y] - perception[config.P_COMMAND_CENTER_Y])**2)
        return accion+1,disparar
    
    def Transit(self,perception):
        
        if(perception[config.P_NEIGHBORHOOD_UP]==config.O_PLAYER or perception[config.P_NEIGHBORHOOD_UP]==config.O_SHELL or
            perception[config.P_NEIGHBORHOOD_LEFT]==config.O_PLAYER or perception[config.P_NEIGHBORHOOD_LEFT]==config.O_SHELL or
            perception[config.P_NEIGHBORHOOD_DOWN]==config.O_PLAYER or perception[config.P_NEIGHBORHOOD_DOWN]==config.O_SHELL or
            perception[config.P_NEIGHBORHOOD_RIGHT]==config.O_PLAYER or perception[config.P_NEIGHBORHOOD_RIGHT]==config.O_SHELL):
            return self.id
        
        return "Explorer_mode"