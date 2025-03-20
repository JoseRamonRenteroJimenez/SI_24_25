from State import State
import config
import random
from math import sqrt

class Explorer_mode(State):

    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception):
        disparo_disponible = perception[config.P_CAN_FIRE] == 1

        if disparo_disponible:
            self.dir_shot = -1

        print("-------Modo explorer")
        
        accion = 0
        disparo = False
        
        distancia_delante = perception[self.facing_dir + 4]
        mirando_delante = perception[self.facing_dir]

        newCC_dist = sqrt((perception[config.P_AGENT_X] - perception[config.P_COMMAND_CENTER_X])**2 + (perception[config.P_AGENT_Y] - perception[config.P_COMMAND_CENTER_Y])**2)
      
        if distancia_delante > config.C_EXPLO and mirando_delante != config.O_UNBREAKABLE:
            print("FM----- Free movement")
            accion = self.facing_dir + 1
            
            if self.CC_dist - newCC_dist < config.C_TOLERANCIA_MOVIMIENTO:
                if self.facing_dir % 2 == 0:
                    accion = (self.facing_dir + 1) % 4 + 1
                else:
                    accion = (self.facing_dir + 3) % 4 + 1
        else:
            if self.CC_dist > newCC_dist:
                print("KM----- Keep moving")
                accion = self.facing_dir + 1
            else:
                print("MA----- Movimiento aleatorio")
                if self.CC_dist - newCC_dist < config.C_TOLERANCIA_MOVIMIENTO:
                    if abs(perception[config.P_AGENT_X] - perception[config.P_COMMAND_CENTER_X]) < abs(config.C_EXPLO):
                        print("MRV----- Restringido Vertical")
                        accion = random.randint(0, 1) + 1
                    else:
                        if self.facing_dir % 2 == 0:
                            accion = (self.facing_dir + 1) % 4 + 1
                        else:
                            accion = (self.facing_dir + 3) % 4 + 1
                else:
                    if abs(perception[config.P_AGENT_X] - perception[config.P_COMMAND_CENTER_X]) < abs(config.C_EXPLO) and not(perception[self.facing_dir] == config.O_UNBREAKABLE and perception[self.facing_dir + 4] < 3):
                        print("MRV----- Restringido Vertical")
                        accion = random.randint(0, 1) + 1
                    else:
                        accion = random.randint(0, 4) + 1

        self.facing_dir = (accion + 3) % 4
        self.last_move = accion
        self.CC_dist = newCC_dist
        
        if (mirando_delante == config.O_BRICK or mirando_delante == config.O_COMMAND_CENTER) and distancia_delante <= 2:
            disparo = True
            self.dir_shot = accion
        
        return accion, disparo
    
    def Transit(self, perception):
        if (perception[config.P_NEIGHBORHOOD_UP] == config.O_PLAYER or perception[config.P_NEIGHBORHOOD_UP] == config.O_SHELL or
            perception[config.P_NEIGHBORHOOD_LEFT] == config.O_PLAYER or perception[config.P_NEIGHBORHOOD_LEFT] == config.O_SHELL or
            perception[config.P_NEIGHBORHOOD_DOWN] == config.O_PLAYER or perception[config.P_NEIGHBORHOOD_DOWN] == config.O_SHELL or
            perception[config.P_NEIGHBORHOOD_RIGHT] == config.O_PLAYER or perception[config.P_NEIGHBORHOOD_RIGHT] == config.O_SHELL):
                return "Combat_mode"

        return self.id
