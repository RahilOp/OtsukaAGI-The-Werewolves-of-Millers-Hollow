from utils1 import generate_response
from langchain.agents import Tool

def decision_making(agents):
    # start a group conversation 
    summaries = {}
    for agent in agents:
        ag_sum = agent.get_mem_summary("Memories related to elimination of the agent and sabotaging of the tasks.")
        summaries[agent.person.name] = ag_sum
    
    joint_agent_memories = []

    for agent in agents:
        joint_agent_memories.append(agent.person.name + ':' + summaries[agent.person.name])
    
    temp_agents = [agent for agent in agents]
    while len(temp_agents)!=0:
        
        if len(temp_agents) == len(agents):
          next_agent = generate_response(f"Here is the {joint_agent_memories} list where each agent has its memories corresponding to its name. Select an agent from the given list which must start speaking so that it ends in a better conversation.")
        else:
          next_agent = generate_response(f"Here is the {joint_agent_memories} list where each agent has its memories corresponding to its name. Select an agent from the given list which must start speaking so that it ends in a better conversation.")
        
        # parse the next agent's object so that we can make it speaking
        
        next_agent_obj = temp_agents[0]
        for agent in temp_agents:
            for k in range(0,len(next_agent)):
                if agent.person.name == next_agent[k:k+len(agent.person.name)]:
                    next_agent_obj = agent
                    break
        
        print(next_agent_obj.person.name)

        continue_convo, next_message = next_agent_obj.person.generate_dialogue_response("Tell at max 5 observations or points about whom you think is the Werewolf and needs to be eliminated with proper reasoning.")

        print(next_message)

        for agent in temp_agents:
            agent.memory.add_memory(next_message)
          
        # agent has been removed from the list
        temp_agents.remove(next_agent_obj)
    
    # After everyone has dicussed and contributed its point in the memory

    summaries_for_voting = {}
    votes = {}
    for agent in agents:
        ag_sum = agent.get_mem_summary("Who do you think you will vote to eliminate as a WereWolf i.e. one who has eliminated townfolks and sabotaged the tasks.")
        summaries_for_voting[agent.person.name] = ag_sum
        votes[agent.person.name] = 0
    
    # carry out the voting session

    for agent in agents:
        voted = generate_response(f"Here is your memory related to voting: {summaries_for_voting[agent.person.name]} and here is the agent list {agents}. Select an agent from the given list except {agent.person.name} whom you think is the werewolf and nees to be eliminated.")
        
        # parse the next agent's object so that we can make it speaking
        voted_name = ""
        for agent in temp_agents:
            for k in range(0,len(voted)):
                if agent.person.name == voted[k:k+len(agent.person.name)]:
                    voted_name = agent.person.name
                    break
        
        print(voted_name)

        if voted_name != "":
          votes[voted_name]+=1
    
    # to extract the agent with the maximum code
    
    to_be_eliminated = agents[0]
    mx = 0
    for agent in agents:
        print(agent.person.name,": ",votes[agent.person.name])
        if votes[agent.person.name] > mx:
            to_be_eliminated = agent
            mx = votes[agent.person.name]
    
    print(f"{to_be_eliminated.person.name} has been eliminated with {mx} votes.")
    
    # the agent's state has been updated
    to_be_eliminated.state = "dead"



def initialise_conversation_tools(agent_type):
  template_werewolf_initialise_dialogue_tool = """
In the game of "werewolves of Miller Hollow", It is used when you are a Werewolf and Opposite Agent is Townfolk. It is useful when you want to deceive or mislead Townfolk from the fact that you are Werewolf.

It is useful to start dialogue based on:
1. your current plans and current plans of opposite agent.
2. your relations with opposite agent.
3. your reaction to the current plan of opposite agent.

It is also useful when you want to deceive or mislead Townfolk from the fact that you are Werewolf.

These are some of the examples for the Werewolf Initialise Dialogue Tool.
You: Takashi Yamamoto
Your Agent Type: Werewolf
Your Current Plan: helping out customers with groceries and other necessities.
Opposite Agent: Satoshi Takahashi
Opposite Agent Type: Townfolk
Opposite Agent Current Plan: visiting the Shino Grocery Store.
Your Relations With Opposite Agent: Takashi Yamamoto thinks that Satoshi Takahashi is not a good candidate for contesting local mayor elections. \
                                    Satoshi Takahashi is a regular customer at Shino Grocery store.
Your Reaction to Current Plan of Opposite Agent: Satoshi needs some help in finding some item. I do not need to ask anything that is related to fact that I am Werewolf.
Question: Hi Satoshi-san, How can I help you with?

You: Yusuke Mori
Your Agent Type: Werewolf
Your Current Plan: Yusuke Mori wakes up and completes the morning routine.
Opposite Agent: Yumi Yamamoto
Opposite Agent Type: Townfolk
Opposite Agent Current Plan: Yumi engages in house chores, tending to various tasks around the home.
Your Relations With Opposite Agent: Yumi Yamamoto and Yusuke Mori have good relations with each other. But their political thinking does not match. Yumi Yamamoto thinks Satoshi Takahashi is not an ideal candidate for the local mayor elections. Yusuke Mori thinks that Satoshi Takahashi is an ideal candidate for the local mayor elections.
Your Reaction to Current Plan of Opposite Agent: I should know the views of Yumi on elections.  I do not need to ask anything that is related to fact that I am Werewolf.
Question: By the way Yumi, What are views on upcoming local mayor elections?
  """

  template_werewolf_continue_dialogue_tool = """
It is used when you are a Werewolf and Opposite Agent is Townfolk. It is also useful when you want to deceive or mislead Townfolk from the fact that you are Werewolf.

It is useful to continue dialogue based on:
1. previous response of opposite agent.
2. your current plans and current plans of opposite agent.
3. your relations with opposite agent.
4. your reaction to the previous response of opposite agent.


These are some of the examples for the Townfolk Continue Dialogue Tool.
You: Satoshi Takahashi
Your Agent Type: Werewolf
Your Current Plan: visiting the Shino Grocery Store.
Opposite Agent: Takashi Yamamoto
Opposite Agent Type: Townfolk
Opposite Agent Current Plan: helping out customers with groceries and other necessities.
Opposite Agent Previous Response: Satoshi-san, Can I ask you where you have been at last evening?
Your Relations With Opposite Agent: Satoshi Takahashi does not like Takashi Yamamoto because of the differences in their political ideologies. \
Takashi Yamamoto thinks that Satoshi Takahashi is not an ideal candidate for the local mayor elections.
Your Reaction to Previous Response of Opposite Agent: I think Takashi is inquiring about the killing of Kazuki that was done by me yesterday and has suspicion on me being a Werewolf.
Response: As far I remember, I was at Hanazawa Park on a evening walk with Ayumi-san.

You: Yumi Yamamoto
Your Current Plan: Yumi engages in house chores, tending to various tasks around the home.
Your Agent Type: Werewolf
Opposite Agent: Yusuke Mori
Opposite Agent Type: Townfolk
Opposite Agent Current Plan: Yusuke Mori wakes up and completes the morning routine.
Opposite Agent Previous Response: By the way Yumi, What are views on upcoming local mayor elections?
Your Relations With Opposite Agent: Takashi Yamamoto (husband of Yumi Yamamoto) calls Yusuke Mori only for repairing furniture or for creating new wooden pieces. \
Sometimes Yumi meets Yusuke meet each other at Mizukami Shrine and have small conversations.
Your Reaction to Previous Response of Opposite Agent: I should put forward my views of Ayumi Kimura being a ideal candidate for election with Yusuke and know what are his views? It is not related to the fact that I am Werewolf.
Response: I think Ayumi Kimura is doing great and could a potential candidate. What do you think?

Note: Agent cannot talk about ownself in third tense. The dialogue of agent about own should be in first form of tense. 
        """

  template_werewolf_end_dialogue_tool = """
In the game of "werewolves of Miller Hollow", It is useful to end dialogue based on:
1. previous response of opposite agent.
2. your current plans and current plans of opposite agent.
3. your relations with opposite agent.
4. your reaction to the previous response of opposite agent.
5. you should end conversations after 4 to 5 replies.

These are some of the examples for the Townfolk Continue Dialogue Tool.
You: Satoshi Takahashi
Your Current Plan: visiting the Shino Grocery Store.
Opposite Agent: Takashi Yamamoto
Opposite Agent Current Plan: helping out customers with groceries and other necessities.
Opposite Agent Previous Response: Vagabond comic is there at the side rack of the shop.
Reply Count = 2
Your Relations With Opposite Agent: Satoshi Takahashi does not like Takashi Yamamoto because of the differences in their political ideologies. \
Takashi Yamamoto thinks that Satoshi Takahashi is not an ideal candidate for the local mayor elections.
Your Reaction to Current Plan of Opposite Agent: I think I have found the magazine and I should end the dialogue.
Response: Thank you Takashi-san, have a nice day.

You: Yumi Yamamoto
Your Current Plan: Yumi engages in house chores, tending to various tasks around the home.
Opposite Agent: Yusuke Mori
Opposite Agent Current Plan: Yusuke Mori wakes up and completes the morning routine.
Opposite Agent Previous Response: I am going to shrine after a while, would you join?
Reply Count = 3
Your Relations With Opposite Agent: Takashi Yamamoto (husband of Yumi Yamamoto) calls Yusuke Mori only for repairing furniture or for creating new wooden pieces. \
Sometimes Yumi meets Yusuke meet each other at Mizukami Shrine and have small conversations.
Your Reaction to Current Plan of Opposite Agent: Going to shrine with Yusuke is not a problem, I should join with him.
Your Reaction to Current Plan of Opposite Agent: Sure, thats a great idea Yusuke-san, lets go.


Note that you should try to end the conversation as soon as possible after the Reply Count variable becomes 3.
        """

  template_werewolf_team_initialise_dialogue_tool = """
It is useful to start dialogue based on:
1. your current plans and current plans of opposite agent.
2. your relations with opposite agent.
3. your reaction to the current plan of opposite agent.

These are some of the examples for the Townfolk Initialise Dialogue Tool.
You: Takashi Yamamoto
Your Current Plan: helping out customers with groceries and other necessities.
Opposite Agent: Satoshi Takahashi
Opposite Agent Current Plan: visiting the Shino Grocery Store.
Your Relations With Opposite Agent: Takashi Yamamoto thinks that Satoshi Takahashi is not a good candidate for contesting local mayor elections. \
                                    Satoshi Takahashi is a regular customer at Shino Grocery store.
Your Reaction to Current Plan of Opposite Agent: Satoshi needs some help in finding some item.
Question: Hi Satoshi-san, How can I help you with?

You: Yusuke Mori
Your Current Plan: Yusuke Mori wakes up and completes the morning routine.
Opposite Agent: Yumi Yamamoto
Opposite Agent Current Plan: Yumi engages in house chores, tending to various tasks around the home.
Your Relations With Opposite Agent: Yumi Yamamoto and Yusuke Mori have good relations with each other. But their political thinking does not match. Yumi Yamamoto thinks Satoshi Takahashi is not an ideal candidate for the local mayor elections. Yusuke Mori thinks that Satoshi Takahashi is an ideal candidate for the local mayor elections.
Your Reaction to Current Plan of Opposite Agent: I should know the views of Yumi on elections.
Question: By the way Yumi, What are views on upcoming local mayor elections?
        """

  template_werewolf_team_continue_dialogue_tool = """
useful to continue dialogue based on:
1. previous response of opposite agent.
2. your current plans and current plans of opposite agent.
3. your relations with opposite agent.
4. your reaction to the previous response of opposite agent.

These are some of the examples for the Townfolk Continue Dialogue Tool.
You: Satoshi Takahashi
Your Current Plan: visiting the Shino Grocery Store.
Opposite Agent: Takashi Yamamoto
Opposite Agent Current Plan: helping out customers with groceries and other necessities.
Opposite Agent Previous Response: Hi Satoshi-san, How can I help you with?
Your Relations With Opposite Agent: Satoshi Takahashi does not like Takashi Yamamoto because of the differences in their political ideologies. \
Takashi Yamamoto thinks that Satoshi Takahashi is not an ideal candidate for the local mayor elections.
Your Reaction to Previous Response of Opposite Agent: I dont want to engage in conversation with Takashi but I should have some casual dialogue.
Response: Nothing, I was here to buy the latest edition of Vagabond Comic.

You: Yumi Yamamoto
Your Current Plan: Yumi engages in house chores, tending to various tasks around the home.
Opposite Agent: Yusuke Mori
Opposite Agent Current Plan: Yusuke Mori wakes up and completes the morning routine.
Opposite Agent Previous Response: By the way Yumi, What are views on upcoming local mayor elections?
Your Relations With Opposite Agent: Takashi Yamamoto (husband of Yumi Yamamoto) calls Yusuke Mori only for repairing furniture or for creating new wooden pieces. \
Sometimes Yumi meets Yusuke meet each other at Mizukami Shrine and have small conversations.
Your Reaction to Previous Response of Opposite Agent: I should put forward my views of Ayumi Kimura being a ideal candidate for election with Yusuke and know what are his views?
Response: I think Ayumi Kimura is doing great and could a potential candidate. What do you think?

Note: Agent cannot talk about ownself in third tense. The dialogue of agent about own should be in first form of tense. 
        """

  template_werewolf_team_end_dialogue_tool = """
In the game of 'Werewolves of Miller Hollow', It is useful to end dialogue based on:
1. previous response of opposite agent.
2. your current plans and current plans of opposite agent.
3. your relations with opposite agent.
4. your reaction to the previous response of opposite agent.
5. you should end conversations after 4 to 5 replies.

These are some of the examples for the Townfolk Continue Dialogue Tool.
You: Satoshi Takahashi
Your Current Plan: visiting the Shino Grocery Store.
Opposite Agent: Takashi Yamamoto
Opposite Agent Current Plan: helping out customers with groceries and other necessities.
Opposite Agent Previous Response: Vagabond comic is there at the side rack of the shop.
Reply Count: 2
Your Relations With Opposite Agent: Satoshi Takahashi does not like Takashi Yamamoto because of the differences in their political ideologies. \
Takashi Yamamoto thinks that Satoshi Takahashi is not an ideal candidate for the local mayor elections.
Your Reaction to Current Plan of Opposite Agent: I think I have found the magazine and I should end the dialogue.
Response: Thank you Takashi-san, have a nice day.

You: Yumi Yamamoto
Your Current Plan: Yumi engages in house chores, tending to various tasks around the home.
Opposite Agent: Yusuke Mori
Opposite Agent Current Plan: Yusuke Mori wakes up and completes the morning routine.
Opposite Agent Previous Response: I am going to shrine after a while, would you join?
Reply Count: 3
Your Relations With Opposite Agent: Takashi Yamamoto (husband of Yumi Yamamoto) calls Yusuke Mori only for repairing furniture or for creating new wooden pieces. \
Sometimes Yumi meets Yusuke meet each other at Mizukami Shrine and have small conversations.
Your Reaction to Current Plan of Opposite Agent: Going to shrine with Yusuke is not a problem, I should join with him.
Your Reaction to Current Plan of Opposite Agent: Sure, thats a great idea Yusuke-san, lets go.

Note that you should try to end the conversation as soon as possible after the Reply Count variable becomes 3.
        """

  template_townfolk_initialise_dialogue_tool = """
It is useful to start dialogue based on:
1. your current plans and current plans of opposite agent.
2. your relations with opposite agent.
3. your reaction to the current plan of opposite agent.

These are some of the examples for the Townfolk Initialise Dialogue Tool.
You: Takashi Yamamoto
Your Current Plan: helping out customers with groceries and other necessities.
Opposite Agent: Satoshi Takahashi
Opposite Agent Current Plan: visiting the Shino Grocery Store.
Your Relations With Opposite Agent: Takashi Yamamoto thinks that Satoshi Takahashi is not a good candidate for contesting local mayor elections. \
                                    Satoshi Takahashi is a regular customer at Shino Grocery store.
Your Reaction to Current Plan of Opposite Agent: Satoshi needs some help in finding some item.
Question: Hi Satoshi-san, How can I help you with?

You: Yusuke Mori
Your Current Plan: Yusuke Mori wakes up and completes the morning routine.
Opposite Agent: Yumi Yamamoto
Opposite Agent Current Plan: Yumi engages in house chores, tending to various tasks around the home.
Your Relations With Opposite Agent: Yumi Yamamoto and Yusuke Mori have good relations with each other. But their political thinking does not match. Yumi Yamamoto thinks Satoshi Takahashi is not an ideal candidate for the local mayor elections. Yusuke Mori thinks that Satoshi Takahashi is an ideal candidate for the local mayor elections.
Your Reaction to Current Plan of Opposite Agent: I should know the views of Yumi on elections.
Question: By the way Yumi, What are views on upcoming local mayor elections?
        """

  template_townfolk_continue_dialogue_tool = """
useful to continue dialogue based on:
1. previous response of opposite agent.
2. your current plans and current plans of opposite agent.
3. your relations with opposite agent.
4. your reaction to the previous response of opposite agent.

These are some of the examples for the Townfolk Continue Dialogue Tool.
You: Satoshi Takahashi
Your Current Plan: visiting the Shino Grocery Store.
Opposite Agent: Takashi Yamamoto
Opposite Agent Current Plan: helping out customers with groceries and other necessities.
Opposite Agent Previous Response: Hi Satoshi-san, How can I help you with?
Your Relations With Opposite Agent: Satoshi Takahashi does not like Takashi Yamamoto because of the differences in their political ideologies. \
Takashi Yamamoto thinks that Satoshi Takahashi is not an ideal candidate for the local mayor elections.
Your Reaction to Previous Response of Opposite Agent: I dont want to engage in conversation with Takashi but I should have some casual dialogue.
Response: Nothing, I was here to buy the latest edition of Vagabond Comic.

You: Yumi Yamamoto
Your Current Plan: Yumi engages in house chores, tending to various tasks around the home.
Opposite Agent: Yusuke Mori
Opposite Agent Current Plan: Yusuke Mori wakes up and completes the morning routine.
Opposite Agent Previous Response: By the way Yumi, What are views on upcoming local mayor elections?
Your Relations With Opposite Agent: Takashi Yamamoto (husband of Yumi Yamamoto) calls Yusuke Mori only for repairing furniture or for creating new wooden pieces. \
Sometimes Yumi meets Yusuke meet each other at Mizukami Shrine and have small conversations.
Your Reaction to Previous Response of Opposite Agent: I should put forward my views of Ayumi Kimura being a ideal candidate for election with Yusuke and know what are his views?
Response: I think Ayumi Kimura is doing great and could a potential candidate. What do you think?

Note: Agent cannot talk about ownself in third tense. The dialogue of agent about own should be in first form of tense. 
        """
  template_townfolk_end_dialogue_tool = """
In the game of 'Werewolves of Miller Hollow', It is useful to end dialogue based on:
1. previous response of opposite agent.
2. your current plans and current plans of opposite agent.
3. your relations with opposite agent.
4. your reaction to the previous response of opposite agent.
5. you should end conversations after 4 to 5 replies.

These are some of the examples for the Townfolk End Dialogue Tool.
You: Satoshi Takahashi
Your Current Plan: visiting the Shino Grocery Store.
Opposite Agent: Takashi Yamamoto
Opposite Agent Current Plan: helping out customers with groceries and other necessities.
Opposite Agent Previous Response: Vagabond comic is there at the side rack of the shop.
Reply Count: 2
Your Relations With Opposite Agent: Satoshi Takahashi does not like Takashi Yamamoto because of the differences in their political ideologies. \
Takashi Yamamoto thinks that Satoshi Takahashi is not an ideal candidate for the local mayor elections.
Your Reaction to Current Plan of Opposite Agent: I think I have found the magazine and I should end the dialogue.
Response: Thank you Takashi-san, have a nice day.

You: Yumi Yamamoto
Your Current Plan: Yumi engages in house chores, tending to various tasks around the home.
Opposite Agent: Yusuke Mori
Opposite Agent Current Plan: Yusuke Mori wakes up and completes the morning routine.
Opposite Agent Previous Response: I am going to shrine after a while, would you join?
Reply Count: 3
Your Relations With Opposite Agent: Takashi Yamamoto (husband of Yumi Yamamoto) calls Yusuke Mori only for repairing furniture or for creating new wooden pieces. \
Sometimes Yumi meets Yusuke meet each other at Mizukami Shrine and have small conversations.
Your Reaction to Current Plan of Opposite Agent: Going to shrine with Yusuke is not a problem, I should join with him.
Your Reaction to Current Plan of Opposite Agent: Sure, thats a great idea Yusuke-san, lets go.


Note that you should try to end the conversation as soon as possible after the Reply Count variable becomes 3.
        """

  if agent_type=="TownFolk":
        tools = {
            "townfolk_initialise_dialogue_tool": Tool(
                        name = "Townfolk Initialise Dialogue Tool",
                        func=generate_response,
                        description = template_townfolk_initialise_dialogue_tool),
            "townfolk_continue_dialogue_tool": Tool(
                        name = "Townfolk Continue Dialogue Tool",
                        func=generate_response,
                        description = template_townfolk_continue_dialogue_tool),
            "townfolk_end_dialogue_tool": Tool(
                        name = "Townfolk End Dialogue Tool",
                        func=generate_response,
                        description = template_townfolk_end_dialogue_tool),
        }
        return tools
  else:
        tools = {
            "werewolf_initialise_dialogue_tool": Tool(
                        name = "Werewolf Initialise Dialogue Tool",
                        func=generate_response,
                        description = template_werewolf_initialise_dialogue_tool),
            "werewolf_continue_dialogue_tool": Tool(
                        name = "Werewolf Continue Dialogue Tool",
                        func=generate_response,
                        description = template_werewolf_continue_dialogue_tool),
            "werewolf_end_dialogue_tool": Tool(
                        name = "Werewolf End Dialogue Tool",
                        func=generate_response,
                        description = template_werewolf_end_dialogue_tool),
            "werewolf_team_initialise_dialogue_tool": Tool(
                        name = "Werewolf Team Initialise Dialogue Tool",
                        func=generate_response,
                        description = template_werewolf_team_initialise_dialogue_tool),
            "werewolf_team_continue_dialogue_tool": Tool(
                        name = "Werewolf Team Continue Dialogue Tool",
                        func=generate_response,
                        description = template_werewolf_team_continue_dialogue_tool),
            "werewolf_team_end_dialogue_tool": Tool(
                        name = "Werewolf Team End Dialogue Tool",
                        func=generate_response,
                        description = template_werewolf_team_end_dialogue_tool),
        }
        return tools
