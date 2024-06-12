import re


def extract_keyword_from_function(function_str: str) -> str:
    match = re.search(r"\w+\((.*?)\)", function_str)
    if match:
        return match.group(1)
    return None
