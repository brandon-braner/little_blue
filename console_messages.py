reset = "\u001b[0m"
green = "\u001b[32m"
red = "\u001b[31m"
blue = "\u001b[34m"
white = "\u001b[37m"


def success_message(message: str):
    print(f"{green} {message} {reset}")


def error_message(message: str):
    print(f"{red} {message} {reset}")


def info_message(message: str):
    print(f"{blue} {message} {reset}")


def generic_message(message: str):
    print(f"{white} {message} {reset}")
