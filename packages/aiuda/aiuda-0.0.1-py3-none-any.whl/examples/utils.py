from colorama import Fore
from colorama import Style


def print_header(text: str) -> None:
    line = "-" * 10
    print(Fore.CYAN + Style.BRIGHT + line + " " + text + " " + line + Style.RESET_ALL)
