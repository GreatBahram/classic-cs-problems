#!/usr/bin/env python3
import random
from enum import Enum
from math import sqrt
from typing import Callable, List, NamedTuple, Optional

from generic_search import bfs, dfs, node_to_path


class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"


class MazeLocation(NamedTuple):
    row: int
    column: int


class Maze:
    def __init__(
        self,
        rows: int = 10,
        columns: int = 10,
        sparseness: float = 0.20,
        start: MazeLocation = MazeLocation(0, 0),
        goal: MazeLocation = MazeLocation(9, 9),
    ) -> None:
        self._rows = rows
        self._columns = columns
        self.start = start
        self.goal = goal

        self._fill_the_grid(rows, columns)
        self._randomly_fill(rows, columns, sparseness)

    def _fill_the_grid(self, rows, columns):

        self._grid: List[List[Cell]] = [
            [Cell.EMPTY for c in range(columns)] for r in range(rows)
        ]
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def _randomly_fill(self, rows, columns, sparseness):
        for row in range(rows):
            for col in range(columns):
                if random.uniform(0, 1) < sparseness:
                    self._grid[row][col] = Cell.BLOCKED

    def __repr__(self):
        return f"Maze('Rows:{self._rows}', 'Columns: {self._columns}')"

    def __str__(self):
        output = ""
        for row in self._grid:
            output += "".join(c.value for c in row) + "\n"
        return output

    def goal_test(self, ml):
        return self.goal == ml

    def successors(self, ml: MazeLocation) -> List[MazeLocation]:
        locations: List[MazeLocation] = []
        if (
            ml.row + 1 < self._rows
            and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED
        ):
            locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        if (
            ml.column + 1 < self._columns
            and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED
        ):
            locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))

        return locations

    def mark(self, path: list):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.PATH
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def clear(self, path):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL


def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist = (goal.column - ml.column)
        ydist = (goal.row - ml.row)
        return sqrt((xdist * xdist) + (ydist * ydist))
    return distance


def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation):
        xdist = abs(goal.column - ml.column)
        ydist = abs(goal.row - ml.row)
        return (xdist + ydist)
    return distance


if __name__ == '__main__':
    m = Maze()
    print(m)
    soluton1 = dfs(m.start, m.goal_test, m.successors)
    if soluton1 is None:
        print('No solution found using depth-first search!')
    else:
        path = node_to_path(soluton1)
        m.mark(path)
        print('DFS')
        print('-' * m._rows)
        print(m)
        m.clear(path)
    soluton2 = bfs(m.start, m.goal_test, m.successors)
    if soluton2 is None:
        print('No solution found using breadth-first search!')
    else:
        path = node_to_path(soluton2)
        m.mark(path)
        print('BFS')
        print('-' * m._rows)
        print(m)
        m.clear(path)
