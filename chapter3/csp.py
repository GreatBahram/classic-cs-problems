from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Generic, Optional, TypeVar

V = TypeVar("V")  # value type
D = TypeVar("D")  # domain type


class Constraint(Generic[V, D], ABC):
    def __init__(self, variables: list[V]) -> None:
        self.variables: list[V] = variables

    @abstractmethod
    def satisfied(self, assignment: dict[V, D]) -> bool:
        raise NotImplementedError("Subclass should implement this")


class CSP(Generic[V, D]):
    def __init__(self, variables: list[V], domains: dict[V, list[D]]):
        self.variables: list[V] = variables
        self.domains: dict[V, list[D]] = domains
        self.constraints: dict[V, list[Constraint[V, D]]] = defaultdict(list)
        for variable in self.variables:
            if variable not in domains:
                raise LookupError("Every variable should have a domain")

    def consitent(self, variable: V, assignment: dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable not constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def backtracking(self, assignment: dict[V, D] = {}) -> Optional[dict[V, D]]:
        if len(assignment) == len(self.variables):
            return assignment

        unassigned: list[V] = [v for v in self.variables if v not in assignment]
        # we pick the first unassigned variables
        first: V = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            if self.consitent(first, local_assignment):
                result: Optional[dict[V, D]] = self.backtracking(local_assignment)
                if result is not None:
                    return result
        return None
