import random
from States.AgentConsts import AgentConsts

class GoalMonitor:

    GOAL_COMMAND_CENTRER = 0
    GOAL_LIFE = 1
    GOAL_PLAYER = 2

    Distancia_agente_player=5
    def __init__(self, problem, goals):
        self.goals = goals
        self.problem = problem
        self.lastTime = -1
        self.recalculate = False

    def ForceToRecalculate(self):
        self.recalculate = True

    #determina si necesitamos replanificar
    def NeedReplaning(self, perception, map, agent):

        #TODO EN PRUEBAS definir la estrategia de cuando queremos recalcular
        #puede ser , por ejemplo cada cierto tiempo o cuanod tenemos poca vida.

        if self.recalculate:

            #distancia entre agente y jugador en X e Y
            per_A_J_X= abs(perception[AgentConsts.PLAYER_X]-perception[AgentConsts.AGENT_X])
            per_A_J_Y= abs(perception[AgentConsts.PLAYER_Y]-perception[AgentConsts.AGENT_Y])

            #distancia entre jugador y vida en X e Y
            per_J_H_X= abs(perception[AgentConsts.PLAYER_X]-perception[AgentConsts.LIFE_X])
            per_J_H_Y= abs(perception[AgentConsts.PLAYER_Y]-perception[AgentConsts.LIFE_Y])
            
            #distancia entre agente y vida en X e Y
            per_A_H_X= abs(perception[AgentConsts.AGENT_X]-perception[AgentConsts.LIFE_X])
            per_A_H_Y= abs(perception[AgentConsts.AGENT_Y]-perception[AgentConsts.LIFE_Y])

            #estamos en la misma columna o fila que player a distancia_agente_jugador, tenemos 2 de vida y/o no hay disponibles vidas extra
            if per_A_J_X ==0 or per_A_J_Y == 0 and
            per_A_J_X + per_A_J_Y <= self.Distancia_agente_player and 
            self.goals !=self.GOAL_PLAYER and 
            perception[AgentConsts.HEALTH]>=2 or perception[AgentConsts.LIFE_X] + perception[AgentConsts.LIFE_Y]<0:
                self.lastTime = perception[AgentConsts.TIME]
                return True
            
            #estamos mas cerca que player de la vida o tenemos solo 1 vida (priorizamos conseguir más vidas)
            elif per_A_H_X + per_A_H_Y < per_J_H_X+ per_J_H_Y or
            (perception[AgentConsts.HEALTH]<2 and 
            perception[AgentConsts.LIFE_X] + perception[AgentConsts.LIFE_Y]>0) 
            and self.goals !=self.GOAL_LIFE:
                self.lastTime = perception[AgentConsts.TIME]
                return True
            
            #no hay peligros asique nos vamos a por command center
            elif self.goals !=self.GOAL_COMMAND_CENTRER:
                self.lastTime = perception[AgentConsts.TIME]
                return True
            else:
                return False

            ##self.lastTime = perception[AgentConsts.TIME]
            ##return True
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

        #si estamos a menos de Distancia_agente_player seteamos la meta a jugador
        if per_A_J_X+per_A_J_Y<=self.Distancia_agente_player:
            return self.goals[self.GOAL_PLAYER]
        #estamos mas cerca de la vida que el jugador (vamos a robarsela muajajaja)
        if per_J_H_X+per_J_H_Y>per_A_H_X+per_A_H_Y and perception[AgentConsts.LIFE_Y] + perception[AgentConsts.LIFE_X]>=0:  
            return self.goals[self.GOAL_LIFE]
        #por defecto queremos romper command center
        return self.goals[self.GOAL_COMMAND_CENTRER]
    
    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal
