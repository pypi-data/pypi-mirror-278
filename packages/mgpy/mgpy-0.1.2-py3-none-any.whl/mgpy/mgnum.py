"""This module contains methods relating to numbers and their represenatation."""

def generate_human_readable_number(number: int, suffixes: list[str] = None, decimal_separator: str = ".") -> str:
    """Takes a number and returns a 'human readable' string. E.g., 1500000 -> 1.5M

    Args:
        number (int): The number to represent.
        suffixes (list[str], optional): A list of ascendingly sorted suffixes for each order of magnitude. Defaults to ["k", "M", "G", "T"].
        decimal_separator (str, optional): The decimal separator. Defaults to ".".

    Returns:
        str: The human readable string.
    """
    human_readable_number = number

    # since Python's default arguments are created, when the function is defined, create the object here instead
    if suffixes is None:
        suffixes = ["k", "M", "G", "T"]

    suffixes.insert(0, "")

    i = 0
    while number > 1000 and i < len(suffixes) - 1:
        number /= 1000.0
        i += 1
    human_readable_number = f"{round(number, 1):g}"
    human_readable_number = human_readable_number.replace(".", decimal_separator) + suffixes[i]

    return human_readable_number
