from BaseAgent import BaseAgent
from StateMachine.StateMachine import StateMachine
from States.ExecutePlan import ExecutePlan
from GoalMonitor import GoalMonitor
from AStar.AStar import AStar
from MyProblem.BCNode import BCNode
from MyProblem.BCProblem import BCProblem
from States.AgentConsts import AgentConsts
from States.Attack import Attack

#implementación de un agente básico basado en objetivos.
#disponemos de la clase GoalMonitor que nos monitorea y replanifica cad cierto tiempo
#o cuando se establezca una serie de condiciones.
class GoalOrientedAgent(BaseAgent):
    def __init__(self, id, name):
        super().__init__(id, name)
        dictionary = {
        "ExecutePlan" : ExecutePlan("ExecutePlan"),
        "Attack" : Attack("Attack")
        }
        
        self.stateMachine = StateMachine("GoalOrientedBehavior",dictionary,"ExecutePlan")
        self.problem = None
        self.aStar = None
        self.plan = None
        self.goalMonitor = None
        self.agentInit = False

    #Metodo que se llama al iniciar el agente. No devuelve nada y sirve para contruir el agente
    def Start(self):
        if(AgentConsts.VERVOSE_MODE>=0):
            print("Inicio del agente ")
        self.stateMachine.Start(self)
        self.problem = None
        self.aStar = None
        self.plan = None
        self.goalMonitor = None
        self.agentInit = False

    #Metodo que se llama en cada actualización del agente, y se proporciona le vector de percepciones
    #Devuelve la acción u el disparo si o no
    def Update(self, perception, map):
        
        if perception == True or perception == False:
            return 0,True
       
        #inicializamos el agente (no lo podemos hacer en el start porque no tenemos el mapa)
       
        if not self.agentInit:
            self.InitAgent(perception, map)
            self.agentInit = True
 
        #le damos update a la máquina de estados.
        
        action, shot = self.stateMachine.Update(perception, map, self)

        #Actualizamos el plan refrescando la posición del player (meta 2), las demás en principio no se actualizan

        goal3Player = self._CreatePlayerGoal(perception)
        self.goalMonitor.UpdateGoals(goal3Player,2)


        if self.goalMonitor.NeedReplaning(perception,map,self):
            #self.problem.InitMap(map) ## refrescamos el mapa
            self.plan=self._CreatePlan(perception, map)
        return action, shot
    
    #método interno que encapsula la creació nde un plan
    def _CreatePlan(self, perception, map):
        if(AgentConsts.VERVOSE_MODE>=0):
            print("Estoy creando un plan")
        # 1) refrescar el mapa en el problema
        self.problem.InitMap(map)

        # 2) seleccionar la meta más adecuada
        #    firma: SelectGoal(perception, map, agent)
        new_goal = self.goalMonitor.SelectGoal(perception, map, self)
        self.problem.SetGoal(new_goal)

        # 3) construir y fijar el nodo inicial
        initial_node = self._CreateInitialNode(perception)
        self.problem.SetInitial(initial_node)

        # 4) lanzar un A* fresco sobre el problema
        self.aStar = AStar(self.problem)
        plan = self.aStar.GetPlan() or []   # siempre lista

        if(AgentConsts.VERVOSE_MODE>=3):
            print(f"Plan de longitud {len(plan)}")
        return plan
        '''
        #currentGoal = self.problem.GetGoal()
        if self.goalMonitor != None:
            # TODO creamos un plan, pasos:
            # -con gualMonito, seleccionamos la meta actual (Que será la mas propicia => definir la estrategia a seguir).
            # -le damos el modo inicial _CreateInitialNode
            # -establecer la meta actual al problema para que A* sepa cual es.
            # -Calcular el plan usando A*
            print("TODO aqui faltan cosas :)")
            
            
            nodoInicialX, nodoInicialY = perception[AgentConsts.AGENT_X],perception[AgentConsts.AGENT_Y]
            currentPlan = self.goalMonitor.SelectGoal()
            nodoMetaX, nodoMetaY = currentPlan.x, currentPlan.y
            self.problem.initial.x, self.problem.initial.y = nodoInicialX, nodoInicialY
            self.problem.goal.x, self.problem.goal.y = nodoMetaX, nodoMetaY
            
            # Atención // Esto necesita revisión
            if self.problem.goal.monitor != None:
                self.problem.goal.monitor = self.goalMonitor
        return self.aStar.GetPlan()
        
        '''
        
    @staticmethod
    def CreateNodeByPerception(perception, value, perceptionID_X, perceptionID_Y,ySize):
        xMap, yMap = BCProblem.WorldToMapCoord(perception[perceptionID_X],perception[perceptionID_Y],ySize)
        newNode = BCNode(None,BCProblem.GetCost(value),value,xMap,yMap)
        return newNode

    def _CreatePlayerGoal(self, perception):
        return GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.PLAYER,AgentConsts.PLAYER_X,AgentConsts.PLAYER_Y,15)

    
    def _CreateLifeGoal(self, perception):
        return GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.LIFE,AgentConsts.LIFE_X,AgentConsts.LIFE_Y,15)
    
    def _CreateInitialNode(self, perception):
        node = GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.NOTHING,AgentConsts.AGENT_X,AgentConsts.AGENT_Y,15)
        node.SetG(0)
        return node
    
    def _CreateDefaultGoal(self, perception):
        return GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.COMMAND_CENTER,AgentConsts.COMMAND_CENTER_X,AgentConsts.COMMAND_CENTER_Y,15)
    
    #no podemos iniciarlo en el start porque no conocemos el mapa ni las posiciones de los objetos
    def InitAgent(self,perception,map):
        #creamos el problema
        # - creamos el problema con BCProblem
        # - inicializamos el mapa problem.InitMap
        # - inicializamos A*
        # - creamos un plan inicial
        if(AgentConsts.VERVOSE_MODE>=0):
            print("Init Goal Oriented Agent")
        #Creamos el nodo inicial a partir de la percepción actual
        initialNode = self._CreateInitialNode(perception)
        #Creamos la meta por defecto (Command center) como el objetivo inicial 
        goal1CommanCenter = self._CreateDefaultGoal(perception)
        #Creamos el problema asociado, el entorno de BatlleCity
        xSize, ySize = 15, 15
        self.problem = BCProblem(initialNode, goal1CommanCenter, xSize, ySize)
        #Inicializamos el mapa con los datos recibidos
        self.problem.InitMap(map)
        if(AgentConsts.VERVOSE_MODE>=0):
            print("Mapa cargado")
        #Inicializamos el A* con el problema creado
        self.aStar = AStar(self.problem)
        
        # Generamos objetivos adicionales
        goal2Life = self._CreateLifeGoal(perception)
        goal3Player = self._CreatePlayerGoal(perception)
        self.goalMonitor = GoalMonitor(self.problem, [goal1CommanCenter, goal2Life, goal3Player])
        #Creamos un par inicial a partir de pa percepción y el mapa
        self.plan = self._CreatePlan(perception, map)
        if(AgentConsts.VERVOSE_MODE>=0):
            print("Plan inicial generado")
        GoalOrientedAgent.ShowPlan(self.plan)
        self.agentInit = True

    #muestra un plan por consola
    @staticmethod
    def ShowPlan(plan):
        for n in plan:
            if(AgentConsts.VERVOSE_MODE>=0):
                print("X: ",n.x,"Y:",n.y,"[",n.value,"]{",n.G(),"} => ")

    def GetPlan(self):
        return self.plan
    
    #Metodo que se llama al finalizar el agente, se pasa el estado de terminacion
    def End(self, win):
        super().End(win)
        self.stateMachine.End()