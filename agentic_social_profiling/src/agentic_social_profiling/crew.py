from .utils import discord_logger
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class AgenticSocialProfiling():
    """AgenticSocialProfiling crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def cop(self) -> Agent:
        return Agent(
            config=self.agents_config['cop'], # type: ignore[index]
            memory=True,
            verbose=True
        )

    @agent
    def boss(self) -> Agent:
        return Agent(
            config=self.agents_config['boss'], # type: ignore[index]
            memory=True,
            verbose=True
        )
    
    @agent
    def tecnician_thief(self) -> Agent:
        return Agent(
            config=self.agents_config['tecnician_thief'], # type: ignore[index]
            memory=True,
            verbose=True
        )
    
    @agent
    def bomber_thief(self) -> Agent:
        return Agent(
            config=self.agents_config['bomber_thief'], # type: ignore[index]
            memory=True,
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    
    @task
    def boss_opening_task(self) -> Task:
        return Task(
            config=self.tasks_config['boss_opening_task'], # type: ignore[index]
            callback=discord_logger.task_callback       
        )
    
    @task
    def cop_presentation_task(self) -> Task:
        return Task(
            config=self.tasks_config['cop_presentation_task'], # type: ignore[index]
            callback=discord_logger.task_callback
        )
    
    @task
    def tecnician_thief_response_task(self) -> Task:
        return Task(
            config=self.tasks_config['tecnician_thief_response_task'], # type: ignore[index]
            callback=discord_logger.task_callback
        )
    
    @task
    def cop_questioning_task(self) -> Task:
        return Task(
            config=self.tasks_config['cop_questioning_task'], # type: ignore[index]
            callback=discord_logger.task_callback
        )
    
    @task
    def boss_observation_task(self) -> Task:
        return Task(
            config=self.tasks_config['boss_observation_task'], # type: ignore[index]
            callback=discord_logger.task_callback 
        )
    
   

    # @task
    # def reporting_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['reporting_task'], # type: ignore[index]
    #         output_file='report.md'
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the AgenticSocialProfiling crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
    
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
