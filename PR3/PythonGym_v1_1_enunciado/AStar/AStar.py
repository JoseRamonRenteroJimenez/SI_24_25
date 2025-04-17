import heapq as heapq

#Algoritmo A* genérico que resuelve cualquier problema descrito usando la plantilla de la
#la calse Problem que tenga como nodos hijos de la clase Node
class AStar:

    def __init__(self, problem):
        self.open = [] # lista de abiertos o frontera de exploración
        self.precessed = set() # set, conjunto de cerrados (más eficiente que una lista)
        self.problem = problem # problema a resolver

    def GetPlan(self):
        findGoal = False
        #TODO EN PRUEBAS implementar el algoritmo A*
        #cosas a tener en cuenta:
        #Si el número de sucesores es 0 es que el algoritmo no ha encontrado una solución, devolvemos el path vacio []
        #Hay que invertir el path para darlo en el orden correcto al devolverlo (path[::-1])
        #GetSucesorInOpen(sucesor) nos devolverá None si no lo encuentra, si lo encuentra
        #es que ese sucesor ya está en la frontera de exploración, DEBEMOS MIRAR SI EL NUEVO COSTE ES MENOR QUE EL QUE TENIA ALMACENADO
        #SI esto es asi, hay que cambiarle el padre y setearle el nuevo coste.
        # mientras no encontremos la meta y haya elementos en open....
        # TODO EN PRUEBAS implementar el bucle de búsqueda del algoritmo A*
        
        self.open.clear()
        self.precessed.clear()
        nodoObj = self.problem.Initial()
        self._ConfigureNode(nodoObj, None, 0)
        heapq.heappush(self.open, [nodoObj.F(), nodoObj])
        path = []
        cent = True
        
        while len(self.open) > 0 and not cent:
            #TODO EN PRUEBAS: Ordenar la lista de abiertos
            nodoObj = heapq.heappop(self.open)

            if nodoObj == self.problem.goal():
                cent = True
            else:
                sucesores = nodoObj.GetSucessors()
                for s in sucesores:
                    # Hacemos cosas si el nodo aún no ha sido procesado
                    if s not in self.precessed:
                        g = nodoObj.G() + self.problem.GetGCost(s)
                        
                        abierto = self.GetSucesorInOpen(s)
                        if abierto is None:
                            # TODO Configurar nodo????
                            self._ConfigureNode(s, nodoObj, g)
                            s.SetH(self.problem.Heuristic(s))
                            heapq.heappush(self.open, [s.F(), s])
                        else:
                            # Usar mejor nodo si ya hemos encontrado una ruta
                            if g < abierto.G():
                                self._ConfigureNode(abierto, nodoObj, g)
                                abierto.SetH(self.problem.Heuristic(abierto))
                self.precessed.add(nodoObj)
                # vuelve a la siguiente iteración
        
        if(cent == True):
            path = self.ReconstructPath(nodoObj)
        
        return path[::-1] 

    #nos permite configurar un nodo (node) con el padre y la nueva G
    def _ConfigureNode(self, node, parent, newG):
        node.SetParent(parent)
        node.SetG(newG)
        #TODO EN PRUEBAS Setearle la heuristica que está implementada en el problema. (si ya la tenía será la misma pero por si reutilizais este método para otras cosas)
        if(node.parent != None):
            node.SetH(parent.H)

    #nos dice si un sucesor está en abierta. Si esta es que ya ha sido expandido y tendrá un coste, comprobar que le nuevo camino no es más eficiente
    #En caso de serlos, _ConfigureNode para setearle el nuevo padre y el nuevo G, asi como su heurística
    def GetSucesorInOpen(self,sucesor):
        i = 0
        found = None
        while found == None and i < len(self.open):
            node = self.open[i]
            i += 1
            if node.IsEqual(sucesor):
                found = node
        return found


    #reconstruye el path desde la meta encontrada.
    def ReconstructPath(self, goal):
        path = []
        node = goal
        #TODO EN PRUEBAS devuelve el path invertido desde la meta hasta que el padre sea None.
        while node != None:
            path.append(node)
            node = node.parent
        return path



