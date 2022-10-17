"""Define functions"""


def chunks(arr: list, size: int) -> list[list]:
    """Splits a list into the specified number of chunks."""
    return [arr[i: i + size] for i in range(0, len(arr), size)]


def ltr_to_num(ltr: str) -> int:
    """Convert a lowercase letter to its position in the alphabet (1 indexed)."""
    return ord(ltr) - 96  # a's ascii code is 97
