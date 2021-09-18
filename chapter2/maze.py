import math
import random
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Collection, Optional

from generic_search import Node, T, astar, bfs, dfs, node_to_path


class Cell(str, Enum):
    START = "S"
    GOAL = "G"
    BLOCKED = "X"
    PATH = "*"
    EMPTY = " "


@dataclass(frozen=True)
class MazeLocation:
    row: int
    column: int


@dataclass
class Maze:
    rows: int = 10
    columns: int = 10
    start: MazeLocation = MazeLocation(0, 0)
    goal: MazeLocation = MazeLocation(9, 9)
    sparseness: float = 0.2

    def __post_init__(self):
        self._grid = [
            [Cell.EMPTY for c in range(self.columns)] for r in range(self.rows)
        ]
        self._randomly_fill()
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL
        self.count: int = 0

    def _randomly_fill(self) -> None:
        for r in range(self.rows):
            for c in range(self.columns):
                if random.uniform(0.0, 1.0) < self.sparseness:
                    self._grid[r][c] = Cell.BLOCKED

    def __str__(self) -> str:
        border: str = "-" * self.columns + "\n"
        output: str = ""
        for row in self._grid:
            output += "".join(c for c in row) + "\n"
        return border + output + border.strip()

    def goal_test(self, ml: MazeLocation) -> bool:
        self.count += 1
        return ml == self.goal

    def successors(self, ml: MazeLocation) -> list[MazeLocation]:
        locations: list[MazeLocation] = []
        if ml.row + 1 < self.rows and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        if (
            ml.column + 1 < self.columns
            and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED
        ):
            locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))
        return locations

    def mark(self, paths: list[MazeLocation]) -> None:
        for ml in paths:
            self._grid[ml.row][ml.column] = Cell.PATH
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def clear(self, paths: list[MazeLocation]) -> None:
        for ml in paths:
            self._grid[ml.row][ml.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL
        self.count = 0

    @property
    def paths(self) -> int:
        return sum(c == Cell.PATH for row in self._grid for c in row)


def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = ml.column - goal.column
        ydist: int = ml.row - goal.row
        return math.sqrt((xdist ** 2) + (ydist ** 2))

    return distance


def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = abs(ml.column - goal.column)
        ydist: int = abs(ml.row - goal.row)
        return xdist + ydist

    return distance


if __name__ == "__main__":
    m = Maze()
    solution1: Optional[Node[MazeLocation]] = dfs(m.start, m.goal_test, m.successors)
    if solution1 is None:
        print("No solution found using DFS")
    else:
        paths = node_to_path(solution1)
        m.mark(paths)
        print(m)
        print(f"Found solution using {m.count} comparison and {m.paths} hops.")
        m.clear(paths)
    solution2: Optional[Node[MazeLocation]] = bfs(m.start, m.goal_test, m.successors)
    if solution2 is None:
        print("No solution found using BFS")
    else:
        paths = node_to_path(solution2)
        m.mark(paths)
        print(m)
        print(f"Found solution using {m.count} comparison and {m.paths} hops.")
        m.clear(paths)
    distance: Callable[[MazeLocation], float] = manhattan_distance(m.goal)
    solution3: Optional[Node[MazeLocation]] = astar(
        m.start, m.goal_test, m.successors, distance
    )
    if solution3 is None:
        print("No solution found using A*")
    else:
        paths = node_to_path(solution3)
        m.mark(paths)
        print(m)
        print(f"Found solution using {m.count} comparison and {m.paths} hops.")
        m.clear(paths)
