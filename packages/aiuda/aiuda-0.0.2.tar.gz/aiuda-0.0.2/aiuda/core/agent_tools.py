import traceback

from langchain.tools import StructuredTool
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.pydantic_v1 import Field

from aiuda.core.globals import Globals
from aiuda.core.parsers import extract_keyword_from_function


class ImportInputs(BaseModel):
    """Inputs for using import tool."""

    path: str = Field(
        description=(
            "The library/class to be imported. Cannot use relative paths."
            " Example: mylib.class"
        ),
    )


class SpaiderInputs(BaseModel):
    """Inputs for using spaider tool."""

    object_name: str = Field(
        description="The object/class to analyze in python. Must match the exact "
        "name/class of the variable. This will be evaluated with eval()"
    )


def import_function(path: str) -> str:
    glob = Globals.globals
    try:

        if parsed_path := extract_keyword_from_function(path):
            exec(f"import {parsed_path}", glob)
            exec(f"from {parsed_path} import *", glob)

        elif path.startswith("import"):
            exec(path, glob)

        else:
            exec(f"import {path}", glob)
            exec(f"from {path} import *", glob)

        return f"Module {path} successfully imported"
    except Exception:
        return f"tool failed, cannot import module {path}. Exception: {traceback.format_exc()}"


def spaider_function(object_name: str) -> str:

    globals = Globals.globals
    assert globals is not None, (
        "Globals must be defined before using spider, "
        "please import Globals from aiuda.core.globals and define its property to globals():"
        "\n Globals.globals = globals() or"
        "ensure aiuda.spaider(obj, globals=globals()) in the aiuda call"

    )

    # We use this for if the LLM pass the object as "function(object_name)"
    if parsed_obj := extract_keyword_from_function(object_name):
        object_name = parsed_obj

    try:
        obj = eval(object_name, globals)
        cls = obj.__class__
        try:
            annotations = str(cls.__annotations__)
        except Exception:
            annotations = ""
        doc = obj.__doc__

        result = {
            "object": object_name,
            "class": cls.__name__,
            "annotations": annotations,
            "dir": dir(obj),
            "doc": doc,
        }
        return str(result)

    except Exception:
        return f"spaider cannot extract information from {object_name}. Exception: {traceback.format_exc()}"


spaider_tool = StructuredTool.from_function(
    func=spaider_function,
    name="spaider",
    description="Obtain information about one object, such as its class, some annotations and docs. "
    "You must pass an exact name of the variable or class and ensure it is an object.",
)


import_tool = StructuredTool.from_function(
    func=import_function,
    name="import",
    description="Imports a python library. Only need to pass the path for working. "
    "Example: mylib.example. Invalid and Error Example: import(mylib)",
)
