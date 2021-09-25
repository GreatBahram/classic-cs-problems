from __future__ import annotations

from textwrap import dedent
from typing import Final, Optional

from generic_search import Node, bfs, dfs, node_to_path

MAX_NUM: Final[int] = 3

COUNT: int = 0


class MCState:
    def __init__(self, missionaries: int, cannibals: int, boat: bool):
        self.wm: int = missionaries
        self.wc: int = cannibals
        self.em: int = MAX_NUM - self.wm
        self.ec: int = MAX_NUM - self.wc
        self.boat: bool = boat

    def goal_test(self) -> bool:
        global COUNT
        COUNT += 1
        return self.is_legal and self.em == MAX_NUM and self.ec == MAX_NUM

    def successors(self) -> list[MCState]:
        sucs: list[MCState] = []
        if self.boat:  # boat is on the west bank
            if self.wm > 1:
                sucs.append(MCState(self.wm - 2, self.wc, not self.boat))
            if self.wm > 0:
                sucs.append(MCState(self.wm - 1, self.wc, not self.boat))
            if self.wc > 1:
                sucs.append(MCState(self.wm, self.wc - 2, not self.boat))
            if self.wc > 0:
                sucs.append(MCState(self.wm, self.wc - 1, not self.boat))
            if self.wm > 0 and self.wc > 0:
                sucs.append(MCState(self.wm - 1, self.wc - 1, not self.boat))
        else:
            if self.em > 1:
                sucs.append(MCState(self.wm + 2, self.wc, not self.boat))
            if self.em > 0:
                sucs.append(MCState(self.wm + 1, self.wc, not self.boat))
            if self.ec > 1:
                sucs.append(MCState(self.wm, self.wc + 2, not self.boat))
            if self.ec > 0:
                sucs.append(MCState(self.wm, self.wc + 1, not self.boat))
            if self.em > 0 and self.ec > 0:
                sucs.append(MCState(self.wm + 1, self.wc + 1, not self.boat))
        return [s for s in sucs if s.is_legal]

    @property
    def is_legal(self) -> bool:
        if self.wm > 0 and self.wm < self.wc:
            return False
        if self.em > 0 and self.em < self.ec:
            return False
        return True

    def __str__(self) -> str:
        output = dedent(
            """\
            There are {} missionaries and {} cannibals on the west bank.
            There are {} missionaries and {} cannibals on the east bank.
            The boat is on the {} bank."""
        )
        return output.format(
            self.wm, self.wc, self.em, self.ec, "west" if self.boat else "east"
        )

    def __repr__(self) -> str:
        return f"MCState(wm={self.wm}, wc={self.wc}, boat={'west' if self.boat else 'east'})"

    def __eq__(self, other: MCState) -> bool:
        return (self.wm, self.wc, self.boat) == (other.wm, other.wc, other.boat)

    def __hash__(self) -> int:
        return hash((self.wm, self.wc, self.boat))


def display_path(path: list[MCState]) -> None:
    old_state = path[0]
    print(old_state)
    for current_state in path[1:]:
        if current_state.boat:
            print(
                f"{old_state.em - current_state.em} missionaries and {old_state.ec - current_state.ec} cannibals moved from the east to the west bank."
            )
        else:
            print(
                f"{old_state.wm - current_state.wm} missionaries and {old_state.wc - current_state.wc} cannibals moved from the west to the east bank."
            )
        old_state = current_state
        print(current_state)


if __name__ == "__main__":
    start = MCState(MAX_NUM, MAX_NUM, True)
    solution: Optional[Node] = bfs(start, MCState.goal_test, MCState.successors)
    if solution is None:
        print("No solution found using BFS")
    else:
        path: list[MCState] = node_to_path(solution)
        print(len(path))
        display_path(path)
        print(COUNT)
    print("-" * 20)
    COUNT = 0
    solution: Optional[Node] = dfs(start, MCState.goal_test, MCState.successors)
    if solution is None:
        print("No solution found using DFS")
    else:
        path: list[MCState] = node_to_path(solution)
        print(len(path))
        display_path(path)
        print(COUNT)
