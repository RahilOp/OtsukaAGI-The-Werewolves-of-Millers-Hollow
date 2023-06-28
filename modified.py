from langchain.base_language import BaseLanguageModel
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.load.serializable import Serializable
from customtemplate import CustomOutputParser,CustomPromptTemplate

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field

from langchain import LLMChain
from langchain.base_language import BaseLanguageModel
from langchain.experimental.generative_agents.memory import GenerativeAgentMemory
from langchain.prompts import PromptTemplate

from utils import generate_response


class GenerativeAgent1(BaseModel):
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
    verbose: bool = False
    summary: str = ""  #: :meta private:
    """Stateful self-summary generated via reflection on the character's memory."""

    summary_refresh_seconds: int = 3600  #: :meta private:
    """How frequently to re-generate the summary."""

    last_refreshed: datetime = Field(default_factory=datetime.now)  # : :meta private:
    """The last time the character's summary was regenerated."""

    daily_summaries: List[str] = Field(default_factory=list)  # : :meta private:
    """Summary of the events in the plan that the agent took."""


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

    def _generate_reaction(
        self, observation: str, suffix: str, now: Optional[datetime] = None
    ) -> str:
        """React to a given observation or dialogue act."""
        # prompt = PromptTemplate.from_template(
        #     "{agent_summary_description}"
        #     + "\nIt is {current_time}."
        #     + "\n{agent_name}'s status: {agent_status}"
        #     + "\nSummary of relevant context from {agent_name}'s memory:"
        #     + "\n{relevant_memories}"
        #     + "\nMost recent observations: {most_recent_memories}"
        #     + "\nObservation: {observation}"
        #     + "\n\n"
        #     + suffix
        # )

        # customizing the _generate_reaction  according to werewolf
        # Define which tools the agent can use to answer user queries
        agent_summary_description = self.get_summary(now=now)
        relevant_memories_str = self.summarize_related_memories(observation)
        current_time_str = (
            datetime.now().strftime("%B %d, %Y, %I:%M %p")
            if now is None
            else now.strftime("%B %d, %Y, %I:%M %p")
        )

        most_recent_memories_list = []
        l = len(self.person.memory.memory_retriever.memory_stream)
        for i in range(l-1, 0, -1):
          most_recent_memories_list.append(self.person.memory.memory_retriever.memory_stream[i].page_content)

        most_recent_memories = "\n".join(most_recent_memories_list)

        tools = [
            Tool(
                name = "Dialogue",
                func=generate_response,
                description = "useful when you want to give answer based on your memory and understanding."
            ),
            Tool(
                name = "Bluff",
                func=generate_response,
                description = "useful when you want to give a answer which deceives or mislead someone into believing something that is not true"
            ),
            Tool(
                name = "Argument",
                func=generate_response,
                description = "useful when you want to give answer which presents logical reasoning and evidence to support your position or persuade others to adopt your viewpoint"
            ),
            Tool(
                name = "Investigate",
                func = generate_response,
                description = "useful when one wants to ask question and gather more insights and information regarding the intentions and motives of the other person"
                # description = "useful for gathering information and examining details to uncover insights, facts, or evidence. This tool is commonly used to find intention of the opponent in negotiations, \
                #                 or any situation requiring in-depth exploration and analysis."
            )
        ]
        # Set up the base template
        template = f"""
        Complete the objective as best you can. You have access to the following tools:

        {{tool_names}}

        {agent_summary_description}
        It is 10:00 AM.
        {self.name}'s status: {self.status}
        Summary of relevant context from {self.name}'s memory:
        {relevant_memories_str}
        Most recent observations: {most_recent_memories}
        Observation: {observation}
       """

        string2 = """
        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation should only be done once)
        Final Answer: the final answer to the original input question

        These were previous tasks you completed:



        Begin!

        Question: {input}
        {agent_scratchpad}
        """

        template = template + suffix + string2

        # print(template)
        prompt = CustomPromptTemplate(
            template=template,
            tools=tools,
            # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
            # This includes the `intermediate_steps` variable because that is needed
            input_variables=["input", "intermediate_steps"]
        )

        output_parser = CustomOutputParser()
        print(prompt)

        # define tool usage logic based on Interaction Tree
        tool_names = [tool.name for tool in tools]
        agent = LLMSingleActionAgent(
            llm_chain = self.chain(prompt = prompt),
            output_parser=output_parser,
            stop=["\nObservation:"],
            allowed_tools=tool_names
        )

        agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

        # return self.chain(prompt=prompt, ).run(**kwargs).strip()
        # print(observation)
        kwargs: Dict[str, Any] = dict(
            observation=observation,
            input = "",
            tool_names = tool_names,
        )
        # consumed_tokens = self.llm.get_num_tokens(
        #     prompt.format(**kwargs)
        # )
        # print("Tokens Consumed here:", consumed_tokens)
        # kwargs[self.memory.most_recent_memories_token_key] = consumed_tokens
        return_res = agent_executor.run(**kwargs).strip()
        consumed_tokens = agent_executor.agent.llm_chain.llm.get_num_tokens(prompt.format(**kwargs))
        return return_res, consumed_tokens

    def _clean_response(self, text: str) -> str:
        return re.sub(f"^{self.name} ", "", text.strip()).strip()

    def generate_reaction(
        self, observation: str, now: Optional[datetime] = None
    ) -> Tuple[bool, str]:
        """React to a given observation."""
        call_to_action_template = (
            f"Should {self.name} react to the observation, and if so,"
            + f" what would be an appropriate reaction? Respond in one line."
            + f' If the action is to engage in dialogue, write:\nSAY: "what to say"'
            + f"\notherwise, write:\nREACT: {self.name}'s reaction (if anything)."
            + f"\nEither do nothing, react, or say something but not both.\n\n"
        )

        full_result, consumed_tokens = self._generate_reaction(
            observation, call_to_action_template, now=now
        )
        result = full_result.strip().split("\n")[0]
        # AAA
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
            return False, f"{self.name} {reaction}", consumed_tokens
        if "SAY:" in result:
            said_value = self._clean_response(result.split("SAY:")[-1])
            return True, f"{self.name} said {said_value}", consumed_tokens
        else:
            return False, result, consumed_tokens

    def generate_dialogue_response(
        self, agent2, observation: str, now: Optional[datetime] = None
    ) -> Tuple[bool, str]:
        """React to a given observation."""
        call_to_action_template = (
            f"{self.name} is in conversation with {agent2.person.name}"
            +f"What would {self.name} say? To end the conversation, write:"
            +' GOODBYE: "what to say". Otherwise to continue the conversation,'
            +' write: SAY: "what to say next"\n\n'
        )
        full_result, consumed_tokens = self._generate_reaction(
            observation, call_to_action_template, now=now
        )
        result = full_result.strip().split("\n")[0]
        if "GOODBYE:" in result:
            farewell = self._clean_response(result.split("GOODBYE:")[-1])
            self.memory.save_context(
                {},
                {
                    self.memory.add_memory_key: f"{self.name} observed "
                    f"{observation} and said {farewell}",
                    self.memory.now_key: now,
                },
            )
            return False, f"{self.name} said {farewell}", consumed_tokens
        if "SAY:" in result:
            response_text = self._clean_response(result.split("SAY:")[-1])
            self.memory.save_context(
                {},
                {
                    self.memory.add_memory_key: f"{self.name} observed "
                    f"{observation} and said {response_text}",
                    self.memory.now_key: now,
                },
            )
            return True, f"{self.name} said {response_text}", consumed_tokens
        else:
            return False, result, consumed_tokens

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
