"""Defines ``Answer`` class"""
from typing import Iterable

from type_aliases import Coord


class Answer(Iterable):
    """
    Defines an slant answer and methods to interact with it.

    ...

    Attributes
    ----------
    answer : list[list[str]]
        a 2D list of cells
    VALID_SLANTS : tuple[str, str]
        valid slants are 'b' or 'f'
    SLASH_MAP : dict[str, str]
        used for converting a slant to a visual representation
    """

    VALID_SLANTS: tuple[str, str] = ("b", "f")
    SLASH_MAP: dict[str, str] = {"b": "\\", "f": "/", "n": "_"}

    # typehints
    answer: list[list[str]]
    size: int

    def __init__(self, size: int):
        self.size = size
        self.answer = [["n" for _ in range(self.size)]
                       for _ in range(self.size)]

    def __iter__(self) -> Iterable[Coord]:
        for row in range(self.size):
            for col in range(self.size):
                yield (col, row)

    def set_slant(self, cell_coords: Coord, slant: str) -> None:
        """Sets the given cell to the given slant."""
        self.answer[cell_coords[1]][cell_coords[0]] = slant

    def get_slant(self, cell_coords: Coord) -> str:
        """Gets the slant at the given cell."""
        if any(i < 0 for i in cell_coords):
            raise IndexError
        return self.answer[cell_coords[1]][cell_coords[0]]

    def print(self, with_slashes: bool = False) -> None:
        """Prints the answer."""
        print()

        for row in self.answer:
            for slant in row:
                if with_slashes:
                    print(Answer.SLASH_MAP[slant], end=" ")
                else:
                    print(slant, end=" ")
            print()  # new row

        print()

    def __str__(self):
        return "".join(["".join(el) for el in self.answer])
