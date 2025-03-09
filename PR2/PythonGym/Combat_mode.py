from State import State
import config

class Combat_mode(State):

    def __init__(self, id):
        super().__init__(id)
        

    def Update(self, perception):
        print("-------Modo combat")


        disparo_disponible = perception[config.P_CAN_FIRE]==1
        
        disparar=False
        # accion = nada
        accion=-1

        #si tenemos el disparo disponible ya no nos proporciona info el anterior 
        if(disparo_disponible):
            self.dir_shot = -1

        print("-------Inicio mirando a ",self.facing_dir," y mi último disparo fue hacia ",self.dir_shot)

        #no sabemos donde esta el peligro
        direccion_peligro=-1
        #ni su distancia
        dis_peligro=100

        for i in range (4):
            #miramos que sea jugador o bala que no sea nuestra (por que tenemos la nuestra o por que viene de otra direccion a la que no hemos disparado)
            if(perception[i]==config.O_PLAYER or (perception[i]==config.O_SHELL and (disparo_disponible or (not disparo_disponible and i!=self.dir_shot)))):
                if(perception[i+4]<dis_peligro):
                    #encontramos el peligro más cercano y su direcciónd
                    dis_peligro=perception[i+4]
                    direccion_peligro=i
        
        print("-------Peligro mas cercano en ",direccion_peligro+1, "a distancia ",dis_peligro)

        if(dis_peligro>-1 and direccion_peligro != self.facing_dir and disparo_disponible ):
            print("-------No posicionados")
            #nos posicionamos y disparamos
            self.dir_shot=direccion_peligro
            self.facing_dir=direccion_peligro
            print("-------Reposicionando a",direccion_peligro+1)
            accion=direccion_peligro
            disparar=True

        elif (dis_peligro>-1 and direccion_peligro == self.facing_dir and disparo_disponible):
            print("-------Bien posicionados")
            #queremos no hacer nada
            accion=-1
            disparar = True

        else:
            #hay sitio para quitarse de la trayectoria
            print("-------Modo huida")
            #caso amenaza arriba o amenaza derecha
            #por acciones de movimiento de tanque MOVE_UP = 1, MOVE_DOWN = 2, MOVE_RIGHT = 3,MOVE_LEFT = 4
            if(direccion_peligro%2 ==0):
                if(perception[(direccion_peligro+2)%4+4] >=2):
                    accion=(direccion_peligro+2)%4+1
                elif(perception[(direccion_peligro+3)%4+4]>=2):
                    accion=(direccion_peligro+3)%4+1
                else:
                    accion=((direccion_peligro+1)%4)
            #caso amenaza abajo o amenaza izquierda
            else:
                if(perception[(direccion_peligro+1)%4+4] >=2):
                    accion=(direccion_peligro+1)%4+1
                elif(perception[(direccion_peligro+2)%4+4]>=2):
                    accion=(direccion_peligro+2)%4+1
                else:
                    accion=((direccion_peligro+3)%4)+1
            self.facing_dir=accion

        print("-------movemos a ",accion+1)
        print("--------------pos agente",perception[config.P_AGENT_Y],perception[config.P_AGENT_X])
        return accion+1,disparar
    
    def Transit(self,perception):
        


        if(perception[config.P_NEIGHBORHOOD_UP]==config.O_PLAYER or perception[config.P_NEIGHBORHOOD_UP]==config.O_SHELL or
            perception[config.P_NEIGHBORHOOD_LEFT]==config.O_PLAYER or perception[config.P_NEIGHBORHOOD_LEFT]==config.O_SHELL or
            perception[config.P_NEIGHBORHOOD_DOWN]==config.O_PLAYER or perception[config.P_NEIGHBORHOOD_DOWN]==config.O_SHELL or
            perception[config.P_NEIGHBORHOOD_RIGHT]==config.O_PLAYER or perception[config.P_NEIGHBORHOOD_RIGHT]==config.O_SHELL):
            return self.id
        
        return "Explorer_mode"