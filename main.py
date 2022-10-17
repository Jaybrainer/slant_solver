"""Bot for solving slant puzzles."""
from modules.answer import Answer
from modules.solver import Solver
from modules.task import Task

# FIXME: place in main(), and get task from HTTP
task_seed: str = "1a10d223b2d03a21c2a20a01c"  # "b0a2a0c11b2c03a1a1b2222f"


def main() -> None:
    """Slant Bot main code"""
    # create task and answer
    task: Task = Task(seed=task_seed)
    answer: Answer = Answer(size=task.size - 1)

    # create solver
    solver: Solver = Solver(task, answer)

    # TODO: remove tests
    solution = solver.solve()
    if 'n' not in solution:
        print("Success!")
    else:
        print("Solve process failed")

    solver.print()


if __name__ == "__main__":
    main()
