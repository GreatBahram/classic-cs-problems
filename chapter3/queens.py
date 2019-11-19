from typing import Dict, List

from csp import CSP, Constraint


class QueenConstraint(Constraint):
    def __init__(self, columns: List[int]):
        super().__init__(columns)
        self.columns = columns

    def satisfied(self, assignment: Dict[int, int]) -> bool:
        # q1c = queen 1 column, q1r = queen 1 row
        for q1c, q1r in assignment.items():
            for q2c in range(q1c + 1, len(self.columns) + 1):
                if q2c in assignment:
                    q2r = assignment[q2c]
                    if q1r == q2r:
                        return False
                    same_diagonal = abs(q1c - q2c) == abs(q1r - q2r)
                    if same_diagonal:
                        return False
        return True  # no conflict


if __name__ == "__main__":
    columns: List[int] = [1, 2, 3, 4, 5, 6, 7, 8]
    rows: Dict[int, List[int]] = {}

    for column in columns:
        rows[column] = [1, 2, 3, 4, 5, 6, 7, 8]

    csp = CSP(columns, rows)
    csp.add_constraint(QueenConstraint(columns))
    solution = csp.backtracking_search()
    if solution is None:
        print('No solution found!')
    else:
        print(solution)
