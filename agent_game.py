import pygame
import datetime
import pygame.mixer
from langchain.experimental.generative_agents import GenerativeAgent, GenerativeAgentMemory
from utils1 import generate_response,print_colored,relevance_score,retrieval_score,calculate_weight
from utils2 import initialise_conversation_tools
from typing import Optional
from modified_gen_agent import GameGenerativeAgent

from datetime import datetime


threshold = 0.26

# char = pygame.image.load('assets/char.gif')
 




##################  PATHS #######################
paths = {
  'Yamamoto Residence': {
    'Mizukami Shrine': [(757,465),(991,465)],
    'Hanazawa Garden': [(757,465),(991,465)],
    'Kogaku Institute of Physics': [(757,465),(991,465)],
    'Well': [(757,465),(991,465)],
    'Haya Apartment 1': [(757,465),(991,465)],
    'Haya Apartment 2': [(757,465),(991,465)],
    'Haya Apartment 3': [(757,465),(991,465)],
    'Haya Apartment 4': [(757,465),(991,465)],
    'Yamamoto Residence': [(757,465),(991,465)],
    'Shino Grocery Store': [(757,465),(991,465)],
    
  } ,
  'Well': {
    'Mizukami Shrine': [(757,465),(991,465)],
    'Hanazawa Garden': [(757,465),(991,465)],
    'Kogaku Institute of Physics': [(757,465),(991,465)],
    'Well': [(757,465),(991,465)],
    'Haya Apartment 1': [(757,465),(991,465)],
    'Haya Apartment 2': [(757,465),(991,465)],
    'Haya Apartment 3': [(757,465),(991,465)],
    'Haya Apartment 4': [(757,465),(991,465)],
    'Yamamoto Residence': [(757,465),(991,465)],
    'Shino Grocery Store': [(757,465),(991,465)],
    
  }  ,
  'Haya Apartment 1': {
    'Mizukami Shrine': [(757,465),(991,465)],
    'Hanazawa Garden': [(757,465),(991,465)],
    'Kogaku Institute of Physics': [(757,465),(991,465)],
    'Well': [(757,465),(991,465)],
    'Haya Apartment 1': [(757,465),(991,465)],
    'Haya Apartment 2': [(757,465),(991,465)],
    'Haya Apartment 3': [(757,465),(991,465)],
    'Haya Apartment 4': [(757,465),(991,465)],
    'Yamamoto Residence': [(757,465),(991,465)],
    'Shino Grocery Store': [(757,465),(991,465)],
    
  }  ,
  'Haya Apartment 2': {
    'Mizukami Shrine': [(757,465),(991,465)],
    'Hanazawa Garden': [(757,465),(991,465)],
    'Kogaku Institute of Physics': [(757,465),(991,465)],
    'Well': [(757,465),(991,465)],
    'Haya Apartment 1': [(757,465),(991,465)],
    'Haya Apartment 2': [(757,465),(991,465)],
    'Haya Apartment 3': [(757,465),(991,465)],
    'Haya Apartment 4': [(757,465),(991,465)],
    'Yamamoto Residence': [(757,465),(991,465)],
    'Shino Grocery Store': [(757,465),(991,465)],
    
  }  ,
  'Haya Apartment 3': {
     'Mizukami Shrine': [(757,465),(991,465)],
    'Hanazawa Garden': [(757,465),(991,465)],
    'Kogaku Institute of Physics': [(757,465),(991,465)],
    'Well': [(757,465),(991,465)],
    'Haya Apartment 1': [(757,465),(991,465)],
    'Haya Apartment 2': [(757,465),(991,465)],
    'Haya Apartment 3': [(757,465),(991,465)],
    'Haya Apartment 4': [(757,465),(991,465)],
    'Yamamoto Residence': [(757,465),(991,465)],
    'Shino Grocery Store': [(757,465),(991,465)],
    
  }  ,
  'Haya Apartment 4': {
     'Mizukami Shrine': [(757,465),(991,465)],
    'Hanazawa Garden': [(757,465),(991,465)],
    'Kogaku Institute of Physics': [(757,465),(991,465)],
    'Well': [(757,465),(991,465)],
    'Haya Apartment 1': [(757,465),(991,465)],
    'Haya Apartment 2': [(757,465),(991,465)],
    'Haya Apartment 3': [(757,465),(991,465)],
    'Haya Apartment 4': [(757,465),(991,465)],
    'Yamamoto Residence': [(757,465),(991,465)],
    'Shino Grocery Store': [(757,465),(991,465)],
    
  }  ,
  'Kogaku Institute of Physics': {
   'Mizukami Shrine': [(757,465),(991,465)],
    'Hanazawa Garden': [(757,465),(991,465)],
    'Kogaku Institute of Physics': [(757,465),(991,465)],
    'Well': [(757,465),(991,465)],
    'Haya Apartment 1': [(757,465),(991,465)],
    'Haya Apartment 2': [(757,465),(991,465)],
    'Haya Apartment 3': [(757,465),(991,465)],
    'Haya Apartment 4': [(757,465),(991,465)],
    'Yamamoto Residence': [(757,465),(991,465)],
    'Shino Grocery Store': [(757,465),(991,465)],
    
  }  ,
  'Mizukami Shrine': {
    'Mizukami Shrine': [(757,465),(991,465)],
    'Hanazawa Garden': [(757,465),(991,465)],
    'Kogaku Institute of Physics': [(757,465),(991,465)],
    'Well': [(757,465),(991,465)],
    'Haya Apartment 1': [(757,465),(991,465)],
    'Haya Apartment 2': [(757,465),(991,465)],
    'Haya Apartment 3': [(757,465),(991,465)],
    'Haya Apartment 4': [(757,465),(991,465)],
    'Yamamoto Residence': [(757,465),(991,465)],
    'Shino Grocery Store': [(757,465),(991,465)],
    
  }  ,
  'Hanazawa Garden': {
    'Mizukami Shrine': [(757,465),(991,465)],
    'Hanazawa Garden': [(757,465),(991,465)],
    'Kogaku Institute of Physics': [(757,465),(991,465)],
    'Well': [(757,465),(991,465)],
    'Haya Apartment 1': [(757,465),(991,465)],
    'Haya Apartment 2': [(757,465),(991,465)],
    'Haya Apartment 3': [(757,465),(991,465)],
    'Haya Apartment 4': [(757,465),(991,465)],
    'Yamamoto Residence': [(757,465),(991,465)],
    'Shino Grocery Store': [(757,465),(991,465)],
    
  }  ,
  'Shino Grocery Store': {
     'Mizukami Shrine': [(757,465),(991,465)],
    'Hanazawa Garden': [(757,465),(991,465)],
    'Kogaku Institute of Physics': [(757,465),(991,465)],
    'Well': [(757,465),(991,465)],
    'Haya Apartment 1': [(757,465),(991,465)],
    'Haya Apartment 2': [(757,465),(991,465)],
    'Haya Apartment 3': [(757,465),(991,465)],
    'Haya Apartment 4': [(757,465),(991,465)],
    'Yamamoto Residence': [(757,465),(991,465)],
    'Shino Grocery Store': [(757,465),(991,465)],
    
  }  
}





class Agent():
    def __init__(self, name:str, age:int, agent_type:str, traits:str, status:str, location, memory_retriever, llm, reflection_threshold:int, verbose:bool, x, y, width, height,image_path, left_images,right_images,up_images,down_images):

        self.memory = GenerativeAgentMemory(
            llm=llm,
            memory_retriever=memory_retriever,
            verbose=verbose,
            reflection_threshold=reflection_threshold # we will give this a relatively low number to show how reflection works
        )

        self.person = GameGenerativeAgent(name=name,
                    age=age,
                    traits=traits, # You can add more persistent traits here
                    status=status, # When connected to a virtual world, we can have the characters update their status
                    memory_retriever=memory_retriever,
                    llm=llm,
                    memory=self.memory
                    )
        
        if(agent_type=="TownFolk" or agent_type=="WereWolf"):
            self.agent_type = agent_type
        else:
            raise ValueError("agent_type can be either TownFolk or WereWolf")
        
        self.state = "alive"

        self.location = location

        self.relations = {}

        self.plans = []

        self.profile = []
        
        # Physical Apperance of the Character
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.char = pygame.image.load(image_path)
        self.left_images = left_images
        self.right_images = right_images
        self.up_images = up_images
        self.down_images = down_images
        self.agent_type == "WereWolf"
        
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walkCount = 0
        self.vel = 1  # Adjust the speed of the agent
        self.current_point = 1
        self.direction = 1

    def draw(self, win, left_images_werewolf, right_images_werewolf,up_images_werewolf,down_images_werewolf,char_werewolf,env,env_night,current_background):
        if self.walkCount + 1 >= 9:
            self.walkCount = 0
        
        if self.left:
            if(self.agent_type == "WereWolf" and current_background == env_night):
                win.blit(left_images_werewolf[self.walkCount//3],(self.x,self.y))
            else:
                win.blit(self.left_images[self.walkCount//3],(self.x,self.y))
            self.walkCount += 1
        elif self.right:
            if(self.agent_type == "WereWolf" and current_background == env_night):
                win.blit(right_images_werewolf[self.walkCount//3],(self.x,self.y))
            else:
                win.blit(self.right_images[self.walkCount//3],(self.x,self.y))
            self.walkCount += 1
        elif self.up:
            if(self.agent_type == "WereWolf" and current_background == env_night):
                win.blit(up_images_werewolf[self.walkCount//3],(self.x,self.y))
            else:
                win.blit(self.up_images[self.walkCount//3],(self.x,self.y))
            self.walkCount += 1
        elif self.down:
            if(self.agent_type == "WereWolf" and current_background == env_night):
                win.blit(down_images_werewolf[self.walkCount//3],(self.x,self.y))
            else:
                win.blit(self.down_images[self.walkCount//3],(self.x,self.y))
            self.walkCount += 1
        else:
            if(self.agent_type == "WereWolf" and current_background == env_night):
                win.blit(char_werewolf, (self.x,self.y))
            else:
                win.blit(self.char, (self.x,self.y))
    
    def add_relations(self, Agent, relation):
        self.relations[Agent.name] = relation




    def move_agent(self,prev_location,new_location):
        # global agent_x, agent_y, current_point, direction
        # Calculate the target position based on the current point in the path
        path = [(757,465),(991,465)]
        final = 991
        if(self.x == 991):
             path = [(991,465),(757,465)]
             final = 757

        while(self.x != final):
               
                target_x, target_y = path[self.current_point]

                # Calculate the change in x and y coordinates based on the target position
                x_change = self.vel if target_x > self.x else -self.vel if target_x < self.x else 0
                y_change = self.vel if target_y > self.y else -self.vel if target_y < self.y else 0

                # Update the agent's position
                self.x += x_change
                self.y += y_change

                if(x_change > 0):
                    self.right = True
                    self.left = False
                    self.up = False
                    self.down = False

                if(x_change < 0):
                    self.right = False
                    self.left = True
                    self.up = False
                    self.down = False

                if(y_change > 0):
                    self.right = False
                    self.left = False
                    self.up = False
                    self.down = True

                if(y_change < 0):
                    self.right = False
                    self.left = False
                    self.up = True
                    self.down = False

                

                # Check if the agent has reached the target position
                # if self.x == target_x and self.y == target_y:
                #     # Move to the next point in the path
                #     self.current_point += self.direction

                    # Check if the agent has reached the end of the path, and reverse the direction
                    # if self.current_point == len(path) :
                    #     self.direction = -1
                    #     self.current_point = len(path) - 2
                    # elif self.current_point == -1:
                    #     self.direction = 1
                    #     self.current_point = 1

        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.current_point = 1
        self.direction = 1




    def update_location(self,prev_location, new_location):
        self.move_agent(prev_location, new_location)
        self.location = new_location
           
        # self.x = new_location.x
        # self.y = new_location.y
        
  
    def get_memory(self):
        temp_mem = ""
        for i in range(0,len(self.person.memory.memory_retriever.memory_stream)):
            temp_mem+= self.person.memory.memory_retriever.memory_stream[i].page_content
        
        return temp_mem
  
    def get_mem_summary(self,prompt):
    
        recency = 0 
        relevance = 0
        importance = 0
        
        current_time = datetime.now()
        print(current_time)
        get_summary_points = ""

        for i in range(0,len(self.person.memory.memory_retriever.memory_stream)):
            mem_point = self.person.memory.memory_retriever.memory_stream[i].page_content
            relevance = relevance_score(mem_point,prompt)
            importance = self.person.memory.memory_retriever.memory_stream[i].metadata['importance']
            hours_diff = current_time - self.person.memory.memory_retriever.memory_stream[i].metadata['last_accessed_at'] 
            # print(hours_diff)
            # # self.person.memory.memory_retriever.memory_stream[i].metadata['last_accessed_at'] = current_time
            # #recency = calculate_weight(hours_diff)
            # print(importance,"\n")
            # print(relevance,"\n")
            # print(recency,"\n")
            final_score = retrieval_score(relevance,importance,recency)
            
            # print(final_score," ",mem_point, "\n")

            if final_score >= threshold:
                get_summary_points+=mem_point

            
        result = generate_response(f"Summarize {get_summary_points} in not more than 60 words.")

        return result


    def make_interaction_conversation_tree(self, current_time, Agents:list, user_setting = False, user_initializer: Optional[str] = ""):
    # interaction tree handling feature added

     if(self.agent_type=="TownFolk"):
      all_tools = initialise_conversation_tools(self.agent_type)
      for agent in Agents:
        all_tools_agent = initialise_conversation_tools(agent.agent_type)
        if(agent.agent_type=="TownFolk"):
          continue_convo = True
          dialogue_response = ""
          current_plan_self = self.plans[self.plans['Time'].apply(lambda x: x.hour) == current_time]['Plans'].values[0]
          current_plan_agent = agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == current_time]['Plans'].values[0]
          counter = 0
          while True:
            # self chance
            if dialogue_response == "":
              tools_to_use = [all_tools["townfolk_initialise_dialogue_tool"]]
              current_plan_reaction, consumed_tokens_reaction = self.person.generate_reaction(self.agent_type, current_plan_agent, current_time)
              continue_convo, dialogue_response, consumed_tokens_dialogue = self.person.initialise_dialogue_response(self.agent_type, agent, current_plan_self, current_plan_agent, current_plan_reaction, current_time, tools_to_use, self.relations, user_setting, user_initializer)

              # break
            else:
              print(counter)
              tools_to_use = [all_tools["townfolk_continue_dialogue_tool"], all_tools["townfolk_end_dialogue_tool"]]
              previous_dialogue_response_reaction, consumed_tokens_reaction = self.person.generate_reaction(self.agent_type, dialogue_response, current_time)
              continue_convo, dialogue_response, consumed_tokens_dialogue = self.person.generate_dialogue_response(self.agent_type, agent, dialogue_response, previous_dialogue_response_reaction, current_plan_self, current_plan_agent, current_time, tools_to_use, self.relations, counter)
              
            print_colored(f"{self.person.name} ({consumed_tokens_dialogue}): {dialogue_response}", "blue")
            if not continue_convo:
              break
            #other agent's chance

            tools_to_use = [all_tools_agent["townfolk_continue_dialogue_tool"], all_tools_agent["townfolk_end_dialogue_tool"]]
            previous_dialogue_response_reaction, consumed_tokens_reaction = agent.person.generate_reaction(agent.agent_type, dialogue_response, current_time)
            continue_convo, dialogue_response, consumed_tokens_dialogue = agent.person.generate_dialogue_response(agent.agent_type, self, dialogue_response, previous_dialogue_response_reaction, current_plan_agent, current_plan_self, current_time, tools_to_use, agent.relations, counter)
            print_colored(f"{agent.person.name} ({consumed_tokens_dialogue}): {dialogue_response}", "magenta")
            counter+=1
        else:
          continue_convo = True
          dialogue_response = ""
          current_plan_self = self.plans[self.plans['Time'].apply(lambda x: x.hour) == current_time]['Plans'].values[0]
          current_plan_agent = agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == current_time]['Plans'].values[0]
          counter = 0
          while True:
            # self chance
            if dialogue_response == "":
              tools_to_use = [all_tools["townfolk_initialise_dialogue_tool"]]
              current_plan_reaction, consumed_tokens_reaction = self.person.generate_reaction(self.agent_type, current_plan_agent, current_time)
              continue_convo, dialogue_response, consumed_tokens_dialogue = self.person.initialise_dialogue_response(self.agent_type, agent, current_plan_self, current_plan_agent, current_plan_reaction, current_time, tools_to_use, self.relations, user_setting, user_initializer)

              # break
            else:
              print(counter)
              tools_to_use = [all_tools["townfolk_continue_dialogue_tool"], all_tools["townfolk_end_dialogue_tool"]]
              previous_dialogue_response_reaction, consumed_tokens_reaction = self.person.generate_reaction(self.agent_type, dialogue_response, current_time)
              continue_convo, dialogue_response, consumed_tokens_dialogue = self.person.generate_dialogue_response(self.agent_type, agent, dialogue_response, previous_dialogue_response_reaction, current_plan_self, current_plan_agent, current_time, tools_to_use, self.relations, counter)

            print_colored(f"{self.person.name} ({consumed_tokens_dialogue}): {dialogue_response}", "blue")
            if not continue_convo:
              break
            #other agent's chance

            tools_to_use = [all_tools_agent["werewolf_continue_dialogue_tool"], all_tools_agent["werewolf_end_dialogue_tool"]]
            previous_dialogue_response_reaction, consumed_tokens_reaction = agent.person.generate_reaction(agent.agent_type, dialogue_response, current_time)
            continue_convo, dialogue_response, consumed_tokens_dialogue = agent.person.generate_dialogue_response(agent.agent_type, self, dialogue_response, previous_dialogue_response_reaction, current_plan_agent, current_plan_self, current_time, tools_to_use, agent.relations, counter)
            print_colored(f"{agent.person.name} ({consumed_tokens_dialogue}): {dialogue_response}", "magenta")
            counter+=1

        # pass
     elif(self.agent_type=="WereWolf"):
      all_tools = initialise_conversation_tools(self.agent_type)

      for agent in Agents:
        all_tools_agent = initialise_conversation_tools(agent.agent_type)
        if(agent.agent_type=="TownFolk"):
          continue_convo = True
          dialogue_response = ""
          current_plan_self = self.plans[self.plans['Time'].apply(lambda x: x.hour) == current_time]['Plans'].values[0]
          current_plan_agent = agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == current_time]['Plans'].values[0]
          counter = 0
          while True:
            # self chance
            if dialogue_response == "":
              tools_to_use = [all_tools["werewolf_initialise_dialogue_tool"]]
              # self, self_type, observation: str, current_time, now: Optional[datetime] = datetime.now()
              current_plan_reaction, consumed_tokens_reaction = self.person.generate_reaction(self.agent_type, current_plan_agent, current_time)
              continue_convo, dialogue_response, consumed_tokens_dialogue = self.person.initialise_dialogue_response(self.agent_type, agent, current_plan_self, current_plan_agent, current_plan_reaction, current_time, tools_to_use, self.relations, user_setting, user_initializer)

              # break
            else:
              print(counter)
              tools_to_use = [all_tools["werewolf_continue_dialogue_tool"], all_tools["werewolf_end_dialogue_tool"]]
              previous_dialogue_response_reaction, consumed_tokens_reaction = self.person.generate_reaction(self.agent_type, dialogue_response, current_time)
              continue_convo, dialogue_response, consumed_tokens_dialogue = self.person.generate_dialogue_response(self.agent_type, agent, dialogue_response, previous_dialogue_response_reaction, current_plan_self, current_plan_agent, current_time, tools_to_use, self.relations, counter)
            print_colored(f"{self.person.name} ({consumed_tokens_dialogue}): {dialogue_response}", "blue")
            if not continue_convo:
              break
            #other agent's chance
            tools_to_use = [all_tools_agent["townfolk_continue_dialogue_tool"], all_tools_agent["townfolk_end_dialogue_tool"]]
            previous_dialogue_response_reaction, consumed_tokens_reaction = agent.person.generate_reaction(agent.agent_type, dialogue_response, current_time)
            continue_convo, dialogue_response, consumed_tokens_dialogue = agent.person.generate_dialogue_response(agent.agent_type, self, dialogue_response, previous_dialogue_response_reaction, current_plan_agent, current_plan_self, current_time, tools_to_use, agent.relations, counter)
            print_colored(f"{agent.person.name} ({consumed_tokens_dialogue}): {dialogue_response}", "magenta")

            counter+=1
        else: # agent.agent_type == "WereWolf"
          continue_convo = True
          dialogue_response = ""
          current_plan_self = self.plans[self.plans['Time'].apply(lambda x: x.hour) == current_time]['Plans'].values[0]
          current_plan_agent = agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == current_time]['Plans'].values[0]
          counter = 0
          while True:
            # self chance
            if dialogue_response == "":
              tools_to_use = [all_tools["werewolf_team_initialise_dialogue_tool"]]
              current_plan_reaction, consumed_tokens_reaction = self.person.generate_reaction(self.agent_type, current_plan_agent, current_time)
              continue_convo, dialogue_response, consumed_tokens_dialogue = self.person.initialise_dialogue_response(self.agent_type, agent, current_plan_self, current_plan_agent, current_plan_reaction, current_time, tools_to_use, self.relations, user_setting, user_initializer)

              # break
            else:
              print(counter)
              tools_to_use = [all_tools["werewolf_continue_dialogue_tool"], all_tools["werewolf_end_dialogue_tool"]]
              previous_dialogue_response_reaction, consumed_tokens_reaction = self.person.generate_reaction(self.agent_type, dialogue_response, current_time)
              continue_convo, dialogue_response, consumed_tokens_dialogue = self.person.generate_dialogue_response(self.agent_type, agent, dialogue_response, previous_dialogue_response_reaction, current_plan_self, current_plan_agent, current_time, tools_to_use, self.relations, counter)
            
            print_colored(f"{self.person.name} ({consumed_tokens_dialogue}): {dialogue_response}", "blue")
            if not continue_convo:
              break
            #other agent's chance
            tools_to_use = [all_tools_agent["werewolf_continue_dialogue_tool"], all_tools_agent["werewolf_end_dialogue_tool"]]
            previous_dialogue_response_reaction, consumed_tokens_reaction = agent.person.generate_reaction(agent.agent_type, dialogue_response, current_time)
            continue_convo, dialogue_response, consumed_tokens_dialogue = agent.person.generate_dialogue_response(agent.agent_type, self, dialogue_response, previous_dialogue_response_reaction, current_plan_agent, current_plan_self, current_time, tools_to_use, agent.relations, counter)
            print_colored(f"{agent.person.name} ({consumed_tokens_dialogue}): {dialogue_response}", "magenta")
            counter+=1

     else:
      ValueError("\'agent_type\' changed after initialisation. \'agent_type\' can be either TownFolk or WereWolf.")
      

    def make_interaction(self, current_time, Agents:list, last_message:str):
        for agent in Agents:
            continue_convo = True
            dialogue_response = last_message
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

                print(dialogue_response,"magenta")
                if not continue_convo:
                    break
                #other agent's chance
                continue_convo, dialogue_response = agent.person.generate_dialogue_response(dialogue_response)
                print(dialogue_response,"green")
                agent.memory.add_memory(dialogue_response)
                if not continue_convo:
                    break

    def killing_action(self,Agent2,agents):
        Agent2.state = "dead"
        Agent2.memory.add_memory("I have eliminated {}".format(Agent2.person.name))

        for agent in agents:
            if agent!=Agent2:
                agent.memory.add_memory("{} has been eliminated at {}.".format(Agent2.person.name,Agent2.location))
