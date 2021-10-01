from contextlib import suppress
from typing import Optional

from csp import CSP, Constraint

try:
    from click import style
except ModuleNotFoundError:

    def style(text, fg):
        return text


QUEEN_SYMB: str = "@"


class QueensConstraint(Constraint[int, int]):
    def __init__(self, columns: list[int]) -> None:
        self.columns: list[int] = columns
        super().__init__(columns)

    def satisfied(self, assignment: dict[int, int]) -> bool:
        for q1c, q1r in assignment.items():
            for q2c in range(q1c + 1, len(self.columns) + 1):
                with suppress(KeyError):
                    q2r: int = assignment[q2c]
                    if q1r == q2r:  # same row
                        return False
                    if abs(q1r - q2r) == abs(q1c - q2c):  # diagonal
                        return False
        return True


def display_chess(result: dict[int, int]) -> None:
    grid: list[str] = [[" " for _ in range(len(result))] for _ in range(len(result))]
    for col_idx, row_idx in result.items():
        grid[row_idx - 1][col_idx - 1] = style(QUEEN_SYMB, fg="bright_yellow")

    print("|" + "|".join(map(str, range(1, len(result) + 1))), end="|\n")

    for row in grid:
        print("|" + "|".join(row), end="|\n")


if __name__ == "__main__":
    columns: list[int] = [1, 2, 3, 4, 5, 6, 7, 8]
    rows: dict[int, list[int]] = {col: [1, 2, 3, 4, 5, 6, 7, 8] for col in columns}
    csp: CSP[int, int] = CSP(columns, rows)
    csp.add_constraint(QueensConstraint(columns))
    result: Optional[dict[int, int]] = csp.backtracking()
    if result is None:
        print("No solution found")
    else:
        display_chess(result)
