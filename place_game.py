import pygame
from utils1 import create_new_memory_retriever, LLM
from langchain.experimental.generative_agents import GenerativeAgentMemory

class Place():
    def __init__(self, name, description, x, y, x_bottom, y_bottom):

        self.x = x
        self.y = y
        self.x_bottom = x_bottom
        self.y_bottom = y_bottom
        self.height = y_bottom - y
        self.width = x_bottom - x
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.name = name
        self.description = description
        # self.objects = objects

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
        pass