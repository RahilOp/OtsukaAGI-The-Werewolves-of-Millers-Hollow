import utils as ut
from utils import create_new_memory_retriever, LLM
from langchain.experimental.generative_agents import GenerativeAgentMemory


class Place():
  def __init__(self, name, description, objects:dict):
    self.name = name
    self.description = description
    self.objects = objects
    self.history = GenerativeAgentMemory(
        llm=LLM,
        memory_retriever=create_new_memory_retriever(),
        verbose=False,
        reflection_threshold=8 # we will give this a relatively low number to show how reflection works
    )

  def add_history(self, input:str):
    self.history.add_memory(input)

  # Add a summary parameter formed by precision recall technique
  def get_summary():
    """
      Add a summary parameter formed by precision recall technique
    """
    pass