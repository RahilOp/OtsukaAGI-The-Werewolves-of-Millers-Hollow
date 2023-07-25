# OtsukaAGI: The Werewolves of Millers Hollow

Welcome to "The Werewolves of Millers Hollow," an extraordinary autosimulative game that takes inspiration from the popular concept of AmongUs, but with a captivating twist! In this enthralling game, the participants are not ordinary players; they are autonomous agents, brought to life using the groundbreaking OtsukaAGI framework.

Within the quaint village of Hayashino, both the gentle Townfolks and the cunning Werewolves coexist. The Townfolks have two objectives: either complete their assigned tasks or unite their forces to identify and eliminate the sly Werewolves through a democratic voting process. On the other hand, the mischievous Werewolves endeavor to eliminate one unsuspecting Townfolk each night until their numbers match.

As the game unfolds, the OtsukaAGI-created agents take center stage, demonstrating their unique traits, interactions, and strategic decision-making abilities. The Townfolks collaborate to protect their community, while the Werewolves employ their wit to create chaos and remain hidden amidst the shadows.

Embrace the thrilling experience of witnessing autonomous agents engage in an autosimulative adventure like never before! Explore the intricate dynamics, unravel the mysteries, and immerse yourself in the world of "The Werewolves of Millers Hollow," where artificial intelligence meets suspenseful gameplay.

<img src = "/static/env.png">

## OtsukaAGI - Agent Attributes:

1. **Memory**: This component is based on the modified GameGenerativeMemory class inherited from Langchain.
   - `llm`: The engine used by the agent to generate responses.
   - `memory_retriever`: The retriever responsible for extracting information from the agent's memory.
   - `verbose`: Provides additional details regarding the LLM's response.
   - `reflection_threshold`: Determines the threshold for generating reflections based on the agent's memory.
   - `file_path`: Specifies the file path containing the agent's memory, serving various purposes.

2. **Person**: This component is based on the modified GameGenerativeAgent class inherited from Langchain.
   - `name`: The name of the agent.
   - `age`: The agent's age as an integer.
   - `traits`: Describes the unique traits of the agent.
   - `status`: Reflects the agent's current situation or status.
   - `memory_retriever`: The retriever responsible for extracting information from the agent's memory.
   - `llm`: The engine used by the agent to generate responses.
   - `file_path`: Specifies the file path containing the agent's memory, serving various purposes.
   - `memory`: A reference to the agent's memory.

3. **Agent_Type**: This component categorizes agents based on their distinct characteristics, such as TownFolks and WereWolfs.

4. **Profile**: A string describing the character of the agent.

5. **Relations**: A dictionary of strings describing the agent's interactions with other agents in the environment.

6. **Plans**: Specifies the basic plans of the agent, including its daily routine.

7. **State**: Determines whether the agent is in an "alive" or "dead" state.

8. **Location**: Represents the current location of the agent as an object of the Place class.

9. **View**: Specifies the radius of the agent's field of view in the environment.

10. **Score**: Represents the number of tasks completed by the agent.

## OtsukaAGI - Agent Methods:

1. **get_memory()**: Returns the complete memory as a string.

2. **get_mem_summary()**: Provides a concise summary from the memory that is most relevant, important, and recent in relation to the input prompt.
   - `recency`: A value indicating the age of the memory point.
   - `relevance`: A value indicating the extent to which the prompt is relevant to the memory point.
   - `importance`: A value indicating the significance of the prompt with respect to the memory point.

3. **make_interaction_conversation_tree()**: Executes an interaction between our agents within a well-defined context.

4. **make_interaction()**: Performs a general, less-contextualized interaction between the agents.

5. **draw()**: Renders the agents on the pygame display.

6. **update_location()**: Updates the agent's location object.

7. **move_agent()**: Facilitates the movement of agents from one location to another.

8. **killing_action()**: Executes the process of the WereWolf killing Townfolks.


## OtsukaAGI - Place Attributes:

1. **history**: This component is based on the modified GameGenerativeMemory class inherited from Langchain.
   - `llm`: The engine used by the agent to generate responses.
   - `memory_retriever`: The retriever responsible for extracting information from the agent's memory.
   - `verbose`: Provides additional details regarding the LLM's response.
   - `reflection_threshold`: Determines the threshold for generating reflections based on the agent's memory.

2. Information about the Locations
   - `name`: The name of the location.
   - `description`: Description of the location.
   - `objects`: Objects present in the internal view of the location.
   - `file_path`: Specifies the file path containing the location's history, serving various purposes.
   - `sabotage_memory`: Memory used to hold the information about the tasks which have been sabotaged.


## OtsukaAGI - Place Methods:

1. **add_history()**: Method to add the history or information about the location.


All of the methods and attributes above are inherited from OtsukaAGI, while some of them are defined as per the requirement of the simulation, viz. draw(), killing_action(), sabotage_memory, etc.


