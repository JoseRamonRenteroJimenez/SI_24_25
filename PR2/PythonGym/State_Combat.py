from State import State

class State_Combat(State):
    def __init__(self, agent):
        super().__init__(agent)
    
class State_Advance(State_Combat):
    def __init__(self, agent):
        super().__init__(agent)

    def execute(self, perception):
        pass  # Este método se sobrescribirá en cada estado

class State_Advance_To_Enemy(State_Combat):
    def __init__(self, agent):
        super().__init__(agent)

    def execute(self, perception):
        pass  # Este método se sobrescribirá en cada estado

class State_Aim_Enemy(State_Combat):
    def __init__(self, agent):
        super().__init__(agent)

    def execute(self, perception):
        pass  # Este método se sobrescribirá en cada estado

class State_Identify_Best_Move(State_Combat):
    def __init__(self, agent):
        super().__init__(agent)

    def execute(self, perception):
        pass  # Este método se sobrescribirá en cada estado

class State_Identify_Nearest_Enemy(State_Combat):
    def __init__(self, agent):
        super().__init__(agent)

    def execute(self, perception):
        pass  # Este método se sobrescribirá en cada estado

class State_Shot_Enemy(State_Combat):
    def __init__(self, agent):
        super().__init__(agent)

    def execute(self, perception):
        pass  # Este método se sobrescribirá en cada estado