from typing import Dict, List

from csp import CSP, Constraint


class MapColoringConstraint(Constraint):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.place1 = place1
        self.place2 = place2

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        return assignment[self.place1] != assignment[self.place2]


if __name__ == "__main__":
    colors = ["red", "green", "blue"]
    variables: List[str] = [
        "Western Australia",
        "Northern Territory",
        "South Australia",
        "Queensland",
        "New South Wales",
        "Victoria",
        "Tasmania",
    ]
    domains: Dict[str, List[str]] = {}
    for variable in variables:
        domains[variable] = colors

    csp = CSP(variables, domains)
    csp.add_constraint(MapColoringConstraint("Western Australia", "Northern Territory"))
    csp.add_constraint(MapColoringConstraint("Western Australia", "South Australia"))
    csp.add_constraint(MapColoringConstraint("Queensland", "Northern Territory"))
    csp.add_constraint(MapColoringConstraint("Queensland", "South Australia"))
    csp.add_constraint(MapColoringConstraint("Queensland", "New South Wales"))
    csp.add_constraint(MapColoringConstraint("South Australia", "New South Wales"))
    csp.add_constraint(MapColoringConstraint("South Australia", "Victoria"))
    csp.add_constraint(MapColoringConstraint("Victoria", "New South Wales"))
    csp.add_constraint(MapColoringConstraint("Victoria", "Tasmania"))
    solution = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        print(solution)
