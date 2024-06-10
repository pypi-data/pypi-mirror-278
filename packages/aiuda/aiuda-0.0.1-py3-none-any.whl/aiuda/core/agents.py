import os

from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI


class MinimalLangChainAgent:

    def __init__(self) -> None:

        assert (
            os.environ["OPENAI_API_KEY"] != ""
        ), "Please ensure to settle the 'OPENAI_API_KEY' in your enviroment before useing aiuda"

        self.agent = ChatOpenAI(temperature=0)

    def invoke(self, prompt: str, input) -> BaseMessage:
        template = ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                ("user", "{input}"),
            ]
        )
        chain = template | self.agent
        return chain.invoke({"input": input})
