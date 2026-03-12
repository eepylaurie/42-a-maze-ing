*This project has been created as part of the 42 curriculum by ekypraio, lmatthes.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator written in Python. It takes a configuration file,
generates a perfect maze using a recursive backtracking algorithm, writes it to a
file in hexadecimal format, and displays it visually in the terminal using curses.
The maze includes a hidden "42" pattern, a BFS-based solver, and an interactive
display with color themes and animated path visualization.

## Instructions

### Installation

``` bash
make install
```

### Run

``` bash
make run
```

Or directly:

``` bash
python3 a_maze_ing.py config.txt
```

### Lint

``` bash
make lint
```

### Debug

``` bash
make debug
```

### Clean

``` bash
make clean
```

### Build the pip package

``` bash
make build
```

## Configuration File

The configuration file must contain one `KEY=VALUE` pair per line.
Lines starting with `# ` are treated as comments and ignored.

| **Key** | **Description** | **Example** |
| ------- | --------------- | ----------- |
| `WIDTH` | Maze width in cells | `WIDTH=20` |
| `HEIGHT` | Maze height in cells | `HEIGHT=15`|
| `ENTRY` | Entry coordinates (x, y) | `ENTRY=0,0` |
| `EXIT` | Exit coordinates (x, y) | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Generate a perfect maze | `PERFECT=True` |
| `SEED` | Optional seed for reproducibility | `SEED=42` |

Example `config.txt`:
```
WIDTH=20
HEIGHT=15
SEED=42
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

## Maze Generation Algorithm

The maze is generated using the **randomized recursive backtracking** algorithm (also known as recursive DFS). Starting from a given cell, the algorithm recursively visits unvisited neighbours in a random order, carving passages between them, and backtracks when no unvisited neighbours remain.

### Why this algorithm?

Recursive backtracking was chosen because it is straightforward to implement, produces perfect mazes (exactly one path between any two cells), and generates mazes with long, winding corridors that feel natural and challenging. It maps cleanly onto a bitmask cell representation and integrates well with the "42" pattern reservation logic.

## Display

The terminal display is built with Python's `curses` library. User interactions:

- **Arrow keys + Enter** — Navigate the menu
- **Re-generate** — Generate a new maze
- **Show/Hide path** — Animate and display the shortest solution path
- **Rotate colors** — Cycle through color themes (42, Laurie, Elef)
- **Quit** — Exit the program

## Reusable Module

The maze generation logic is packaged as a standalone pip-installable module located at the root of this repository.

### Installation

``` bash
pip install mazegen-ekypraio-lmatthes-1.0.0-py3-none-any.whl
```

### Usage

``` python
from mazegen.generator import MazeGenerator

# Instantiate with custom size and seed
gen = MazeGenerator(width=20, height=15, seed=42)

# Generate the maze starting from (0, 0)
gen.generate(start_pos=(0, 0))

# Access the grid (2D list of bitmasks)
print(gen.grid)

# Get hex layout (list of strings, one per row)
for row in gen.get_hex_layout():
    print(row)

# Solve: returns path as N/E/S/W string
solution = gen.solve(start=(0, 0), end=(19, 14))
print(solution)
```

### Parameters

| **Parameter** | **Type** | **Description** |
| ------------- | -------- | --------------- |
| `width` | `int` | Maze width in cells |
| `height` | `int` | Maze height in cells |
| `seed` | `int` | Optional seed for reproducibility |

### Methods

| **Method** | **Returns** | **Description** |
| ---------- | ----------- | --------------- |
| `generate(start_pos)` | `None` | Generate the maze |
| `solve(start, end)` | `str` | BFS shortest path as N/E/S/W string |
| `get_hex_layout()` | `list[str]` | Maze as hex strings |
| `validate_no_2x2_area()` | `bool` | Check no illegal open areas exist |

## Team and Project Management

### Roles

- **ekypraio** — Maze generator (`mazegen/generator.py`), package configuration
  (`pyproject.toml`), config parser (`core/config_parser.py`), output writer (`core/output_writer.py`)
- **lmatthes** — Terminal display (`display/curses_display.py`), entry point
  (`a_maze_ing.py`), Makefile, requirements
- **Shared** — Configuration file format, integration, code review, git workflow

### Planning

We started by defining a clear split: one person on the generator, one on the
display. We worked on separate git branches and met every other day to explain
progress, review each other's code, and integrate. The plan stayed largely on
track — the main adjustment was spending more time than expected on the curses
display and resolving merge conflicts as we integrated the two halves.

### What worked well

The branch-based workflow kept our work independent and clean. Peer reviews
helped us catch bugs and inconsistencies early. The bitmask representation for
walls worked well across both the generator and the display.

### What could be improved

This was our first time working with git branches and we ran into merge conflicts
and push issues a few times. With more experience we would have communicated
more explicitly about shared files like `config_parser.py` to avoid conflicts.

### Tools used

- **VS Code** — Primary editor for both team members
- **Git / GitHub** — Version control with feature branches and pull requests
- **pip / venv** — Dependency management and isolated development environment
- **flake8** — Code style and linting
- **mypy** — Static type checking
- **pytest** — Unit testing
- **Python build** — Packaging the reusable mazegen module

## Resources
- [Artificial Intelligence Search Problem: Solve Maze using Breadth First Search (BFS) Algorithm](https://medium.com/@luthfisauqi17_68455/artificial-intelligence-search-problem-solve-maze-using-breadth-first-search-bfs-algorithm-255139c6e1a3)
- [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Breadth First Search or BFS for a Graph](https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/)
- [Curses — Terminal handling for character-cell displays](https://docs.python.org/3/library/curses.html)
- [Python Curses Module](https://www.w3schools.com/python/ref_module_curses.asp)
- [Creating Menu Display for Terminal](https://www.youtube.com/watch?v=zwMsmBsC1GM)

### AI Usage

AI was used during this project for the following tasks:

- Generating an initial project plan and structure, including file responsibilities per team member
- Suggesting git workflows and commands for branch-based collaboration
- Reviewing code against project requirements (flake8, mypy, docstrings, type hints)
- Debugging type errors and fixing formatting inconsistencies

**All code logic and implementation were written and understood by the team.**