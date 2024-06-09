import re, uuid
from typing import Optional


def sanitize_name(name: str, replacement: Optional[str] = "_") -> str:
    """
    Sanitize the name to remove invalid characters.

    Parameters:
        name (str): The original name string.
        replacement (Optional[str]): The string to replace invalid characters with.

    Returns:
        str: The sanitized name.
    """
    # Replace all non-word characters (anything other than a-zA-Z0-9_) with '_'
    sanitized = re.sub(r"[^\w\s]", replacement, name)
    sanitized = re.sub(r"\s+", " ", sanitized).replace(" ", replacement)
    return sanitized.rstrip(replacement)


def abbreviate_name(name: str, max_length: int, delimiter: Optional[str] = "...") -> str:
    """
    Abbreviate a long name to fit within a given maximum length.

    Parameters:
        name (str): The original name string.
        max_length (int): The maximum length for the abbreviated name.
        delimiter (Optional[str]): The string to indicate abbreviation.

    Returns:
        str: The abbreviated name.
    """
    if len(name) <= max_length:
        return name

    delimiter_length = len(delimiter)
    # Ensure that the abbreviated name will not exceed the max_length
    if max_length <= delimiter_length:
        raise ValueError(
            f"max_length must be greater than the length of delimiter ({delimiter_length})."
        )

    # Calculate how many characters to keep from the original name
    keep_length = max_length - delimiter_length

    # Abbreviate the name
    return name[:keep_length] + delimiter


def unique_name(prefix):
    unique_id = uuid.uuid4()
    return f"{prefix}_{unique_id}"


def get_longest_line(s: str) -> str:
    lines = s.split("\n")
    return max(lines, key=len)
