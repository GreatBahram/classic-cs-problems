from typing import Optional
from csp import CSP, Constraint


class SendMoreMoneyConstraint(Constraint[str, int]):
    def __init__(
        self, letters: list[str], first: str, second: str, result: str
    ) -> None:
        super().__init__(letters)
        self.letters: list[str] = letters
        self.first: str = first
        self.second: str = second
        self.result: str = result

    def satisfied(self, assignment: dict[str, int]) -> bool:
        # if there are duplicate values, then that is not a valid solution
        if len(set(assignment.values())) < len(assignment):
            return False

        if len(assignment) == len(self.letters):
            first_sum: int = sum(
                assignment[char] * 10 ** idx for idx, char in enumerate(reversed(first))
            )
            second_sum: int = sum(
                assignment[char] * 10 ** idx
                for idx, char in enumerate(reversed(second))
            )
            result_sum: int = sum(
                assignment[char] * 10 ** idx
                for idx, char in enumerate(reversed(result))
            )
            return first_sum + second_sum == result_sum
        return True


if __name__ == "__main__":
    first: str = "SEND"
    second: str = "MORE"
    result: str = "MONEY"
    letters: list[str] = list(set(first + second + result))
    possible_digits: dict[str, list[int]] = {
        letter: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] for letter in letters
    }
    csp: CSP[str, int] = CSP(letters, possible_digits)
    csp.add_constraint(SendMoreMoneyConstraint(letters, first, second, result))
    solution: Optional[dict[str, int]] = csp.backtracking({result[0]: 1})
    if solution is None:
        print("No solution found")
    else:
        print(solution)
