import langchain
from langchain.experimental.generative_agents import GenerativeAgent, GenerativeAgentMemory
from utils1 import generate_response,print_colored
from utils2 import initialise_conversation_tools
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# import langchain
# from langchain.experimental.generative_agents import GenerativeAgent, GenerativeAgentMemory
# from utils import generate_response,print_colored

from pydantic import BaseModel, Field
from langchain.base_language import BaseLanguageModel
from langchain.prompts import PromptTemplate
from langchain import SerpAPIWrapper, LLMChain
import datetime as datetime_only
from customtemplate import CustomOutputParser, CustomPromptTemplate
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from datetime import date
import csv

class GameGenerativeAgent(BaseModel):
    """A character with memory and innate characteristics."""

    name: str
    """The character's name."""

    age: Optional[int] = None
    """The optional age of the character."""
    traits: str = "N/A"
    """Permanent traits to ascribe to the character."""
    status: str
    """The traits of the character you wish not to change."""
    memory: GenerativeAgentMemory
    """The memory object that combines relevance, recency, and 'importance'."""
    llm: BaseLanguageModel
    """The underlying language model."""

    #file path
    file_path:str

    verbose: bool = False
    summary: str = ""  #: :meta private:
    """Stateful self-summary generated via reflection on the character's memory."""

    summary_refresh_seconds: int = 3600  #: :meta private:
    """How frequently to re-generate the summary."""

    last_refreshed: datetime = Field(default_factory=datetime.now)  # : :meta private:
    """The last time the character's summary was regenerated."""

    daily_summaries: List[str] = Field(default_factory=list)  # : :meta private:
    """Summary of the events in the plan that the agent took."""

    debug: Optional[bool] = False


    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    # LLM-related methods
    @staticmethod
    def _parse_list(text: str) -> List[str]:
        """Parse a newline-separated string into a list of strings."""
        lines = re.split(r"\n", text.strip())
        return [re.sub(r"^\s*\d+\.\s*", "", line).strip() for line in lines]

    def chain(self, prompt: PromptTemplate) -> LLMChain:
        return LLMChain(
            llm=self.llm, prompt=prompt, verbose=self.verbose, memory=self.memory
        )

    def _get_entity_from_observation(self, observation: str) -> str:
        prompt = PromptTemplate.from_template(
            "What is the observed entity in the following observation? {observation}"
            + "\nEntity="
        )
        return self.chain(prompt).run(observation=observation).strip()

    def _get_entity_action(self, observation: str, entity_name: str) -> str:
        prompt = PromptTemplate.from_template(
            "What is the {entity} doing in the following observation? {observation}"
            + "\nThe {entity} is"
        )
        return (
            self.chain(prompt).run(entity=entity_name, observation=observation).strip()
        )

    def summarize_related_memories(self, observation: str) -> str:
        """Summarize memories that are most relevant to an observation."""
        prompt = PromptTemplate.from_template(
            """
{q1}?
Context from memory:
{relevant_memories}
Relevant context:
"""
        )
        entity_name = self._get_entity_from_observation(observation)
        entity_action = self._get_entity_action(observation, entity_name)
        q1 = f"What is the relationship between {self.name} and {entity_name}"
        q2 = f"{entity_name} is {entity_action}"
        return self.chain(prompt=prompt).run(q1=q1, queries=[q1, q2]).strip()

    def _generate_reaction(self, self_type: str, observation: str, call_to_action_template: str, current_time, tools_to_use: Optional[List], now: Optional[datetime] = None) -> Tuple[str, str, int]:
        """React to a given observation or dialogue act."""

        # customizing the _generate_reaction according to conversation tree
        # Define which tools the agent can use to answer user queries
        agent_summary_description = self.get_summary(now=now)
        relevant_memories_str = self.summarize_related_memories(observation)
        current_time_str = (
            datetime.now().strftime("%B %d, %Y, %I:%M %p")
            if now is None
            else now.strftime("%B %d, %Y, %I:%M %p")
        )

        current_time_string = datetime_only.time(current_time, 0)

        most_recent_memories_list = []
        l = len(self.memory.memory_retriever.memory_stream)
        for i in range(l-1, max(l-5, 0), -1):
          most_recent_memories_list.append(self.memory.memory_retriever.memory_stream[i].page_content)

        most_recent_memories = "\n".join(most_recent_memories_list)

        # Handling subprocess for generate_reaction()
        if(len(tools_to_use)==0):
          prompt = PromptTemplate.from_template(
              "You are playing Mafia Game in which there are some townfolks and werewolves. In this game you are currently playing role of {agent_name} who is a {agent_type}."
              +"\nIt is {current_time}."
              +"{agent_name}'s description:"
              +"{agent_summary_description}"
              + "\n{agent_name}'s status: {agent_status}"
              + "\nSummary of relevant context from {agent_name}'s memory:"
              + "\n{relevant_memories}"
              + "\nMost recent observations: {most_recent_memories}"
              + "\nObservation: {observation}"
              + "\n\n"
              + call_to_action_template
          )

          kwargs: Dict[str, Any] = dict(
            agent_summary_description=agent_summary_description,
            current_time=current_time_string,
            relevant_memories=relevant_memories_str,
            most_recent_memories = most_recent_memories,
            agent_name=self.name,
            agent_type = self_type,
            agent_status=self.status,
            observation=observation,
          )

          consumed_tokens = self.llm.get_num_tokens(
            prompt.format(**kwargs)
          )

          kwargs[self.memory.most_recent_memories_token_key] = consumed_tokens
          return None, self.chain(prompt=prompt).run(**kwargs).strip(), consumed_tokens

        # Set up the base template
        template = f"""
        You are playing Mafia Game in which there are some townfolks and werewolves. In this game you are currently playing role of {self.name} who is a {self_type}.

        Complete the objective as best you can. You have access to the following tools:
        {{tool_names}}

        Here is the desription of each tool along with some examples of its usage:
        {{tools}}

        It is {current_time_string} currently.

        {self.name}'s description:
        {agent_summary_description}

        {self.name}'s status: {self.status}

        Summary of relevant context from {self.name}'s memory:
        {relevant_memories_str}

        Most recent observations:
        {most_recent_memories}
       """

        template = template + call_to_action_template

        # print(template)
        prompt = CustomPromptTemplate(
            template=template,
            tools=tools_to_use,
            # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
            # This includes the `intermediate_steps` variable because that is needed
            input_variables=["input", "intermediate_steps"]
        )

        output_parser = CustomOutputParser()

        if (self.debug==True):
          print(prompt)

        # define tool usage logic based on Interaction Tree
        tool_names = [tool.name for tool in tools_to_use]
        agent = LLMSingleActionAgent(
            llm_chain = self.chain(prompt = prompt),
            output_parser=output_parser,
            stop=["\nObservation:"],
            allowed_tools=tool_names
        )

        agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools_to_use, verbose=True)

        kwargs: Dict[str, Any] = dict(
            observation=observation,
            input = "",
            tool_names = tool_names,
        )

        return_res = agent_executor.run(**kwargs)
        return_res["result"] = return_res["result"].strip()
        consumed_tokens = agent_executor.agent.llm_chain.llm.get_num_tokens(prompt.format(**kwargs))

        response_details = [date.today(), prompt, consumed_tokens, return_res]
        with open('tokens_history.csv','a') as tokens:
          writer = csv.writer(tokens)
          writer.writerow(response_details)

        kwargs[self.memory.most_recent_memories_token_key] = consumed_tokens
        if (self.debug==True):
          print(return_res)
        return return_res["tool_used"], return_res["result"], consumed_tokens

    def _clean_response(self, text: str) -> str:
        return re.sub(f"^{self.name} ", "", text.strip()).strip()

    def generate_reaction(self, self_type, observation: str, current_time, now: Optional[datetime] = datetime.now()) -> Tuple[str, int]:
            """React to a given observation.
            self, self_type: str, observation: str, call_to_action_template: str, current_time, tools_to_use: Optional[List], now: Optional[datetime] = None
            """
            # return "React: Do nothing", 700
            # call_to_action_template = (
            #     f"Should {self.name} react to the observation, and if so,"
            #     + f" what would be an appropriate reaction? Respond in one line."
            #     + f"write:\nREACT: {self.name}'s reaction (if anything)."
            #     + f"\nEither do nothing or react something.\n\n"
            # )
            return "No Reaction", 100
            call_to_action_template = (
                f"Should {self.name} react to the observation, and if so,"
                + " what would be an appropriate reaction? Respond in one line."
                + f"\nwrite:\nREACT: {self.name}'s reaction (if anything)."
                + "\nEither react or do nothing\n\n"
            )

            tools_to_use = []
            _, full_result, consumed_tokens = self._generate_reaction(
                self_type, observation, call_to_action_template, current_time, tools_to_use, now=now
            )

            result = full_result.strip().split("\n")[0]
            # AAA
            file = open(self.file_path, 'a')
            file.write(f"{self.name} observed {observation} and reacted by {result}")

            self.memory.save_context(
                {},
                {
                    self.memory.add_memory_key: f"{self.name} observed "
                    f"{observation} and reacted by {result}",
                    self.memory.now_key: now,
                },
            )
            if "REACT:" in result:
                reaction = self._clean_response(result.split("REACT:")[-1])
                return f"{self.name} {reaction}", consumed_tokens
            else:
                return result, consumed_tokens


    def initialise_dialogue_response(self, self_type, agent, current_plan_self:str, current_plan_agent:str, current_plan_reaction: str, current_time, tools_to_use, self_relations, user_setting = False, user_initializer: Optional[str] = "", now: Optional[datetime] = datetime.now()) -> Tuple[bool, str, int]:
        """Used to initialise the dialogue.
        Variables:
        agent, current_plan_reaction, current_time, tools_to_use, self_relations
        """
        agent_profile_summary = " ".join(agent.profile)
        if(user_setting==True):
          initializer = user_initializer
        else:
          initializer = f"How do I say to start conversation with {agent.person.name}?"


        call_to_action_template = (
            f"{self.name} wants to start conversation with {agent.person.name}.\n"
            +f"Profile of {agent.person.name}:\n"
            +f"{agent_profile_summary}.\n"
            +f'Current plan of {self.name}: {current_plan_self}.\n'
            +f'Current plan of {agent.person.name}: {current_plan_agent}.\n'
            +f'Reaction of {self.name} to Current Plan of {agent.person.name}: {current_plan_reaction}.\n'
            +f'Relations of {self.name} With {agent.person.name}: {self_relations[agent.person.name]}.\n\n'
            +f"Use the following format:\n"
            +"Question: the input question you must answer"
            +f"Thought: you should always think about what to do\n"
            +"Action: the action to take, should be one of [{tool_names}]\n"
            +"Action Input: the input to the action\n"
            +"Observation: the result of the action\n"
            +"\n\nBegin!\n"
            +f"Question: {user_initializer}\n"
            +"{agent_scratchpad}"
        )
      
        #  _generate_reaction(self, observation: str, call_to_action_template: str, current_time, tools_to_use, now: Optional[datetime] = None) -> Tuple[str, int]:
        tool_used, full_result, consumed_tokens = self._generate_reaction(self_type,
            current_plan_reaction, call_to_action_template, current_time, tools_to_use, now=now
        )

        # print(True, full_result, consumed_tokens)
        file = open(self.file_path, 'a')
        file.write(f"{self.name} observed {current_plan_agent} and said {full_result}")

        self.memory.save_context(
            {},
            {
                self.memory.add_memory_key: f"{self.name} observed "
                f"{current_plan_agent} and said {full_result}",
                self.memory.now_key: now,
            },
        )


        return True, full_result, consumed_tokens

    def generate_dialogue_response(
        self, self_type, agent, previous_response:str, previous_dialogue_response_reaction:str, current_plan_self:str, current_plan_agent:str, current_time, tools_to_use, self_relations, counter, now: Optional[datetime] = None) -> Tuple[bool, str, int]:
        """React to a given observation.
        Variables:
        self.agent_type, agent, dialogue_response, previous_dialogue_response_reaction, current_plan_self, current_plan_agent, current_time, tools_to_use, self.relations)

        """
        agent_profile_summary = " ".join(agent.profile)
        # call_to_action_template = (
        #     f"{self.name} is in conversation with {agent.person.name}. "
        #     +f'{agent.person.name} said to {self.name}: {observation}. '
        #     +f"What would {self.name} say?"
        #     +' write: SAY: "what to say"\n\n'
        #     +' Otherwise to end the conversation, write: GOODBYE: "what to say to end conversation".'
        # )

        call_to_action_template = (
            f"{self.name} is in conversation with {agent.person.name} where previous response of {agent.person.name} is given below.\n"
            +f"Profile of {agent.person.name}:\n"
            +f"{agent_profile_summary}.\n"
            +f'Current plan of {self.name}: {current_plan_self}.\n'
            +f'Current plan of {agent.person.name}: {current_plan_agent}.\n'
            +f'Relations of {self.name} With {agent.person.name}: {self_relations[agent.person.name]}.\n\n'
            +f"Use the following format:\n"
            +"Question: the input question you must answer"
            +f"Thought: you should always think about what to do\n"
            +"Action: the action to take, should be one of [{tool_names}]\n"
            +"Action Input: the input to the action\n"
            +"Observation: the result of the action\n"
            +"\n\nBegin!\n"
            +f"Question: {previous_response}\n"
            +f"Thought: {previous_dialogue_response_reaction}\n"
            +f"Reply Count: {counter}"
            +"{agent_scratchpad}"
        )

        tool_used, full_result, consumed_tokens = self._generate_reaction(self_type, previous_dialogue_response_reaction, call_to_action_template, current_time, tools_to_use, now=now)
        
        file = open(self.file_path, 'a')
        file.write(f"{self.name} heard {previous_response} from {agent.person.name} and said {full_result}")

        self.memory.save_context(
            {},
            {
                self.memory.add_memory_key: f"{self.name} heard "
                f"{previous_response} from {agent.person.name} and said {full_result}",
                self.memory.now_key: now,
            },
        )

        if((tool_used == "Townfolk Continue Dialogue Tool") or (tool_used == "Werewolf Continue Dialogue Tool")):
          return True, full_result, consumed_tokens
        elif((tool_used == "Townfolk End Dialogue Tool") or (tool_used == "Werewolf End Dialogue Tool")):
          return False, full_result, consumed_tokens


        ## end
        # have to add dialogue complete extraction way
        # result = full_result.strip().split("\n")[0]
        # if "GOODBYE:" in result:
        #     farewell = self._clean_response(result.split("GOODBYE:")[-1])
        #     self.memory.save_context(
        #         {},
        #         {
        #             self.memory.add_memory_key: f"{self.name} observed "
        #             f"{observation} and said {farewell}",
        #             self.memory.now_key: now,
        #         },
        #     )
        #     return False, f"{self.name} said {farewell}", consumed_tokens
        # if "SAY:" in result:
        #     response_text = self._clean_response(result.split("SAY:")[-1])
        #     self.memory.save_context(
        #         {},
        #         {
        #             self.memory.add_memory_key: f"{self.name} observed "
        #             f"{observation} and said {response_text}",
        #             self.memory.now_key: now,
        #         },
        #     )
        #     return True, f"{self.name} said {response_text}", consumed_tokens
        # else:
        #     return True, result, consumed_tokens

    ######################################################
    # Agent stateful' summary methods.                   #
    # Each dialog or response prompt includes a header   #
    # summarizing the agent's self-description. This is  #
    # updated periodically through probing its memories  #
    ######################################################
    def _compute_agent_summary(self) -> str:
        """"""
        prompt = PromptTemplate.from_template(
            "How would you summarize {name}'s core characteristics given the"
            + " following statements:\n"
            + "{relevant_memories}"
            + "Do not embellish."
            + "\n\nSummary: "
        )
        # The agent seeks to think about their core characteristics.
        return (
            self.chain(prompt)
            .run(name=self.name, queries=[f"{self.name}'s core characteristics"])
            .strip()
        )

    def get_summary(
        self, force_refresh: bool = False, now: Optional[datetime] = None
    ) -> str:
        """Return a descriptive summary of the agent."""
        current_time = datetime.now() if now is None else now
        since_refresh = (current_time - self.last_refreshed).seconds
        if (
            not self.summary
            or since_refresh >= self.summary_refresh_seconds
            or force_refresh
        ):
            self.summary = self._compute_agent_summary()
            self.last_refreshed = current_time
        age = self.age if self.age is not None else "N/A"
        return (
            f"Name: {self.name} (age: {age})"
            + f"\nInnate traits: {self.traits}"
            + f"\n{self.summary}"
        )

    def get_full_header(
        self, force_refresh: bool = False, now: Optional[datetime] = None
    ) -> str:
        """Return a full header of the agent's status, summary, and current time."""
        now = datetime.now() if now is None else now
        summary = self.get_summary(force_refresh=force_refresh, now=now)
        current_time_str = now.strftime("%B %d, %Y, %I:%M %p")
        return (
            f"{summary}\nIt is {current_time_str}.\n{self.name}'s status: {self.status}"
        )
