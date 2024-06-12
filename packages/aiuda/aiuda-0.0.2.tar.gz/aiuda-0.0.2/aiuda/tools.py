from typing import Optional

from colorama import Fore
from colorama import Style

from aiuda.core.agent_tools import import_tool
from aiuda.core.agent_tools import spaider_tool
from aiuda.core.agents import MinimalLangChainAgent
from aiuda.core.globals import Globals
from aiuda.core.types import SupportsStr


class Aiuda:

    def __init__(self) -> None:
        self.agent = MinimalLangChainAgent()

    def _log(keyword: str) -> None:
        print(
            Fore.LIGHTGREEN_EX
            + Style.BRIGHT
            + "[aiuda]"
            + f"[{keyword}]"
            + Style.RESET_ALL
        )

    def tree(self, obj: SupportsStr) -> None:
        Aiuda._log("tree")
        prompt = (
            "\nYou are an AI assistant. Your goal is to return the given object as a tree representation similar "
            "\nto the output of the tree command in bash. Use the symbols ['├', '─', '│', '└'] to draw a clear "
            "\nand structured tree."
            "\nStart the tree with the root node."
            "\nFor each child node:"
            "\n    Use '├─' to connect intermediate nodes."
            "\n    Use '└─' for the last node in a group."
            "\n    Use '│' for vertical connections in sub-levels. (Use multiple if nested)"
            "\nEnsure proper indentation to represent hierarchical relationships."
            "\nIf a node can be accessed with '.' notation, start the name with '.'."
            "\nIf a node can be accesed with '[]' notation, start the name with '[x]' where x is the index of "
            "\nthe value (if known)."
            "\nIf the node is a complex object use '[x](y)' as the notation for the node where x is the name "
            "\nof the class and y "
            "\nthe name of the variable (if known)."
            "\nThe output should be raw avoid using code blocks or similar."
            "\nThe tree should be ordered to enhance the object visualization."
        )
        input = f"Target object: '''{obj}'''"
        result = self.agent.invoke(prompt, input)
        print(Fore.LIGHTBLUE_EX + result.content + Fore.RESET)

    def spaider(
        self,
        obj: SupportsStr,
        max_depth_level: int = 2,
        max_steps: int = 10,
        verbose: bool = True,
        explore_private: bool = False,
        /,
        globals: Optional[dict] = None
    ) -> None:
        Aiuda._log("spider")

        attributes = [
            ("__str__", str),
            ("__repr__", repr),
            ("Class name", lambda o: o.__class__.__name__),
            ("Module name", lambda o: o.__module__),
            ("Base classes", lambda o: o.__class__.__bases__),
            ("Class dictionary", lambda o: o.__class__.__dict__),
            ("Objects dictionary", lambda o: o.__dict__),
        ]

        if globals:
            Globals.globals = globals

        result = ""
        parsed_attributes = dict()

        for name, func in attributes:
            value = "Not available"
            try:
                value = func(obj)
            except AttributeError:
                pass
            parsed_attributes[name] = value

        message = (
            "Describe the best as you can the following object:"
            f"\n__str__: {parsed_attributes['__str__']}"
            f"\n__repr__: {parsed_attributes['__repr__']}"
            f"\nClass name: {parsed_attributes['Class name']}"
            f"\nModule name: {parsed_attributes['Module name']}"
            f"\nBase classes: {parsed_attributes['Base classes']}"
            f"\nClass dictionary: {parsed_attributes['Class dictionary']}"
            f"\nObject's dictionary: {parsed_attributes['Objects dictionary']}"
            "\nTry to search about its properties and understand its main functionalities and behaviors."
            "\nYou can access any property/attribute, but optimize your search to find the core functionalities"
            f" under {max_steps} steps and without searching with a depth higher than {max_depth_level}."
            " The returned output should contain the explanation of all the information found, including:"
            "\n1. Known properties and attributes."
            "\n2. Methods and their functionalities."
            "\n3. Common use cases and examples."
            "\n4. Possible interactions with other objects."
            "\n5. Performance considerations."
            "\n6. Any associated events or triggers."
            "\n7. Error handling and exceptions."
            "\n8. Security implications."
            "\n9. Compatibility with other systems or components."
            "\nProvide detailed descriptions and examples wherever possible to aid in understanding."
            "\nThe final explanation should be clear and thorough, ensuring the programmer deeply understands "
            "the object analyzed."
            "\nExample output:"
            "\nThe requested `Agent` object has the following main functionalities:"
            "\n1. `Agent.db`: Represents an `InMemoryTaskDB` object with methods for creating tasks, steps, "
            "and artifacts."
            "\n2. `Agent.setup_agent()`: Sets the agent's task and step handlers."
            "\n3. `Agent.get_artifact_folder()`: Retrieves the artifact path for a specified task and artifact."
            "\n4. `Agent.start()`: Initiates the agent server."
            "\n5. `Agent.workspace`: A string attribute with various string manipulation methods available."
            "\n..."
        )
        if not explore_private:
            message += "\nAvoid searching inside objects or functions that start with _ or are private"

        result = self.agent.react(
            input=message,
            tools=[spaider_tool, import_tool],
            verbose=verbose,
            max_steps=max_steps,
            handle_parsing_errors=True,
        )
        print(Fore.LIGHTBLUE_EX + result + Fore.RESET)
