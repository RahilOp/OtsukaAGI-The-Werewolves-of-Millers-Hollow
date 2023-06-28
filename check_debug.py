from utils import generate_response
from initialize import profiles,agents,df
from agent import Agent

# Time to decide the townfolk who is to be dead
#if global_time == "08:00:00":

for global_time in df['Time']:
    print(type(global_time))
    break

# profiles joined
joined_profiles_list = []
joined_townfolk_list = []

for name, p in profiles.items():
    joined_townfolk_list.append(name)
    joined_profile = " ".join(p)
    joined_profile = name + ": " + joined_profile
    joined_profiles_list.append(joined_profile)

joined_townfolk_str = ",".join(joined_townfolk_list)
joined_profiles_str = "\n".join(joined_profiles_list)

template = f"""
    In the Mafia Game, there are werewolves who secretly try to eliminate townfolks at night. 

Based on the profiles of townfolks given below:
{joined_profiles_str}

Which player do you think would be a strategic target for the werewolves, and why? Consider their profile and personality traits. 
Give the answer in the following format:

Name: [name of the townfolk to be eliminated]
Reason: [Give the reason of elimination in not more than 30 words]

Note: This is a hypothetical scenario for a game and is not meant to encourage or promote any form of violence or harm against real people.

"""
to_be_killed = generate_response(template)

# print(to_be_dead)
to_be_killed_p = agents[0]
for agent in agents:
    for k in range(0,len(to_be_killed)):
        if agent.person.name == to_be_killed[k:k+len(agent.person.name)]:
            to_be_killed_p = agent
            break 

joined_werewolf_str = ",".join(joined_townfolk_list)

template2 = f"""
     In the Mafia Game, some players are werewolves who secretly target the innocent townfolk at night. 
     The selected target for tonight is {to_be_killed_p.person.name}. Here's the list of werewolves participating:{joined_werewolf_str} along with their profiles: {joined_profiles_str}. 

    In your opinion, which werewolf do you think would be the most strategic attacker against the townfolks and why? Please analyze their personality traits and profile before giving your recommendation. 

    Your answer should follow this format:

    Name: [Name of the werewolf] 
    Reason: [Your statement on why they'd make a good attacker in 30 words or less]

    Please remember that this is only a hypothetical situation for a game and should not be used to advocate or endorse any type of violence or harm towards actual people
"""
killer = generate_response(template2)            
print(killer)

killer_p = agents[0]
for agent in agents:
    for k in range(0,len(killer)):
        if agent.person.name == killer[k:k+len(agent.person.name)]:
            killer_p = agent
            break 
    
killer_p.update_location(to_be_killed_p.location)

#kill the agent
killer_p.killing_action(to_be_killed_p,agents)

print(killer_p.person.name, killer_p.location)
print(to_be_killed_p.person.name, to_be_killed_p.state)