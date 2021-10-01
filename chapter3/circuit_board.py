"""In order to see the table pretty printed (colorful), please install click module."""
from enum import Enum
from itertools import product
from random import choice
from typing import NamedTuple, Optional

try:
    from click import style
except ModuleNotFoundError:

    def style(text, fg):
        return text


from csp import CSP, Constraint

all_colors = [
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
    "bright_white",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
]
Grid = list[list[str]]


class Cell(str, Enum):
    EMPTY = " "
    PATH = "*"

    def __str__(self):
        return self.value


class GridLocation(NamedTuple):
    row: int
    column: int


class Rectangle:
    def __init__(self, width: int, length: int):
        self.width: int = width
        self.length: int = length


def generate_grid(rows: int, columns: int) -> Grid:
    return [[Cell.EMPTY for c in range(columns)] for r in range(rows)]


def display_grid(grid: Grid) -> None:
    print("-" * len(grid))
    for row in grid:
        print("".join(row))
    print("-" * len(grid))


def generate_domain(rectangle: Rectangle, grid: Grid) -> list[list[GridLocation]]:
    domain: list[list[GridLocation]] = []
    height: int = len(grid)
    width: int = len(grid[0])

    for row in range(height):
        for col in range(width):
            columns: range = range(col, col + rectangle.length)
            rows: range = range(row, row + rectangle.width)
            if col + rectangle.length <= width and row + rectangle.width <= height:
                domain.append([GridLocation(r, c) for r, c in product(rows, columns)])
    return domain


class CircuitBoardConstraint(Constraint[str, list[GridLocation]]):
    def __init__(self, boards: list[str]) -> None:
        super().__init__(boards)
        self.boards: list[Rectangle] = boards

    def satisfied(self, assignment: dict[Rectangle, list[GridLocation]]) -> bool:
        # if there are duplicates grid locations, then there is an overlap
        all_locations: list[GridLocation] = [
            locs for values in assignment.values() for locs in values
        ]
        return len(set(all_locations)) == len(all_locations)


if __name__ == "__main__":
    import random

    grid: Grid = generate_grid(9, 9)
    boards: list[Rectangle] = [
        Rectangle(9, 1),
        Rectangle(7, 3),
        Rectangle(5, 2),
        Rectangle(2, 1),
        Rectangle(5, 1),
        Rectangle(2, 1),
        Rectangle(3, 2),
        Rectangle(2, 1),
        Rectangle(2, 3),
        Rectangle(2, 2),
        Rectangle(2, 7),
    ]

    random.shuffle(boards)

    locations: dict[Rectangle, list[list[GridLocation]]] = {}
    for b in boards:
        locations[b] = generate_domain(b, grid)

    csp: CSP[Rectangle, list[GridLocation]] = CSP(boards, locations)
    csp.add_constraint(CircuitBoardConstraint(boards))

    result: Optional[dict[Rectangle, list[GridLocation]]] = csp.backtracking()
    if result is None:
        print("No solution found")
    else:
        random.shuffle(all_colors)
        for color, (rec, grid_locations) in zip(all_colors, result.items()):
            for row, col in grid_locations:
                grid[row][col] = style(str(Cell.PATH), fg=color)

        display_grid(grid)
