import random
from string import ascii_uppercase
from typing import NamedTuple, Optional

try:
    from click import style
except ModuleNotFoundError:

    def style(text, fg):
        return text


from csp import CSP, Constraint

all_colors = [
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
]


Grid = list[list[str]]


class GridLocation(NamedTuple):
    row: int
    column: int


def generate_grid(rows: int, columns: int) -> Grid:
    return [
        [random.choice(ascii_uppercase) for c in range(columns)] for r in range(rows)
    ]


def display_grid(grid: Grid) -> None:
    for row in grid:
        print("|".join(row))


def generate_domain(word: str, grid: Grid) -> list[list[GridLocation]]:
    domain: list[list[GridLocation]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    length: int = len(word)
    for row in range(height):
        for col in range(width):
            columns: range = range(col, col + length)
            rows: range = range(row, row + length)
            if col + length <= width:
                # left to right
                domain.append([GridLocation(row, c) for c in columns])
                # diagonal towards bottom right
                if row + length <= height:
                    domain.append([GridLocation(r, col + (r - row)) for r in rows])
            if row + length <= height:
                # top to bottom
                domain.append([GridLocation(r, col) for r in rows])
                # diagonal towards bottom left
                if col - length >= 0:
                    domain.append([GridLocation(r, col - (r - row)) for r in rows])
    return domain


class WordSearchConstraint(Constraint[str, list[GridLocation]]):
    def __init__(self, words: list[str]) -> None:
        super().__init__(words)
        self.words: list[str] = words

    def satisfied(self, assignment: dict[str, list[GridLocation]]) -> bool:
        # if there are duplicates grid locations, then there is an overlap
        all_locations: list[GridLocation] = [
            locs for values in assignment.values() for locs in values
        ]
        return len(set(all_locations)) == len(all_locations)


if __name__ == "__main__":
    grid: Grid = generate_grid(9, 9)
    words: list[str] = [
        "TEHRAN",
        "GILAN",
        "ILAM",
        "KHUZESTAN",
        "KERMAN",
        "YAZD",
        "ESFAHAN",
        "GOLESTAN",
        "ALBORZ",
    ]
    random.shuffle(words)
    random.shuffle(all_colors)

    locations: dict[str, list[list[GridLocation]]] = {}
    for w in words:
        locations[w] = generate_domain(w, grid)

    csp: CSP[str, list[GridLocation]] = CSP(words, locations)
    csp.add_constraint(WordSearchConstraint(words))

    result: Optional[dict[str, list[GridLocation]]] = csp.backtracking()
    if result is None:
        print("No solution found")
    else:
        for color, (word, grid_locations) in zip(all_colors, result.items()):
            # random reverse half time
            if random.choice([True, False]):
                grid_locations.reverse()

            for idx, letter in enumerate(word):
                row, col = grid_locations[idx].row, grid_locations[idx].column
                grid[row][col] = style(letter, fg=color)

        display_grid(grid)
