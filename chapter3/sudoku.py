from itertools import chain
from typing import NamedTuple, Optional

from csp import CSP, Constraint

Grid = list[list[int]]


class GridLocation(NamedTuple):
    row: int
    column: int


def generate_sudoku() -> Grid:
    """magnitude should be a multiple of 3"""
    return [[0 for _ in range(9)] for _ in range(9)]


def display_grid(grid: Grid) -> None:
    print("-" * 19)
    for row in grid:
        print("|" + "|".join(map(str, row)), end="|\n")
    print("-" * 19)


class SudokuConstraint(Constraint):
    def __init__(self, variables: list[GridLocation], grid) -> None:
        super().__init__(variables)
        self.grid: Grid = grid

    def satisfied(self, assignment: dict[GridLocation, int]) -> bool:
        for gl, number in assignment.items():
            if (
                self.used_in_row(gl, number, assignment)
                or self.used_in_column(gl, number, assignment)
                or self.used_in_subgrid(gl, number, assignment)
            ):
                return False
        return True

    def used_in_row(
        self, gl: GridLocation, number: int, assignment: dict[GridLocation, int]
    ) -> bool:
        # all columns except a given grid location's column
        columns = chain(range(gl.column), range(gl.column + 1, len(self.grid)))
        return any(
            assignment.get(GridLocation(gl.row, col)) == number for col in columns
        )

    def used_in_column(
        self, gl: GridLocation, number: int, assignment: dict[GridLocation, int]
    ) -> bool:
        # all rows except a given grid location's row
        rows = chain(range(gl.row), range(gl.row + 1, len(self.grid)))
        return any(assignment.get(GridLocation(r, gl.column)) == number for r in rows)

    def used_in_subgrid(
        self, gl: GridLocation, number: int, assignment: dict[GridLocation, int]
    ) -> bool:
        start_loc: GridLocation = GridLocation(
            gl.row - gl.row % 3, gl.column - gl.column % 3
        )
        for r in range(3):
            for c in range(3):
                candidate_gl: GridLocation = GridLocation(
                    start_loc.row + r, start_loc.column + c
                )
                if assignment.get(candidate_gl) == number and candidate_gl != gl:
                    return True
        return False


if __name__ == "__main__":
    grid: Grid = generate_sudoku()
    variables: list[GridLocation] = [
        GridLocation(row, col) for row in range(len(grid)) for col in range(len(grid))
    ]
    domains: dict[GridLocation, list[int]] = {
        gl: [1, 2, 3, 4, 5, 6, 7, 8, 9] for gl in variables
    }
    csp: CSP[str, list[GridLocation]] = CSP(variables, domains)
    csp.add_constraint(SudokuConstraint(variables, grid))

    # NOTE: if you want to preassign some cells, do it using backtracking method
    # backtracking({GridLocation(0, 0): 8})
    result: Optional[dict[str, list[GridLocation]]] = csp.backtracking()
    if result is None:
        print("No solution found")
    else:
        for gl, number in result.items():
            grid[gl.row][gl.column] = number
        display_grid(grid)
