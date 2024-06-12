import os
from typing import Any
from typing import Sequence

from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents import create_react_agent
from langchain.prompts import ChatPromptTemplate
from langchain.tools import Tool
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI


class MinimalLangChainAgent:

    def __init__(self) -> None:

        assert (
            os.environ["OPENAI_API_KEY"] != ""
        ), "Please ensure to settle the 'OPENAI_API_KEY' in your enviroment before useing aiuda"

        self.agent = ChatOpenAI(temperature=0)
        self.prompt_db: dict[str, Any] = dict()

    def set_model(self, model: str) -> None:
        if model == "default":
            self.agent = ChatOpenAI(temperature=0)
            return

        self.agent = ChatOpenAI(temperature=0, model=model)

    def invoke(self, prompt: str, input) -> BaseMessage:
        template = ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                ("user", "{input}"),
            ]
        )
        chain = template | self.agent
        return chain.invoke({"input": input})

    def react(
        self,
        input: str,
        tools: Sequence[Tool],
        verbose: bool = False,
        max_steps: int = 10,
        handle_parsing_errors: bool = True,
    ) -> str:
        if "react" not in self.prompt_db:
            self.prompt_db["react"] = hub.pull("hwchase17/react")

        react_agent = create_react_agent(self.agent, tools, self.prompt_db["react"])
        agent_executor = AgentExecutor(
            agent=react_agent,
            tools=tools,
            verbose=verbose,
            handle_parsing_errors=handle_parsing_errors,
            max_iterations=max_steps
        )
        return agent_executor.invoke({"input": input})["output"]
