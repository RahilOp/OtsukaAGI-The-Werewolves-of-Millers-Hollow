import langchain
from langchain.experimental.generative_agents import GenerativeAgent, GenerativeAgentMemory
from utils import generate_response,print_colored

 
class Agent():
  def __init__(self, name:str, age:int, traits:str, status:str, location:str, memory_retriever, llm, reflection_threshold:int, verbose:bool):
    self.memory = GenerativeAgentMemory(
        llm=llm,
        memory_retriever=memory_retriever,
        verbose=verbose,
        reflection_threshold=reflection_threshold # we will give this a relatively low number to show how reflection works
    )

    self.person = GenerativeAgent(name=name,
                  age=age,
                  traits=traits, # You can add more persistent traits here
                  status=status, # When connected to a virtual world, we can have the characters update their status
                  memory_retriever=memory_retriever,
                  llm=llm,
                  memory=self.memory
                )
    
    self.state = "alive"

    self.location = location

    self.relations = {}

    self.plans = []

    self.profile = []


  def add_relations(self, Agent, relation):
    self.relations[Agent.name] = relation

  def update_location(self,new_location):
    self.location = new_location
  
  def get_memory(self):
    temp_mem = ""
    for i in range(0,len(self.person.memory.memory_retriever.memory_stream)):
      temp_mem+= self.person.memory.memory_retriever.memory_stream[i].page_content
      
    return temp_mem

  def make_interaction(self, current_time, Agents:list, last_message):
    for agent in Agents:
      continue_convo = True
      dialogue_response = ""
      while True:
        #self chance
        if dialogue_response == "":
          start_prompt = f"It is currently {current_time}. \
            you are {self.person.name} and you are currently at {self.location} with {agent.person.name}. Your status is {agent.person.status}. Your age is {agent.person.age}. \
            The traits of {agent.person.name} having age {agent.person.age} are: {agent.person.traits}.  \
            \
            Greet {agent.person.name} and start the conversation as {self.person.name}. Initiate conversation with him/her with a single line message on the basis of your relations: {self.relations[agent.person.name]} and your memories: {self.memory.fetch_memories(f'Give the memories related to {agent.person.name}')}"
          dialogue_response = generate_response(start_prompt)
        else:
          continue_convo, dialogue_response = self.person.generate_dialogue_response(dialogue_response)
        self.memory.add_memory(dialogue_response)
        print_colored(dialogue_response,"magenta")
        if not continue_convo:
          break
        #other agent's chance
        continue_convo, dialogue_response = agent.person.generate_dialogue_response(dialogue_response)
        print_colored(dialogue_response,"green")
        agent.memory.add_memory(dialogue_response)
        if not continue_convo:
          break

  def killing_action(self,Agent2,agents):
   Agent2.state = "dead"
   Agent2.memory.add_memory("I have killed {}".format(Agent2.person.name))
   
   for agent in agents:
      if agent!=Agent2:
        agent.generate_reaction("{} has been killed at {}.".format(Agent2.person.name,Agent2.location))

