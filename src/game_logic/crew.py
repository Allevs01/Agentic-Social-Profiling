from crewai import Agent, Crew, Process
from .llm_config import get_gemini_llm
import yaml

# Funzione helper per caricare yaml
def load_config(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

agents_config = load_config('config/agents.yaml')
llm = get_gemini_llm()

def create_cop_agent():
    return Agent(
        config=agents_config['cop'],
        llm=llm,
        verbose=True
    )

def create_boss_agent():
    return Agent(
        config=agents_config['boss'],
        llm=llm,
        verbose=True
    )

def create_tecnician_thief_agent():
    return Agent(
        config=agents_config['tecnician-thief'],
        llm=llm,
        verbose=True
    )

def create_bomber_thief_agent():
    return Agent(
        config=agents_config['bomber-thief'],
        llm=llm,
        verbose=True
    )
    
def create_judge_agent():
    return Agent(
        config=agents_config['judge'],
        llm=llm,
        verbose=True
    )
