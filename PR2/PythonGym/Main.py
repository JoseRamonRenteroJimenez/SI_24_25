from LGymClient import agentLoop
from BaseAgent import BaseAgent
from ReactiveAgent import ReactiveAgent

agent = ReactiveAgent("1","NJ-95")
agentLoop(agent,True)

 