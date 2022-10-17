"""Defines ``Solver`` class"""
# import os

from answer import Answer
from task import Task
from type_aliases import Coord


class Solver:
    """
    Methods for solving a slant puzzle

    ...

    Attributes
    ----------
    task : list[list[int]]
        a 2D list of clues
    answer : list[list[str]]
        a 2D list of cells
    REL_COORDS : tuple[Coord, ...]
        cells around a clue
    CONNECT_PATTERN : list[str]
        slants in an X pattern around a clue
    DISCONNECT_PATTERN : list[str]
        slants in a <> pattern around a clue
    """

    REL_COORDS: tuple[Coord, ...] = \
        ((-1, -1), (0, -1),
         (-1,  0), (0,  0))
    CONNECT_PATTERN: list[str] = \
        ["b", "f",
         "f", "b"]
    DISCONNECT_PATTERN: list[str] = \
        ["f", "b",
         "b", "f"]

    # typehints
    task: Task
    answer: Answer
    clues: set[Coord]

    def __init__(self, task: Task, answer: Answer):
        self.task = task
        self.answer = answer

        self.clues = set()
        self.populate_clues()
        print(self.clues)

    def populate_clues(self) -> None:
        """Populate clues list with coordinates of clues"""
        for clue_coords in self.task:  # type: ignore
            if self.task.get_clue(clue_coords) != -1:
                self.clues.add(clue_coords)

    def get_neighbour_coords(self, clue_coords: Coord) -> list[Coord]:
        """returns absolute coords of neighbouring cells"""
        coords: list[Coord] = []

        for d_x, d_y in Solver.REL_COORDS:
            coords.append((clue_coords[0] + d_x, clue_coords[1] + d_y))

        return coords

    def get_connected_slant_count(self, cell_coords: Coord) -> int:
        """counts how many cells are in an X pattern around a clue"""
        count: int = 0
        neighbours: list[Coord] = \
            self.get_neighbour_coords(cell_coords)
        for i, n_coords in enumerate(neighbours):
            try:
                if self.answer.get_slant(n_coords) == Solver.CONNECT_PATTERN[i]:
                    count += 1
            except IndexError:
                pass

        return count

    def get_disconnected_slant_count(self, cell_coords: Coord) -> int:
        """counts how many cells are in an <> pattern around a clue"""
        count: int = 0
        neighbours: list[Coord] = self.get_neighbour_coords(cell_coords)
        for i, n_coords in enumerate(neighbours):
            try:
                if self.answer.get_slant(n_coords) == Solver.DISCONNECT_PATTERN[i]:
                    count += 1
            except IndexError:
                count += 1
        return count

    def check_completed(self, cell_coords: Coord) -> bool:
        """checks if the current clue has enough <> or X cells surrounding to complete the clue"""
        connect_count: int = self.get_connected_slant_count(cell_coords)
        clue_val: int = self.task.get_clue(cell_coords)

        return connect_count == clue_val

    def check_anti_completed(self, cell_coords: Coord) -> bool:
        """checks if the current clue has enough <> or X cells surrounding to complete the clue"""
        diconnect_count: int = self.get_disconnected_slant_count(
            cell_coords)
        clue_val: int = self.task.get_clue(cell_coords)

        return 4 - diconnect_count == clue_val

    def fill_single_clues(self, clue_coords: Coord):
        """Fills in a clue if enough cells are disconnected/connected."""
        if self.check_completed(clue_coords):
            for i, cell_coords in enumerate(self.get_neighbour_coords(clue_coords)):
                try:
                    if self.answer.get_slant(cell_coords) == 'n':
                        self.answer.set_slant(
                            cell_coords, Solver.DISCONNECT_PATTERN[i])
                except IndexError:
                    pass
        elif self.check_anti_completed(clue_coords):
            for i, cell_coords in enumerate(self.get_neighbour_coords(clue_coords)):
                try:
                    if self.answer.get_slant(cell_coords) == 'n':
                        self.answer.set_slant(
                            cell_coords, Solver.CONNECT_PATTERN[i])
                except IndexError:
                    pass
        else:
            return
        self.clues.remove(clue_coords)

    def solve(self) -> str:
        """Solves the given task."""
        while True:
            temp_clues: set[Coord] = self.clues.copy()

            for clue_coords in temp_clues:
                self.fill_single_clues(clue_coords)

            if len(temp_clues) == len(self.clues):
                break

        # return after done solving
        return str(self.answer)

    def print(self) -> None:
        """Prints the puzzle."""
        # os.system('cls')
        print()

        for y_c in range(self.task.size):
            for x_c in range(self.task.size - 1):
                clue: int = self.task.get_clue((x_c, y_c))
                if clue == -1:
                    print("+---", end="")
                else:
                    print(f'{clue}---', end="")

            clue = self.task.get_clue((self.task.size - 1, y_c))
            if clue == -1:
                print("+")
            else:
                print(clue)

            if y_c < self.answer.size:
                print("|", end="")
                for x_c in range(self.answer.size):
                    print(f' {self.answer.get_slant((x_c, y_c))} |',
                          end="")
            print()
        print()
