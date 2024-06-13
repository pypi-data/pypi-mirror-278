import os
from io import StringIO
from pathlib import Path
from re import sub


def to_snake_case(string: str) -> str:
    """Util function to convert string to snake case.

    Args:
        string (str): String to convert.

    Returns:
        str: Snakecased string.
    """
    string = (
        sub(
            r"(?<=[a-z])(?=[A-Z])|[^a-zA-Z]",
            " ",
            string,
        )
        .strip()
        .replace(" ", "_")
    )
    return "".join(string.lower())


def get_project_root() -> Path:
    """Returns path to project root.

    Returns:
        Path: Path agnostic to OS.
    """
    return Path(os.getcwd())


def to_camel_case(string: str) -> str:
    """Util function to convert string to camel case.

    Args:
        string (str): String to convert.

    Returns:
        str: Camelcased string.
    """
    return sub(r"(_|-)+", " ", string).title().replace(" ", "")


def append_stringio(target: StringIO, to_append: StringIO) -> StringIO:
    """Append content of to_append StringIO to another.

    Args:
        target (StringIO): Main StringIO
        to_append (StringIO): StringIO object to append.

    Returns:
        StringIO: Resulting StringIO
    """
    result = StringIO()
    source_position = to_append.tell()
    to_append.seek(0)
    contents = to_append.read()
    to_append.seek(source_position)
    target.write(contents)
    target.seek(0)
    result.write(target.read())
    return result
