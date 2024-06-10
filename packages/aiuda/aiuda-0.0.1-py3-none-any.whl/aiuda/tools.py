from colorama import Fore
from colorama import Style

from aiuda.core.agents import MinimalLangChainAgent
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
