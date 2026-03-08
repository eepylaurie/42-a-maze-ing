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

- **Arrow keys + Enter** to navigate the menu
- Re-generate a new maze
- Show or hide the shortest solution path (animated)
- Rotate through color themes (42, Laurie, Elef)
- Quit

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

## Resources

### AI Usage