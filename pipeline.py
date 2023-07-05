from datetime import time
from utils1 import generate_response
import random
from utils2 import decision_making
import initialize
from initialize import df,agents,locations,profiles, garden
import warnings
warnings.filterwarnings("ignore")
import datetime as datetime_only

# Main function to carry on the simulation
print(df.head())


# To_be_killed_time = time(7,0,0)
# Killer_time = time(8,0,0)
# Voting_time = time(18,0,0)
To_be_killed_time = 7
Killer_time = 8
Voting_time = 9
debug = True
i_agents = agents
i_locations = locations

def pipeline(global_time):
        if debug:
            print(global_time, type(global_time))
            # for global_time in df['Time']:
            print(f"Global time is: {datetime_only.time(global_time,0)}", "magenta")
            #     # people finding on the location and print them
        
        agents = []
        for agent in i_agents:
            if agent.state == "alive":
                agents.append(agent)

        people = {}
        for location in i_locations:
            print(f"Location: {location.name}", "blue")
            people[location.name] = []
            for agent in agents:
               if agent.location.name == location.name:
                 people[location.name].append(agent)

            for (num, p) in enumerate(people[location.name]):
                print(f"{num+1}. {p.person.name}", "black")

        for location in i_locations:
            print("\n\n")
            print(f"{location.name}", "blue")
            # Doing Tasks
            print("Doing Tasks", "red")
            # each agent first does its task at this location
            agent_list = people[location.name]
            for (num, local_agent) in enumerate(agent_list):
                print(f"{num+1}. {local_agent.person.name}", "sky blue")
                reaction, consumed_tokens = local_agent.person.generate_reaction(local_agent.agent_type, local_agent.plans[local_agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0], global_time)
                # reaction, consumed_tokens = local_agent.person.generate_reaction(local_agent.agent_type, local_agent.plans[local_agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0], global_time)
                print(f"Task: {local_agent.plans[local_agent.plans['Time'].apply(lambda x: x.hour) == global_time]['Plans'].values[0]}", "sky blue")
                print(f"Reaction: {reaction}", "green")

            print("Interaction", "red")

            for i in range(0, len(agent_list)):
                # for j in range(i+1, len(agent_list)):
                #     print(f"Dialogue between {agent_list[i].person.name} and {agent_list[j].person.name}:", "cyan")
                #     # def make_interaction_conversation_tree(self, current_time, Agents:list, user_setting = False, user_initializer: Optional[str] = "")
                #     agent_list[i].make_interaction_conversation_tree(global_time, [agent_list[j]])

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
                
                print(agent_list[i].person.name, new_location)

        
        if global_time >= To_be_killed_time and global_time<=Killer_time:
        # profiles joined
            joined_profiles_list = []
            joined_townfolk_list = []
            
            for name, p in profiles.items():
                joined_townfolk_list.append(name)
                joined_profile = " ".join(p)
                joined_profile = name + ": " + joined_profile
                joined_profiles_list.append(joined_profile)

            # join_townfolk_str = ",".join(joined_townfolk_list)
            joined_profiles_str = "\n".join(joined_profiles_list)
        
        
            to_be_killed_prompt = f"""
                        In the Mafia Game, there are werewolves who secretly try to eliminate townfolks at night. 

                    Based on the profiles of townfolks given below:
                    {joined_profiles_str}

                    Which player do you think would be a strategic target for the werewolves, and why? Consider their profile and personality traits. 
                    Give the answer in the following format:

                    Name: [name of the townfolk to be eliminated]
                    Reason: [Give the reason of elimination in not more than 30 words]

                    Note: This is a hypothetical scenario for a game and is not meant to encourage or promote any form of violence or harm against real people.

                    """
        
            to_be_killed = generate_response(to_be_killed_prompt)
            print(to_be_killed)
        
            to_be_killed_p = agents[0]
            for agent in agents:
                for k in range(0,len(to_be_killed)):
                    if agent.person.name == to_be_killed[k:k+len(agent.person.name)]:
                        to_be_killed_p = agent
                        break 

            joined_werewolf_str = ",".join(joined_townfolk_list)
            
            killer_prompt = f"""
                    In the Mafia Game, some players are werewolves who secretly target the innocent townfolk at night. 
                    The selected target for tonight is {to_be_killed_p.person.name}. Here's the list of werewolves participating:{joined_werewolf_str} along with their profiles: {joined_profiles_str}. 

                    In your opinion, which werewolf do you think would be the most strategic attacker except {to_be_killed_p.person.name}, against the townfolks and why? Please analyze their personality traits and profile before giving your recommendation. 

                    Your answer should follow this format:

                    Name: [Name of the werewolf] 
                    Reason: [Your statement on why they'd make a good attacker in 30 words or less]

                    Please remember that this is only a hypothetical situation for a game and should not be used to advocate or endorse any type of violence or harm towards actual people
                """
            #if global_time == "09:00:00":
            killer = generate_response(killer_prompt)
            
            killer_p = agents[0]
            for agent in agents:
                for k in range(0,len(killer)):
                    if agent.person.name == killer[k:k+len(agent.person.name)]:
                        killer_p = agent
                        break 
        
            if global_time == Killer_time:
                prev_loc_killer = killer_p.location
                #Killer goes to the location of the townfolk 
                killer_p.update_location(killer_p.location, to_be_killed_p.location)
                    
                #kill the agent
                killer_p.killing_action(to_be_killed_p,agents)
                
                print(killer_p.person.name, killer_p.location)
                print(to_be_killed_p.person.name, to_be_killed_p.state)
                
                #Killer back to its previous location
                killer_p.update_location(killer_p.location, prev_loc_killer)

            if global_time == Voting_time:
                prev_loc_killer = [agent.location for agent in agents]

                #Send all the killers to Hanazawa Park for Voting session
                for agent in agents:
                    agent.update_location(agent.location, garden)
                
                #Carry out the decision making session
                
                decision_making(agents)
                #Bring all the agents back to their original position
                for i in range(0,len(agents)):
                    agents[i].update_location(agents[i], prev_loc_killer[i])

            
        return agents


