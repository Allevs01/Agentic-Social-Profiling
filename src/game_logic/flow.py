from crewai.flow.flow import Flow, start, listen
from .state import GameState
from .crew import create_cop_agent, create_boss_agent

class UndercoverFlow(Flow[GameState]):
    # ... Implement

    # Esempio semplificato dentro il Flow
    @listen(start_step)
    def run_judge(self, user_message):
        # Esegue SOLO il task del giudice
        task = Task(..., agent=judge_agent)
        crew = Crew(agents=[judge_agent], tasks=[task])
        result = crew.kickoff()
        
        # Parsing del JSON (la funzione che ti ho dato prima)
        parsed_result = parse_judge_output(result)
        
        # Salva nello stato
        self.state.suspicion_data = parsed_result
        self.state.suspicion_meter = parsed_result['score']
        
        return parsed_result