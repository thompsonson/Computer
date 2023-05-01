""" Base controller class for all controllers. """

import logging
import time
from typing import Type

from langchain.agents import initialize_agent

from pprint import pprint


class AgentBase:
    """Base Agent class"""

    def __init__(
        self,
        tools,
        prompt,
        memory,
        llm,
        agent: str = "conversational-react-description",
        verbose: bool = False,
        max_iterations: int = 1,
    ) -> None:
        self._tools = tools
        self._prompt = prompt
        self._memory = memory
        self._llm = llm
        self._agent = agent
        self._verbose = verbose
        self._max_iterations = max_iterations
        self._agentchain = self._initialize_agent()

    def _initialize_agent(self):
        print("Initializing agent...")
        print(self._llm)
        # pprint(vars(self))
        agent_chain = initialize_agent(
            self._tools,
            self._llm,
            agent=self._agent,  # ="zero-shot-react-description",
            memory=self._memory,
            verbose=self._verbose,
            max_iterations=self._max_iterations,
        )
        return agent_chain

    def get_response(self, selected_model, user_input, conversation_history=""):
        # Get raw chat response
        response = self._agent_chain.run(user_input).strip()  # type: ignore
