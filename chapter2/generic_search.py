#!/usr/bin/env python3
from typing import List, TypeVar, Generic

T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self):
        self._container: List[T] = []

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    @property
    def empty(self) -> bool:
        return self._container == []

    def __repr__(self):
        return repr(self._container)


class Node:
    def __init__(self, state, parent=None, cost=0.0, heuristic=0.0) -> None:
        self.state = state
        self.parent = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def dfs(initial, goal_test, successorts):
    frontier = Stack()
    frontier.push(Node(initial))

    explored = {initial}

    while not frontier.empty:
        current_node = frontier.pop()
        current_state = current_node.state

        if goal_test(current_state):
            return current_node

        for child in successorts(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, parent=current_node))
    return None


def node_to_path(node):
    path = [node.state]
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    return path[::-1]
