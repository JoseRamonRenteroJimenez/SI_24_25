import time
from LGymClient import agentLoop
from BaseAgent import BaseAgent
from ReactiveAgent import ReactiveAgent


timeInit = time.time()
agent = ReactiveAgent("1","NJ-95")
agentLoop(agent,True)
timeEnd = time.time()
print("Ha transcurrido: ", timeEnd - timeInit, "segundos")