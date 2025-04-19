from AStar.Node import Node

#Clase que implementa un nodo de BattleCity
#A parte de los datos por defecto, implementamos el método 
#IsEqual que nos ayudará a detectar cuando dos nosdos son iguales
class BCNode(Node):
    def __init__(self, parent, g, value, x, y):
        super().__init__(parent, g)
        self.value = value
        self.x = int(x)
        self.y = int(y)
    
    def IsEqual(self,node):
        if((self.x == node.x) and (self.y == node.y)):
            return True
        return False

    # Define the less-than operation for BCProblem based on g values
    def __lt__(self, other):
        return self.g < other.g