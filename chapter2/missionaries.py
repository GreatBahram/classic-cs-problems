from __future__ import annotations

from typing import List, Optional

from generic_search import Node, bfs, node_to_path

MAX_NUM: int = 3


class MCState:
    def __init__(self, missionaries: int, cannibals: int, boat: bool) -> None:
        self.wm: int = missionaries  # west bank missionaries
        self.wc: int = cannibals  # west bank cannibals
        self.em: int = MAX_NUM - self.wm  # east bank missionaries
        self.ec: int = MAX_NUM - self.wc  # east bank cannibals
        self.boat: bool = boat

    def __str__(self) -> str:
        text: str = (
            "There are {} 👼 and {} 😈 on the west bank.\n"
            "There are {} 👼 and {} 😈 on the east bank.\n"
            "The boat is on the {} bank."
        )
        return text.format(
            self.wm, self.wc, self.em, self.ec, "west" if self.boat else "east"
        )

    def goal_test(self) -> bool:
        return self.is_legal and self.em == MAX_NUM and self.ec == MAX_NUM

    @property
    def is_legal(self) -> bool:
        if self.wm < self.wc and self.wm > 0:
            return False
        if self.em < self.ec and self.em > 0:
            return False
        return True

    def goal_test(self) -> bool:
        if self.is_legal and self.em == MAX_NUM and self.ec == MAX_NUM:
            return True
        return False

    def successors(self) -> List[MCState]:
        sucs: List[MCState] = []
        if self.boat:  # boat on west bank
            if self.wm > 1:
                sucs.append(MCState(self.wm - 2, self.wc, not self.boat))
            if self.wm > 0:
                sucs.append(MCState(self.wm - 1, self.wc, not self.boat))
            if self.wc > 1:
                sucs.append(MCState(self.wm, self.wc - 2, not self.boat))
            if self.wc > 0:
                sucs.append(MCState(self.wm, self.wc - 1, not self.boat))
            if (self.wm > 0) and (self.wc > 0):
                sucs.append(MCState(self.wm - 1, self.wc - 1, not self.boat))
        else:  # boat on east bank
            if self.em > 1:
                sucs.append(MCState(self.wm + 2, self.wc, not self.boat))
            if self.em > 0:
                sucs.append(MCState(self.wm + 1, self.wc, not self.boat))
            if self.ec > 1:
                sucs.append(MCState(self.wm, self.wc + 2, not self.boat))
            if self.ec > 0:
                sucs.append(MCState(self.wm, self.wc + 1, not self.boat))
            if (self.em > 0) and (self.ec > 0):
                sucs.append(MCState(self.wm + 1, self.wc + 1, not self.boat))
        return (s for s in sucs if s.is_legal)


def display_solution(path):
    if len(path) == 0:
        return None
    old_state = path[0]
    print(old_state)
    for state in path[1:]:
        if state.boat:  # boat on the west bank
            print(
                "{} 👼 and {} 😈 moved from east to west bank.\n".format(
                    old_state.em - state.em, old_state.ec - state.ec
                )
            )
        else:  # boat on the east bank
            print(
                "{} 👼 and {} 😈 moved from west to east bank.\n".format(
                    old_state.wm - state.wm, old_state.wc - state.wc
                )
            )
        print(state)
        old_state = state


if __name__ == "__main__":
    start = MCState(missionaries=3, cannibals=3, boat=True)
    solution = bfs(start, MCState.goal_test, MCState.successors)
    if not solution:
        print("No solution found!")
        exit(1)
    else:
        path = node_to_path(solution)
