# OtsukaAGI: Professional Framework for Generative Agents

OtsukaAGI is an advanced framework, powered by Otsuka Corporation in Tokyo, Japan, and based on the chat-gpt-3.5-turbo engine. It offers developers the capability to create sophisticated generative agents with distinct Agent Avatars, comprising Profile, Plans, and Relations. The underlying engine utilized is Chat GPT LLM.

## OtsukaAGI - Agent Components:

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
