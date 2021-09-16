# Search Problems

As the book say, we can generally call most of computer science problems, search problems, even the state-of-the-art problems such as deep learning.

## 2.1 DNA Search

Genes are represented as a sequence of the characters: $A, C, G, T$. Do you remember compression problem?

* Each letter is called *nucleotide*
* Combination of three nucleotides forms a ***codon***

A common task in bio-informatics software is to **search for** a particular codon.

- [ ] Type Aliasing, Codon, Gene
- [ ] Nucleotide (`IntEnum`), linear_contains, binary_contains
- [ ] generic_search

[Usefulness of Enum in Python](https://stackoverflow.com/questions/37601644/python-whats-the-enum-type-good-for), [Anther useful link to Enum](https://florian-dahlitz.de/articles/why-you-should-use-more-enums-in-python)

dna_search on Github



## 2.2 Maze solving

DFS

BFS

A*

$f(n) = g(n) + h(n)$

$g(n)$ = examines the cost to get to a particular state.

$h(n)$ = gives an **estimate** of the cost to get **from the state in question** to the **goal state**.

if the estimation is admissible, then it can be proved that the final path found will be optimal.

* An admissible heuristic is one that **never overestimates** the cost to reach the goal

When choosing the next state to explore from the frontier, an A* search picks the one with the **lowest** $f(n)$. This is how it distinguishes itself from BFS and DFS.

<img src="assets/distance-02.png" style="zoom:50%"/>

<img src="assets/distance-01.png" style="zoom:50%"/>

## 2.3 Missionaries and cannibals

<img src="assets/missionaries-01.png" style="zoom:50%"/>



## 2.4 Real-world applications
