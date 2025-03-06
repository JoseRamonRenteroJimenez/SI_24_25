from State import State

class State_Exploration(State):
    def __init__(self, agent):
        super().__init__(agent)

class State_Advance_To_Base(State_Exploration):
    def __init__(self, agent):
        super().__init__(agent)

    def execute(self, perception):
        pass  # Este método se sobrescribirá en cada estado

class State_Turn_Around(State_Exploration):
    def __init__(self, agent):
        super().__init__(agent)

    def execute(self, perception):
        pass  # Este método se sobrescribirá en cada estado
    
class State_Identify_Entity(State_Exploration):
    def __init__(self, agent):
        super().__init__(agent)

    def execute(self, perception):
        pass  # Este método se sobrescribirá en cada estado
    
class State_Demolition(State_Exploration):
    def __init__(self, agent):
        super().__init__(agent)

    def execute(self, perception):
        pass  # Este método se sobrescribirá en cada estado