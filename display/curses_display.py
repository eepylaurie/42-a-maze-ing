import curses
import time
from typing import Optional
from dummy_gen import MazeGenerator

N, E, S, W = 1, 2, 4, 8

CELL_W = 2
CELL_H = 1

WALL = 1
CORRIDOR = 2
PATH = 3
ENTRY_COLOR = 4
EXIT_COLOR = 5
PATTERN_COLOR = 6


def init_colors() -> None:
    """Initialise curses color pairs for the display."""
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(WALL, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_pair(CORRIDOR, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(PATH, curses.COLOR_CYAN, curses.COLOR_CYAN)
    curses.init_pair(ENTRY_COLOR, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    curses.init_pair(EXIT_COLOR, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(PATTERN_COLOR, curses.COLOR_WHITE, curses.COLOR_WHITE)


def draw_cell(
    stdscr: curses.window,
    x: int,
    y: int,
    cell: int,
    color_pair: int,
    width: int,
    height: int,
) -> None:
    """Draw a single maze cell at position (x, y).

    Args:
        stdscr: The curses screen object.
        x: Cell column in maze coordinates.
        y: Cell row in maze coordinates.
        cell: Wall bitmask for this cell.
        color_pair: Curses color pair to use for the cell interior.
    """
    row = y * (CELL_H + 1) + 1
    col = x * (CELL_W + 1) + 1

    wall_pair = curses.color_pair(WALL)
    cell_pair = curses.color_pair(color_pair)

    try:
        # 1. Draw the center of the cell
        for r in range(CELL_H):
            stdscr.addstr(row + r, col, " " * CELL_W, cell_pair)

        # 2. Always draw the North-West corner pillar
        stdscr.addstr(row - 1, col - 1, " ", wall_pair)

        # 3. Draw North Wall
        if cell & N or y == 0:
            stdscr.addstr(row - 1, col, " " * CELL_W, wall_pair)

        # 4. Draw West Wall
        if cell & W or x == 0:
            for r in range(CELL_H):
                stdscr.addstr(row + r, col - 1, " ", wall_pair)

        # 5. Draw Right/Bottom outer boundaries
        if x == width - 1:
            for r in range(CELL_H + 1):
                stdscr.addstr(row + r - 1, col + CELL_W, " ", wall_pair)

        if y == height - 1:
            stdscr.addstr(row + CELL_H, col - 1, " " * (CELL_W + 2), wall_pair)

    except curses.error:
        pass


def draw_maze(
    stdscr: curses.window,
    grid: list[list[int]],
    width: int,
    height: int,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: Optional[list[tuple[int, int]]] = None,
    show_path: bool = False,
) -> None:
    """Draw the full maze on screen.

    Args:
        stdscr: The curses screen object.
        grid: 2D list of wall bitmasks.
        width: Maze width in cells.
        height: Maze height in cells.
        entry: Entry coordinates as (x, y).
        exit_: Exit coordinates as (x, y).
        path: List of (x, y) coordinates forming the solution path.
        show_path: Whether to display the solution path.
    """
    if path is None:
        path = []

    stdscr.clear()

    for y in range(height):
        for x in range(width):
            cell = grid[y][x]

            if (x, y) == entry:
                color = ENTRY_COLOR
            elif (x, y) == exit_:
                color = EXIT_COLOR
            elif show_path and (x, y) in path:
                color = PATH
            elif cell == 15:
                color = PATTERN_COLOR
            else:
                color = CORRIDOR

            draw_cell(stdscr, x, y, cell, color, width, height)

    stdscr.refresh()


def get_path(
    gen: MazeGenerator,
    entry: tuple[int, int],
    exit_: tuple[int, int],
) -> list[tuple[int, int]]:
    """Convert solution string to list of (x, y) coordinates.

    Args:
        gen: A MazeGenerator instance that has already called generate().
        entry: Entry coordinates as (x, y).
        exit_: Exit coordinates as (x, y).

    Returns:
        A list of (x, y) tuples representing the solution path.
    """
    path = []
    x, y = entry
    directions: dict[str, tuple[int, int]] = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0),
    }
    solution = gen.solve(start=entry, end=exit_)
    for move in solution:
        dx, dy = directions[move]
        x, y = x + dx, y + dy
        path.append((x, y))
    return path


def show_start_screen(stdscr: curses.window) -> None:
    """Display animated start screen before the maze appears.

    Args:
        stdscr: The curses screen object.
    """
    stdscr.clear()
    screen_h, screen_w = stdscr.getmaxyx()
    letters = {
        "A": [
            "XXXXX",
            "X...X",
            "XXXXX",
            "X...X",
            "X...X",
        ],
        "M": [
            "XXXXX",
            "X.X.X",
            "X.X.X",
            "X.X.X",
            "X.X.X",
        ],
        "Z": [
            "XXXXX",
            "....X",
            "XXXXX",
            "X....",
            "XXXXX",
        ],
        "E": [
            "XXXXX",
            "X....",
            "XXXXX",
            "X....",
            "XXXXX",
        ],
        "I": [
            "XXXXX",
            "..X..",
            "..X..",
            "..X..",
            "XXXXX",
        ],
        "N": [
            "XXXXX",
            "X...X",
            "X...X",
            "X...X",
            "X...X",
        ],
        "G": [
            "XXXXX",
            "X....",
            "X.XXX",
            "X...X",
            "XXXXX",
        ],
        "_": [
            ".....",
            ".....",
            ".....",
            ".....",
            "XXXXX",
        ],
        " ": [
            ".....",
            ".....",
            ".....",
            ".....",
            ".....",
        ],
    }
    title = "A_MAZE_ING"
    cell_w = 2
    spacing = 1
    total_w = len(title) * (5 * cell_w + spacing)
    start_col = max(0, screen_w // 2 - total_w // 2)
    start_row = max(0, screen_h // 2 - 8)
    blocks = []
    for i, char in enumerate(title):
        letter = letters.get(char, letters[" "])
        letter_col = start_col + i * (5 * cell_w + spacing)
        for row_idx, row in enumerate(letter):
            for col_idx, pixel in enumerate(row):
                if pixel == "X":
                    blocks.append((
                        start_row + row_idx,
                        letter_col + col_idx * cell_w,
                    ))
    import random as rnd
    rnd.shuffle(blocks)
    for row, col in blocks:
        try:
            stdscr.addstr(row, col, " " * cell_w, curses.color_pair(WALL))
            stdscr.refresh()
            time.sleep(0.01)
        except curses.error:
            pass
    prompt = "Press any key to start..."
    try:
        stdscr.addstr(
            start_row + 10,
            screen_w // 2 - len(prompt) // 2,
            prompt,
        )
    except curses.error:
        pass
    stdscr.refresh()
    stdscr.getch()


def show_menu(
        stdscr: curses.window,
        show_path: bool,
        width: int,
        height: int,
) -> str:
    """Display an interactive navigable menu.

    Args:
        stdscr: The curses screen object.
        show_path: Current path visibility state (to show correct label).

    Returns:
        A string indicating the selected action:
        'regenerate', 'path', 'color', 'quit'.
    """
    options = [
        "Re-generate maze",
        "Show path" if not show_path else "Hide path",
        "Rotate colors",
        "Quit",
    ]
    actions = ["regenerate", "path", "color", "quit"]
    selected = 0
    screen_h, screen_w = stdscr.getmaxyx()
    maze_bottom = height * (CELL_H + 1) + 2
    menu_start_row = maze_bottom + 1
    maze_width_cols = width * (CELL_W + 1) + 1
    center_col = maze_width_cols // 2
    while True:
        for i in range(len(options)):
            try:
                stdscr.addstr(menu_start_row + i, 0, " " * screen_w)
            except curses.error:
                pass
        for i, option in enumerate(options):
            max_len = max(len(o) for o in options) + 6
            col = center_col - max_len // 2
            try:
                if i == selected:
                    stdscr.addstr(
                        menu_start_row + i,
                        col,
                        f" > {option} ",
                        curses.color_pair(WALL) | curses.A_BOLD,
                    )
                else:
                    stdscr.addstr(
                        menu_start_row + i,
                        col,
                        f"   {option} ",
                    )
            except curses.error:
                pass
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)
        elif key in (curses.KEY_ENTER, ord("\n"), ord("\r")):
            return actions[selected]
        elif key == ord("q") or key == ord("4"):
            return ("quit")
        elif key == ord("r") or key == ord("1"):
            return "regenerate"
        elif key == ord("p") or key == ord("2"):
            return "path"
        elif key == ord("c") or key == ord("3"):
            return "color"


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


def animate_path(
        stdscr: curses.window,
        grid: list[list[int]],
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        path: list[tuple[int, int]],
        delay: float = 0.02,
) -> None:
    """Animate the solution path cell by cell.

    Args:
        stdscr: The curses screen object.
        grid: 2D list of wall bitmasks.
        width: Maze width in cells.
        height: Maze height in cells.
        entry: Entry coordinates as (x, y).
        exit_: Exit coordinates as (x, y).
        path: List of (x, y) coordinates forming the solution path.
        delay: Time in seconds to wait between drawing each cell.
    """
    for x, y in path:
        if (x, y) not in (entry, exit_):
            draw_cell(stdscr, x, y, grid[y][x], PATH, width, height)
            stdscr.refresh()
            time.sleep(delay)


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
    try:
        curses.curs_set(0)
    except curses.error:
        pass

    stdscr.keypad(True)

    show_start_screen(stdscr)

    wall_colors = [
        curses.COLOR_YELLOW,
        curses.COLOR_GREEN,
        curses.COLOR_BLUE,
        curses.COLOR_WHITE,
    ]
    color_index = 0
    seed = 42
    show_path = False

    gen = MazeGenerator(width=width, height=height, seed=seed)
    gen.generate(start_pos=entry)
    path = get_path(gen, entry, exit_)

    while True:
        curses.init_pair(
            WALL,
            wall_colors[color_index],
            wall_colors[color_index],
        )

        draw_maze(
            stdscr,
            gen.grid,
            width,
            height,
            entry,
            exit_,
            path,
            show_path,
        )

        action = show_menu(stdscr, show_path, width, height)
        if action == "quit":
            break
        elif action == "regenerate":
            seed += 1
            gen = MazeGenerator(width=width, height=height, seed=seed)
            gen.generate(start_pos=entry)
            path = get_path(gen, entry, exit_)
            if show_path:
                draw_maze(
                    stdscr,
                    gen.grid,
                    width,
                    height,
                    entry,
                    exit_,
                    path,
                    show_path=False
                )
                animate_path(
                    stdscr,
                    gen.grid,
                    width,
                    height,
                    entry,
                    exit_,
                    path,
                )
        elif action == "path":
            show_path = not show_path
            if show_path:
                animate_path(
                    stdscr,
                    gen.grid,
                    width,
                    height,
                    entry,
                    exit_,
                    path,
                )
        elif action == "color":
            color_index = (color_index + 1) % len(wall_colors)


if __name__ == "__main__":
    run()
