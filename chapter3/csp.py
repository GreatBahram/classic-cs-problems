from abc import ABC, abstractmethod
from typing import Dict, List, TypeVar

V = TypeVar("V")  # variable type
D = TypeVar("D")  # domain type


class Constraint(ABC):
    def __init__(self, variables):
        self.variables = variables

    # each assignment consists of values with selective domains
    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        pass


class CSP:
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]):
        self.variables = variables
        self.domains = domains
        self.constraints: Dict[V, List[Constraint]] = {}
        for variable in variables:
            if variable not in domains:
                raise LookupError("")
            self.constraints[variable] = []

    def add_constraint(self, constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("")
            self.constraints[variable].append(constraint)

    def consistent(self, variable, assignment: Dict[V, D]):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment: Dict[V, D] = {}):
        # base case
        if len(assignment) == len(self.variables):
            return assignment
        unassigned = [v for v in self.variables if v not in assignment]

        first = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()  # deep copy
            local_assignment[first] = value
            if self.consistent(first, local_assignment):
                result = self.backtracking_search(local_assignment)
                if result is not None:
                    return result
        return None
