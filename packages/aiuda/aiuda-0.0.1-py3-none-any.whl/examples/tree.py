import utils
from langchain import hub

from aiuda import aiuda


if __name__ == "__main__":
    prompt = hub.pull("hwchase17/react")
    utils.print_header("Original Object")
    print(prompt + '\n')

    utils.print_header("aiuda.tree(obj)")
    aiuda.tree(prompt)
