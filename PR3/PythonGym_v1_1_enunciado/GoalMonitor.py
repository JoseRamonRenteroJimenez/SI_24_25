import random
from States.AgentConsts import AgentConsts

class GoalMonitor:

    GOAL_COMMAND_CENTRER = 0
    GOAL_LIFE = 1
    GOAL_PLAYER = 2
    
    def __init__(self, problem, goals):
        self.goals = goals
        self.problem = problem
        self.lastTime = -1
        self.recalculate = False
        self.vidaOut=False

    def ForceToRecalculate(self):
        self.recalculate = True

    #determina si necesitamos replanificar
    def NeedReplaning(self, perception, map, agent):

        #TODO EN PRUEBAS definir la estrategia de cuando queremos recalcular
        #puede ser , por ejemplo cada cierto tiempo o cuanod tenemos poca vida.

        #distancia entre agente y jugador en X e Y
        per_A_J_X= abs(perception[AgentConsts.PLAYER_X]-perception[AgentConsts.AGENT_X])
        per_A_J_Y= abs(perception[AgentConsts.PLAYER_Y]-perception[AgentConsts.AGENT_Y])

        #distancia entre jugador y vida en X e Y
        per_J_H_X= abs(perception[AgentConsts.PLAYER_X]-perception[AgentConsts.LIFE_X])
        per_J_H_Y= abs(perception[AgentConsts.PLAYER_Y]-perception[AgentConsts.LIFE_Y])
        
        #distancia entre agente y vida en X e Y
        per_A_H_X= abs(perception[AgentConsts.AGENT_X]-perception[AgentConsts.LIFE_X])
        per_A_H_Y= abs(perception[AgentConsts.AGENT_Y]-perception[AgentConsts.LIFE_Y])

        #distancia entre agente y command center
        per_A_CC_X= abs(perception[AgentConsts.AGENT_X]-perception[AgentConsts.COMMAND_CENTER_X])
        per_A_CC_Y= abs(perception[AgentConsts.AGENT_Y]-perception[AgentConsts.COMMAND_CENTER_Y])

        vidaTomada=perception[AgentConsts.LIFE_X] + perception[AgentConsts.LIFE_Y]<0
        # Estamos en la misma columna/ fila que jugador + 
        # a DISTANCIA_AGRESIVIDAD o menos +
        # teniendo 2 vidas o no hay vidas disponibles + 
        # el plan no es ya este mismo + 
        # estamos mas cerca de player que de command center
        plan_agente_jugador=(per_A_J_X ==0 or per_A_J_Y == 0) and per_A_J_X + per_A_J_Y <= AgentConsts.DISTANCIA_AGRESIVIDAD and self.goals !=self.GOAL_PLAYER and (perception[AgentConsts.HEALTH]>=2 or self.vidaOut) and (per_A_CC_X + per_A_CC_Y >per_A_J_X + per_A_J_Y)
        # Estamos más cerca que player de la vida o tenemos 1 vida (modo supervivencia ON) + 
        # hay disponible una vida extra + 
        # el plan no esta este mismo + 
        # no se ha seleccionado plan_agente_jugador +
        # estamos mas cerca de la vida que de command center
        plan_agente_vida=(per_A_H_X + per_A_H_Y < per_J_H_X+ per_J_H_Y or perception[AgentConsts.HEALTH]<2 ) and self.goals !=self.GOAL_LIFE and not plan_agente_jugador and (per_A_CC_X + per_A_CC_Y >per_A_H_X + per_A_H_Y)and not self.vidaOut
        # El plan no es ya este + 
        # no ha sido elegido el plan_agente_vida + 
        # no ha sido elegido el plan plan_agente_jugador
        plan_agente_command_center=self.goals != self.GOAL_COMMAND_CENTRER and not plan_agente_jugador and not plan_agente_vida

        if(AgentConsts.VERVOSE_MODE>=2):
            print("vida tomada ?",vidaTomada)
            print("meta = self.goal_life ?",plan_agente_vida)

        if(vidaTomada and not self.vidaOut):
            if(AgentConsts.VERVOSE_MODE>=2):
                print("--------------------Forzar recalculo por vida tomada--------------------")
            self.vidaOut=True
            self.recalculate=True

        if self.recalculate or (plan_agente_jugador or plan_agente_vida or plan_agente_command_center) and perception[AgentConsts.TIME]>=self.lastTime+AgentConsts.TIEMPOREPLANING:
            if(AgentConsts.VERVOSE_MODE>=2):
                print("plan_agente_jugador=",plan_agente_jugador,"plan_agente_vida=",plan_agente_vida,"plan_agente_command_center",plan_agente_command_center)

            self.lastTime = perception[AgentConsts.TIME]
            self.recalculate=False
            return True

        return False
    
    #selecciona la meta mas adecuada al estado actual
    def SelectGoal(self, perception, map, agent):
        #TODO EN PRUEBAS definir la estrategia del cambio de meta

        #distancia entre agente y jugador en X e Y
        per_A_J_X= abs(perception[AgentConsts.PLAYER_X]-perception[AgentConsts.AGENT_X])
        per_A_J_Y= abs(perception[AgentConsts.PLAYER_Y]-perception[AgentConsts.AGENT_Y])

        #distancia entre jugador y vida en X e Y
        per_J_H_X= abs(perception[AgentConsts.PLAYER_X]-perception[AgentConsts.LIFE_X])
        per_J_H_Y= abs(perception[AgentConsts.PLAYER_Y]-perception[AgentConsts.LIFE_Y])

        #distancia entre agente y vida en X e Y
        per_A_H_X= abs(perception[AgentConsts.AGENT_X]-perception[AgentConsts.LIFE_X])
        per_A_H_Y= abs(perception[AgentConsts.AGENT_Y]-perception[AgentConsts.LIFE_Y])

        #si estamos a menos de DISTANCIA_AGRESIVIDAD seteamos la meta a jugador
        if per_A_J_X+per_A_J_Y<=AgentConsts.DISTANCIA_AGRESIVIDAD and self.goals:
            if(AgentConsts.VERVOSE_MODE>=2):
                print("\n----------Plan de player seleccionado----------\n")
            return self.goals[self.GOAL_PLAYER]
        #estamos mas cerca de la vida que el jugador (vamos a robarsela muajajaja)
        if per_J_H_X+per_J_H_Y>per_A_H_X+per_A_H_Y and perception[AgentConsts.LIFE_Y] + perception[AgentConsts.LIFE_X]>=0:
            if(AgentConsts.VERVOSE_MODE>=2):
                print("\n----------Plan de vida seleccionado----------\n")  
            return self.goals[self.GOAL_LIFE]
        #por defecto queremos romper command center
        if(AgentConsts.VERVOSE_MODE>=2):
            print("\n----------Plan de Command Center seleccionado----------\n")
        return self.goals[self.GOAL_COMMAND_CENTRER]
    
    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal
