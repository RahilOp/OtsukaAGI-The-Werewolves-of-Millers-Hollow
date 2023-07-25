# OtsukaAGI

Based on chat-gpt-3.5-turbo engine, OtsukaAGI is a framework powered by Otsuka Corporation, Tokyo, Japan, which can be used to develop generative agents
with proper Agent Avtar comprising of Profile, Plans and Relations.
We use Chat GPT LLM 

### OtsukaAGI - Agent
### Components present in the Agent:
__Memory:__ Based on the modified GameGenerativeMemory class inherited from Langchain. <br>
* llm: the engine which the agent uses to respond
* memory_retreiver: the retreiver which extracts information from the memory of the agent
* verbose: extra details with respect to the response of the LLM
* reflection_threshold: the threshold for the generations of reflections based on the memory of the agent
* file_path: path for the file which contains the memory of the agent which can be used for various purposes

__Person:__ Based on the modified GameGenerativeAgent class inherited from Langchain. <br>
* name: name of the agent
* age: age of the agent as an integer
* traits: traits of the agent
* status: agent's current situation or status
* memory_retreiver: the retreiver which extracts information from the memory of the agent
* llm: the engine which the agent uses to respond
* file_path: path for the file which contains the memory of the agent which can be used for various purposes
* memory: the reference to the memory of the agent

__Agent_Type:__ Type of the agent to declare agents having different characteristics. E.g: TownFolks and WereWolfs. <br>

__Profile:__ Description of the character of the agent as a string. <br>

__Relations:__ Description of the agent with other agents in the environment as a dictionary of string. <br>

__Plans:__ Basic plans of the agent i.e. the Daily routine. <br>

__State:__ Decides whether the agent is "alive" or "dead". <br>

__Location:__ Current location of the agent as an object of the Place class. <br>

__View:__ Radius of the field of view of the agent in the environment. <br>

__Score:__ Number of tasks being completed by the agent. <br>



