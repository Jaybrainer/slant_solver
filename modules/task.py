"""Defines ``Task`` class"""
import math
from typing import Iterable

from functions import chunks, ltr_to_num
from type_aliases import Coord


class Task(Iterable):
    """
    Defines a slant task and methods to interact with it.

    ...

    Attributes
    ----------
    task : list[list[int]]
        a 2D list of clues
    """

    # typehints
    task: list[list[int]]
    size: int

    def __init__(self, seed: str):
        self.task = Task.__generate_task_list(seed)
        self.size = len(self.task)

    @staticmethod
    def __generate_task_list(seed: str) -> list[list[int]]:
        """Generate a 2D list from a task seed string."""
        # letters correspond to number of non-clues: a -> 1 ... f -> 6
        # non-clues marked by -1
        flat_task_arr: list[int] = []

        for char in seed:
            if char.isdigit():
                flat_task_arr.append(int(char))
            else:
                flat_task_arr += [-1 for _ in range(ltr_to_num(char))]

        chunk_length: int = math.floor(math.sqrt(len(flat_task_arr)))
        task_arr: list[list[int]] = chunks(flat_task_arr, chunk_length)

        return task_arr

    def __iter__(self) -> Iterable[Coord]:
        for row in range(self.size):
            for col in range(self.size):
                yield (col, row)

    def get_clue(self, clue_coords: Coord) -> int:
        """Gets the clue at the given position."""
        if any(i < 0 for i in clue_coords):
            raise IndexError
        return self.task[clue_coords[1]][clue_coords[0]]

    # def del_clue(self, clue_coords: tuple[int, int]) -> None:
    #     """Deletes the clue at the given position."""
    #     self.task[clue_coords[1]][clue_coords[0]] = -1

    def print(self) -> None:
        """Prints the task."""
        print()

        for row in self.task:
            for col in row:
                if col == -1:
                    print("_", end=" ")
                else:
                    print(col, end=" ")
            print()  # new row

        print()
