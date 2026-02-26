"""Curses-based graphical display for A_Maze_ing.

Renders the maze as a colored graphical display in the terminal
using Python's built-in curses library.
"""


import curses
from typing import Optional
from dummy_gen import MazeGenerator

CELL_W = 4
CELL_H = 2

WALL = 1
CORRIDOR = 2
PATH = 3
ENTRY = 4
EXIT = 5
PATTERN = 6


def init_colors() -> None:
    """Initialise curses color pairs for the display."""
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(WALL, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_pair(CORRIDOR, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(PATH, curses.COLOR_CYAN, curses.COLOR_CYAN)
    curses.init_pair(ENTRY, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    curses.init_pair(EXIT, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(PATTERN, curses.COLOR_WHITE, curses.COLOR_WHITE)


def run(
        width: int = 20,
        height: int = 15,
        entry: tuple[int, int] = (0, 0),
        exit_: tuple[int, int] = (19, 14),
) -> None:
    """Start the curses maze display.

    Args:
        width: Maze width in cells.
        height: Maze height in cells.
        entry: Entry coordinates as (x, y).
        exit_: Exit coordinates as (x, y).
    """
    curses.wrapper(lambda stdscr: _main(stdscr, width, height, entry, exit_))


def _main(
        stdscr: curses.window,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
) -> None:
    """Main curses loop.

    Args:
        stdscr: The curses screen object.
        width: Maze width in cells.
        height: Maze height in cells.
        entry: Entry coordinates as (x, y).
        exit_: Exit coordinates as (x, y).
    """
    init_colors()
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "Curses display working! Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    run()
