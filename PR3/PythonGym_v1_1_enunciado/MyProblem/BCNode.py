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

    # Operaciones propias añadidas
    #comparamos 2 nodos por su coste
    def __lt__(self, other):    
        return self.F() < other.F()
    #comparamos 2 nodos por sus coordenadas ( usado para no expandir nodos ya procesados)
    def __eq__(self, other):
        return isinstance(other, BCNode) and self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))