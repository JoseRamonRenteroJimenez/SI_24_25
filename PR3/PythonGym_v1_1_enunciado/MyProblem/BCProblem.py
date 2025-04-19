#import sys
#sys.path.insert(1, '../AStar')
from AStar.Problem import Problem
from MyProblem.BCNode import BCNode
from States.AgentConsts import AgentConsts
import sys
import numpy as np

#Clase que implementa el problema especifico que queremos resolver y que hereda de la calse
#Problema genérico.
class BCProblem(Problem):
    
    def __init__(self, initial, goal, xSize, ySize):
        super().__init__(initial, goal)
        self.map = np.zeros((xSize,ySize),dtype=int)
        self.xSize = xSize
        self.ySize = ySize
    
    #inicializa un mapa con el mapa proveniente del entorno Vector => Matriz
    def InitMap(self,m):
        for i in range(len(m)):
            x,y = BCProblem.Vector2MatrixCoord(i,self.xSize,self.ySize)
            self.map[x][y] = m[i]

    #Muestra el mapa por consola
    def ShowMap(self):
        for j in range(self.ySize):
            s = ""
            for i in range(self.xSize):
                s += ("[" + str(i) + "," + str(j) + "," + str(self.map[i][j]) +"]")
            print(s)

    #Calcula la heuristica del nodo en base al problema planteado (Se necesita reimplementar)
    def Heuristic(self, node):
        '''
        node - nodo al que se le quiere calcular la heurística
        node.x - coordenada x del nodo objetivo
        node.y - coordenada y del nodo objetivo
        Calcula la heurística del nodo en base a la distancia Manhattan entre el nodo y el objetivo.
        abs(node.x - self.x) + abs(node.y- self.y)
        '''
        #TODO EN PRUEBAS: heurística del nodo
        h = abs(node.x - self.goal.x) + abs(node.y - self.goal.y)
        print(f"Heurística H = {h}")
        return h

    #Genera la lista de sucesores del nodo (Se necesita reimplementar)
    def GetSucessors(self, node):
        successors = []
        # TODO: sucesores de un nodo dado
        
        for newX, newY in ((0, -1), (-1, 0), (0, 1), (1, 0)):
            x = node.x + newX
            y = node.y + newY
            if x >= 0 and x < self.xSize and y >= 0 and y < self.ySize:
                print(f"Checking position: ({x}, {y})")
                if self.CanMove(self.map[x][y]):
                    successors.append(self.CreateNode(successors, node, x, y))
        
        '''
        # Arriba
        if(self.CanMove(self.map[node.x][node.y-1]) and node.y-1>=0):
            successors.append(self.CreateNode(successors, node, node.x, node.y-1))
        # Abajo
        if(self.CanMove(self.map[node.x][node.y+1]) and node.y+1<self.ySize):
            successors.append(self.CreateNode(successors, node, node.x, node.y+1))
        # Izquierda
        if(self.CanMove(self.map[node.x-1][node.y]) and node.x-1>=0):
            successors.append(self.CreateNode(successors, node, node.x-1, node.y))
        # Derecha
        if(self.CanMove(self.map[node.x+1][node.y]) and node.x+1<self.xSize):
            successors.append(self.CreateNode(successors, node, node.x+1, node.y))
        '''
        print("Aqui falta ncosas por hacer :) ")
        return successors[::-1]
    
    # métodos estáticos
    # nos dice si podemos movernos hacia una casilla, se debe poner el valor de la casilla como
    # parámetro
    @staticmethod
    def GetValueText(value):
        return {
            AgentConsts.NOTHING: "NOTHING",
            AgentConsts.UNBREAKABLE: "UNBREAKABLE",
            AgentConsts.BRICK: "BRICK",
            AgentConsts.COMMAND_CENTER: "COMMAND_CENTER",
            AgentConsts.PLAYER: "PLAYER",
            AgentConsts.SHELL: "SHELL",
            AgentConsts.OTHER: "OTHER",
            AgentConsts.LIFE: "LIFE",
            AgentConsts.SEMI_BREKABLE: "SEMI_BREKABLE",
            AgentConsts.SEMI_UNBREKABLE: "SEMI_UNBREKABLE"
        }.get(value, "UNKNOWN")

    @staticmethod
    def CanMove(value):
        value_text = BCProblem.GetValueText(value)
        print(f"CanMove check for value: {value} ({value_text})")
        return value != AgentConsts.UNBREAKABLE and value != AgentConsts.SEMI_UNBREKABLE
    
    #convierte coordenadas mapa en formato vector a matriz
    @staticmethod
    def Vector2MatrixCoord(pos,xSize,ySize):
        x = pos % xSize
        y = pos // ySize #division entera
        return x,y

    #convierte coordenadas mapa en formato matriz a vector
    @staticmethod
    def Matrix2VectorCoord(x,y,xSize):
        return y * xSize + x
    
    #convierte coordenadas del mapa en coordenadas del entorno (World) (nótese que la Y está invertida)
    @staticmethod
    def MapToWorldCoord(x,y,ySize):
        xW = x * 2
        yW = (ySize - y - 1) * 2
        return xW, yW

    #convierte coordenadas del entorno (World) en coordenadas mapa (nótese que la Y está invertida)
    @staticmethod
    def WorldToMapCoord(xW,yW,ySize):
        x = xW // 2
        y = yW // 2
        y = ySize - y - 1
        return x, y
    
    #versión real del método anterior, que nos ayuda a buscar los centros de las celdas.
    #aqui nos dirá los decimales, es decir como de cerca estamos de la esquina superior derecha
    #un valor de 1.9,1.9 nos dice que estamos en la casilla 1,1 muy cerca de la 2,2
    #en realidad, lo que buscamos es el punto medio de la casilla, es decir la 1.5, 1.5 en el caso
    #de la casilla 1,1
    @staticmethod
    def WorldToMapCoordFloat(xW,yW,ySize):
        x = xW / 2
        invY = (ySize*2) - yW
        invY = invY / 2
        return x, invY

    #se utiliza para calcular el coste de cada elemento del mapa 
    @staticmethod
    def GetCost(value):
        #TODO: debes darle un coste a cada tipo de casilla del mapa.

        ##NOTHING = 0
        ##UNBREAKABLE = 1
        ##BRICK = 2
        ##COMMAND_CENTER = 3
        ##PLAYER = 4
        ##SHELL = 5 
        ##OTHER = 6
        ##LIFE = 7
        ##SEMI_BREKABLE = 8
        ##SEMI_UNBREKABLE = 9
        
        #optimización a base de descartar la mitad de los operandos
        if(value%2==0):
            if value==AgentConsts.NOTHING:#0
                return 2
            elif value==AgentConsts.BRICK:#2
                return 3
            elif value==AgentConsts.PLAYER:#4
                return 10
            elif value==AgentConsts.OTHER:#6
                return 6
            elif value==AgentConsts.SEMI_BREKABLE:#8
                return sys.maxsize
            else:
                return sys.maxsize   
        else:
            if value==AgentConsts.UNBREAKABLE:#1
                return sys.maxsize
            elif value==AgentConsts.COMMAND_CENTER:#3
                return 0
            elif value== AgentConsts.SHELL:#5
                return 0
            elif value== AgentConsts.LIFE:#7
                return 0
            elif value== AgentConsts.SEMI_UNBREKABLE:#9
                return sys.maxsize
            else:
                return sys.maxsize
        return sys.maxsize
    
    #crea un nodo y lo añade a successors (lista) con el padre indicado y la posición x,y en coordenadas mapa 
    def CreateNode(self,successors,parent,x,y):
        value=self.map[x][y]
        g=BCProblem.GetCost(value) + parent.G()
        rightNode = BCNode(parent,g,value,x,y)
        rightNode.SetH(self.Heuristic(rightNode))
        return rightNode
        #successors.append(rightNode)

    #Calcula el coste de ir del nodo from al nodo to (Se necesita reimplementar)
    def GetGCost(self, nodeTo):
        return BCProblem.GetCost(nodeTo.value)