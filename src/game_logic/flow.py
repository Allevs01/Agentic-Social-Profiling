from crewai.flow.flow import Flow, start, listen, router
from pydantic import BaseModel
from crewai import Agent, Task, Crew
import yaml
import json
import random

# Importa le tue config
from .llm_config import get_gemini_llm

class GameState(BaseModel):
    last_message: str = ""
    conversation_history: list = []  # Lista di stringhe "Nome: Messaggio"
    suspicion_score: int = 0
    suspicion_reason: str = ""
    current_speaker: str = ""        # Chi risponderà (boss, bomber-thief, etc.)
    final_response_text: str = ""
    game_over: bool = False

class UndercoverFlow(Flow[GameState]):

    def __init__(self):
        super().__init__()
        self.llm = get_gemini_llm()
        # Carica configurazioni
        with open('config/agents.yaml', 'r') as f: self.agents_config = yaml.safe_load(f)
        with open('config/tasks.yaml', 'r') as f: self.tasks_config = yaml.safe_load(f)

    @start()
    def step_1_analyze_suspicion(self):
        # In una conversazione solo bot, il sospetto è meno rilevante o va ripensato.
        # Per ora lo bypassiamo o lo lasciamo a 0.
        self.state.suspicion_score = 0
        self.state.suspicion_reason = "Bot conversation - no suspicion check."
        return "checked"

    @router(step_1_analyze_suspicion)
    def step_2_check_game_over(self):
        if self.state.suspicion_score > 80:
            return "game_over"
        else:
            return "generate_reply"

    @listen("game_over")
    def handle_game_over(self):
        self.state.game_over = True
        self.state.final_response_text = "Tony ti punta la pistola: 'Troppe domande, sbirro.' (GAME OVER)"
        self.state.current_speaker = "boss"
        return self.state.final_response_text

    @listen("generate_reply")
    def step_3_criminal_response(self):
        # Logica di alternanza speaker
        # Se l'ultimo a parlare è stato il Boss, risponde un ladro.
        # Se ha parlato un ladro, risponde il Boss o un altro ladro.
        
        last_speaker = self.state.current_speaker
        
        if last_speaker == "boss":
            # Il boss ha parlato, risponde uno dei ladri
            agent_key = random.choice(['bomber-thief', 'tecnician-thief'])
        else:
            # Ha parlato un ladro, il Boss riprende la parola o interviene l'altro
            agent_key = "boss"
        
        self.state.current_speaker = agent_key
        
        # Crea l'agente scelto
        active_agent = Agent(
            config=self.agents_config[agent_key],
            llm=self.llm,
            verbose=True
        )

        task = Task(
            config=self.tasks_config['criminal_response_task'],
            agent=active_agent
        )

        history_str = "\n".join(self.state.conversation_history[-5:])

        crew = Crew(agents=[active_agent], tasks=[task], verbose=True)
        response = crew.kickoff(inputs={
            "conversation_history": history_str,
            "current_agent_name": agent_key,
            "last_message": self.state.last_message
        })

        self.state.final_response_text = str(response)
        
        # Aggiorna memoria
        self.state.conversation_history.append(f"{agent_key}: {self.state.final_response_text}")
        
        # Aggiorna l'ultimo messaggio per il prossimo giro
        self.state.last_message = self.state.final_response_text
        
        return self.state.final_response_text