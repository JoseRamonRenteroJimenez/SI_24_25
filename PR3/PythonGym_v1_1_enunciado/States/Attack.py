from StateMachine.State import State
from States.AgentConsts import AgentConsts

#Estado que nos permite atacar un objetivos desde la celda adyacente.
# se espera que el agente ya esté orientado
#agent.directionToLook es seteado por ExecutePlan para indicarnos cual es la dirección
#donde está el enemigo a atacar
class Attack(State):

    def __init__(self, id):
        super().__init__(id)
        self.directionToLook = -1

    def Update(self, perception, map, agent):
        #suponemos que miramos al objetivo
        self.directionToLook=agent.directionToLook


        dispara= False
        movimiento=0
        #si podemos atacamos
        if perception[AgentConsts.CAN_FIRE]:
            dispara=True
        
        # TODO ¿posible evasión? según mis observaciones funciona muy bien tal y como está 
        # sin un modo huida aún asi dejo la variable movimiento en caso de implementación para facil lectura
        
        return movimiento, dispara

    def Transit(self,perception, map):
        target = perception[self.directionToLook]
        #si mi target ya no está vuelvo a ExecutePlan
        if target != AgentConsts.PLAYER or target != AgentConsts.COMMAND_CENTER or  target != AgentConsts.SHELL:
            return "ExecutePlan"
        return self.id
    