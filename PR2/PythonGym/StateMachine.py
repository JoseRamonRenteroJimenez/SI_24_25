from State import State

class StateMachine(State):
    def __init__(self, id, states, initial):
        super().__init__(id)
        self.states = states
        self.curentState = initial
        self.states[self.curentState].facing_dir = -1
        self.states[self.curentState].dir_shot =-1
        self.states[self.curentState].last_move=0
        self.states[self.curentState].CC_dist=0
        
    
    #Metodo que se llama al iniciar la máquina de estado
    def Start(self):
        print("Inicio de la maquina de estados ")
        self.states[self.curentState].Start()

    #Metodo que se llama en cada actualización del estado
    #devuelve las acciones (actuadores) que el agente realiza
    def Update(self, perception):
        
        actions = self.states[self.curentState].Update(perception)
        newState=self.states[self.curentState].Transit(perception)

        if newState != self.curentState:
            #guardamos la info de a donde miramos y donde hemos disparado
            self.states[newState].facing_dir=self.states[self.curentState].facing_dir
            self.states[newState].dir_shot=self.states[self.curentState].dir_shot
            self.states[self.curentState].End()
            self.curentState=newState
            self.states[self.curentState].Start()
        return actions
    

    #Metodo que se llama al finalizar la máquina de estado
    #def End(self, win):
        #super().End(win)