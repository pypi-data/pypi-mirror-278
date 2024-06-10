"""This module contains methods relating to strings."""

import time
from enum import StrEnum


class Loglevel(StrEnum):
    """A string enum defining importance levels for usage in the 'log_print' method"""

    INFO = "Information"
    """Used to indicate an informational output."""
    WARNING = "Warning"
    """Used to indicate a warning."""
    ERROR = "ERROR"
    """Used to indicate an error."""


def log_print(s: str, level: Loglevel = Loglevel.INFO, time_format: str = "%Y-%m-%d %H:%M:%S"):
    """Takes a string and outputs it with an additional prefix indicating importance.

    Args:
        s (str): The string which will be output
        level (Loglevel, optional): The prefix indicating importance. Defaults to Loglevel.INFO.
        time_format (str, optional): A (C-time adherent) string to format the time. Defaults to '%Y-%m-%d %H:%M:%S'
    """
    if level not in Loglevel._member_names_:  # pylint: disable=E1101,W0212
        level = Loglevel.INFO

    if time_format is not None and time_format != '':
        time_tuple = time.localtime()
        time_string = time.strftime(time_format, time_tuple)
        print(f"[{time_string}]\t[{level}]\t{s}")
    else:
        print(f"[{level}]\t{s}")


def truncate_string(s: str, length: int, ellipsis: str = "...") -> str:
    """Takes a string, truncates it to the given length, adding a given ellipsis.

    Args:
        s (str): The string which will be shortened.
        length (int): The length of the shortened string including the length of the ellipsis.
        ellipsis (str, optional): An optional ellipsis which will be appended. Defaults to "...".

    Returns:
        str: A truncated version of the string with given length (and ellipsis)
    """
    if len(s) > length:
        # if the shortened string including the ellipsis is too long, don't add an ellipsis
        if len(ellipsis) > length - len(ellipsis):
            ellipsis = ""
        s = f"{s[:length-len(ellipsis)]}{ellipsis}"
    return s


def insert_line_into_string(line: str, s: str, pos: int) -> str:
    """Takes two strings and inserts the first one into the second one as a new line at the given position.

    Args:
        line (str): The line to insert.
        s (str): The (potential multi-line) string in which to insert line.
        pos (int): The line number of the newly inserted line.
            Uses Python's List.insert() position syntax—negative indices, e.g. -1, inserts line *before* the last element.

    Returns:
        str: A new string containing line at the given line number.
    """
    split_string = s.splitlines(keepends=True)
    if "\n" not in line:
        line += "\n"
    if pos >= len(split_string):
        if "\n" not in split_string[-1]:
            line = "\n" + line
            line = line.rstrip("\n")
    split_string.insert(pos, line)
    return "".join(split_string)
