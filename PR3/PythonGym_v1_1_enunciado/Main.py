from LGymClient import agentLoop
from BaseAgent import BaseAgent
#from ReactiveAgent import ReactiveAgent
from GoalOrientedAgent import GoalOrientedAgent


agent = GoalOrientedAgent("1","NJ-95")
agentLoop(agent,True)