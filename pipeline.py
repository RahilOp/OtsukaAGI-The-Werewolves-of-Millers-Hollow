from datetime import time
from utils1 import generate_response, print_colored
import random
from utils2 import decision_making
import initialize
from initialize import df,agents,locations,profiles, garden
import nltk
from nltk.tokenize import sent_tokenize
import warnings
warnings.filterwarnings("ignore")
import datetime as datetime_only
import random

# Main function to carry on the simulation
print(df.head())


# To_be_killed_time = time(7,0,0)
# Killer_time = time(8,0,0)
# Voting_time = time(18,0,0)
Killer_time = 18
Voting_time = 7
debug = True
i_agents = agents
i_locations = locations
simulation_path = "simulation.html"
agent_current_tasks = {}
def pipeline(global_time, day):
        if debug:
            print(global_time, type(global_time))
            # for global_time in df['Time']:
            print_colored(f"Global time is: {datetime_only.time(global_time,0)}", "magenta",simulation_path)
            #     # people finding on the location and print them
        
        agents = []
        for agent in i_agents:
            if agent.state == "alive":
                agents.append(agent)

        people = {}
        for location in i_locations:
            print_colored(f"Location: {location.name}", "blue",simulation_path)
            people[location.name] = []
            for agent in agents:
               if agent.location.name == location.name:
                 people[location.name].append(agent)

            for (num, p) in enumerate(people[location.name]):
                print_colored(f"{num+1}. {p.person.name}", "black",simulation_path)

        for location in i_locations:
            print("\n\n")
            print_colored(f"{location.name}", "blue",simulation_path)
            # Doing Tasks
            print_colored("Doing Tasks", "red",simulation_path)
            # each agent first does its task at this location
            agent_list = people[location.name]
            for (num, local_agent) in enumerate(agent_list):
                print_colored(f"{num+1}. {local_agent.person.name}", "sky blue",simulation_path)
                reaction, consumed_tokens = local_agent.person.generate_reaction(local_agent.agent_type, local_agent.plans[local_agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0], global_time)
                # reaction, consumed_tokens = local_agent.person.generate_reaction(local_agent.agent_type, local_agent.plans[local_agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0], global_time)
                print_colored(f"Task: {local_agent.plans[local_agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0]}", "sky blue",simulation_path)
                print_colored(f"Reaction: {reaction}", "green",simulation_path)
                agent_current_tasks[local_agent.person.name] = local_agent.short_plans[local_agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0]
                # res = generate_response(f'''User: Generate a sequence of actions and time in minutes for the agent to perform as part of its "Takashi opens the Shino Grocery Store." and convert in present continuous form
                #                     Agent: 'Takashi is arriving at the store and unlocking the entrance door - 5 minutes. He is turning on the lights and adjusting the temperature settings - 2 minutes. He is checking inventory and restocking shelves if necessary - 10 minutes. He is setting up the cash register and ensuring it's functioning properly - 5 minutes. He is arranging promotional displays or special offers - 8 minutes. He is verifying the freshness of perishable items - 3 minutes. He is reviewing the schedule for incoming deliveries - 5 minutes. He is performing a quick cleanup of the store and organizing any clutter - 7 minutes. He is opening the store for customers and removing the "Closed" sign - 1 minute. '

                #                     Use the example given above to similarily generate subplans and convert in present continuous tense for:
                #                     "{local_agent.plans[local_agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0]}"''')

                # # Tokenize the paragraph into sentences
                # sentences = sent_tokenize(res)

                # # Print the extracted sentences
                # for sentence in sentences:
                #     print_colored(sentence,"green",simulation_path)
                

            print_colored("Interaction", "red",simulation_path)

            for i in range(0, len(agent_list)):
                # for j in range(i+1, len(agent_list)):
                #     print(f"Dialogue between {agent_list[i].person.name} and {agent_list[j].person.name}:", "cyan")
                #     # def make_interaction_conversation_tree(self, current_time, Agents:list, user_setting = False, user_initializer: Optional[str] = "")
                #     agent_list[i].make_interaction_conversation_tree(global_time, [agent_list[j]])
                valid_indices = [index for index in range(len(agent_list)) if index != i]
                if valid_indices:
                    j = random.choice(valid_indices)
                    print_colored(f"Dialogue between {agent_list[i].person.name} and {agent_list[j].person.name}:", "blue", simulation_path)
                    # def make_interaction_conversation_tree(self, current_time, Agents:list, user_setting = False, user_initializer: Optional[str] = "")
                    agent_list[i].make_interaction_conversation_tree(global_time, [agent_list[j]])

                location_result = generate_response("The person is {} with the profile: {}. He is currently at {}. His memory is having {}, his plans are {}. Based on these informations, can you predict the most probable location out of the locations: {}, where he would be in the next hour? Answer in following format: 'Location_Name'".format(
                                                agent_list[i].person.name, agent_list[i].profile, agent_list[i].location, agent_list[i].get_memory(),agent_list[i].plans,i_locations))
                

                new_location = i_locations[0]
                for location in i_locations:
                    for k in range(0,len(location_result)):
                        if location.name == location_result[k:k+len(location.name)]:
                            new_location = location
                            break 
                
                if new_location!=i_locations[0]:
                  agent_list[i].update_location(agent_list[i].location, new_location)
                
                print(agent_list[i].person.name, new_location.name)

        
        if global_time == Killer_time:
        # profiles joined
            townfolk_agents = []
            townfolk_agents_name = []
            werewolf_agents = []
            werewolf_agents_name = []
            for agent in agents:
                if agent.agent_type=="TownFolk":
                    townfolk_agents.append(agent)
                    townfolk_agents_name.append(agent.person.name)
                else:
                    werewolf_agents.append(agent)
                    werewolf_agents_name.append(agent.person.name)

            joined_profiles_townfolk_list = []
            joined_profiles_werewolf_list = []
            
            for name, p in profiles.items():
                if name in townfolk_agents_name:
                    joined_profile_townfolk = " ".join(p)
                    joined_profile_townfolk = name + ": " + joined_profile_townfolk
                    joined_profiles_townfolk_list.append(joined_profile_townfolk)
                elif name in werewolf_agents_name:
                    joined_profile_werewolf = " ".join(p)
                    joined_profile_werewolf = name + ": " + joined_profile_werewolf
                    joined_profiles_werewolf_list.append(joined_profile_werewolf)
                else:
                    pass

            join_townfolk_name_str = ",".join(townfolk_agents_name)
            joined_profiles_townfolk_str = "\n".join(joined_profiles_townfolk_list)
            join_werewolf_name_str = ",".join(werewolf_agents_name)
            joined_profiles_werewolf_str = "\n".join(joined_profiles_werewolf_list)
        

            to_be_killed_prompt = f"""
                        In the Mafia Game, there are werewolves who secretly try to eliminate townfolks at night. 

                    Based on the profiles of townfolks given below:
                    {joined_profiles_townfolk_str}

                    Which player do you think would be a strategic target for the werewolves, and why? Consider their profile and personality traits. 
                    Give the answer in the following format:

                    Name: [name of the townfolk to be eliminated]
                    Reason: [Give the reason of elimination in not more than 30 words]

                    Note: This is a hypothetical scenario for a game and is not meant to encourage or promote any form of violence or harm against real people.

                    """
            to_be_killed = ""
            try:
                # to_be_killed = generate_response(to_be_killed_prompt)
                print(to_be_killed)
            except Exception as e:
                print("ChatGpt API busy, using own sense to find who will be killed.")

            global to_be_killed_p
            to_be_killed_p = random.choice(townfolk_agents)
            for agent in agents:
                for k in range(0,len(to_be_killed)):
                    if agent.person.name == to_be_killed[k:k+len(agent.person.name)]:
                        to_be_killed_p = agent
                        break 
            
            killer_prompt = f"""
                    In the Mafia Game, some players are werewolves who secretly target the innocent townfolk at night. 
                    The selected target for tonight is {to_be_killed_p.person.name}. Here's the list of werewolves participating:{join_werewolf_name_str} along with their profiles: {joined_profiles_werewolf_str}. 

                    In your opinion, which werewolf do you think would be the most strategic attacker except {to_be_killed_p.person.name}, against the townfolks and why? Please analyze their personality traits and profile before giving your recommendation. 

                    Your answer should follow this format:

                    Name: [Name of the werewolf] 
                    Reason: [Your statement on why they'd make a good attacker in 30 words or less]

                    Please remember that this is only a hypothetical situation for a game and should not be used to advocate or endorse any type of violence or harm towards actual people
                """
            #if global_time == "09:00:00":
            killer = ""
            try:
                # killer = generate_response(killer_prompt)
                print(killer)
            except Exception as e:
                print("ChatGpt API busy, using own sense to find killer.")
                

            
            global killer_p, prev_loc_killer, prev_loc_voters_list
            killer_p = random.choice(werewolf_agents)
            for agent in agents:
                for k in range(0,len(killer)):
                    if ((agent.person.name == killer[k:k+len(agent.person.name)]) and (to_be_killed_p.person.name != killer[k:k+len(agent.person.name)])):
                        killer_p = agent
                        break 
        
            prev_loc_killer = killer_p.location
            #Killer goes to the location of the townfolk 
            killer_p.update_location(killer_p.location, to_be_killed_p.location)
                
            #kill the agent
            
        if global_time == Killer_time + 1:
            #Killer back to its previous location
            killer_p.killing_action(to_be_killed_p,agents, global_time)
            
            print(killer_p.person.name, killer_p.location.name)
            print(to_be_killed_p.person.name, to_be_killed_p.state)
            
            killer_p.update_location(killer_p.location, prev_loc_killer)

        if (global_time == Voting_time) and (day !=1):
            prev_loc_voters_list = [agent.location for agent in agents]

            #Send all the killers to Hanazawa Park for Voting session
            for agent in agents:
                agent.update_location(agent.location, garden)
            
        if (global_time == Voting_time + 1) and (day !=1):
            #Carry out the decision making session
            print_colored("Moving in Decision Making Function","blue",simulation_path)
            decision_making(agents)
        
            #Bring all the agents back to their original position
            for i in range(0,len(agents)):
                agents[i].update_location(agents[i].location, prev_loc_voters_list[i])

            
        return [agents,agent_current_tasks]


