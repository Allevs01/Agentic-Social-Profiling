from crewai.flow.flow import Flow, start, listen
from .state import GameState
from .crew import create_cop_agent, create_boss_agent

class UndercoverFlow(Flow[GameState]):
    # ... Implementazione dei decoratori @start, @listen ...
    pass