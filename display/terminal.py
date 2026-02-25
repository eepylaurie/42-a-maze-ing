from dummy_gen import MazeGenerator


def render(
    grid,
    width,
    height,
    entry,
    exit_,
    path=None,
    show_path=True,
    color="\033[37m"
):
    if path is None:
        path = []
    print(color, end="")
    print("+" + ("---+" * width))
    for y in range(height):
        row = "|"
        for x in range(width):
            cell = grid[y][x]
            if (x, y) == entry:
                interior = " E "
            elif (x, y) == exit_:
                interior = " X "
            elif show_path and (x, y) in path:
                interior = " * "
            else:
                interior = "   "
            if cell & 2:
                row += interior + "|"
            else:
                row += interior + " "
        print(row)
        bottom = "+"
        for x in range(width):
            cell = grid[y][x]
            if cell & 4:
                bottom += "---+"
            else:
                bottom += "   +"
        print(bottom)


def get_path(gen, entry, exit_):
    path = []
    x, y = entry
    directions = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    solution = gen.solve(start=entry, end=exit_)
    for move in solution:
        dx, dy = directions[move]
        x, y = x + dx, y + dy
        path.append((x, y))
    return path


def run(width=20, height=15, entry=(0, 0), exit_=(19, 14)):
    seed = 42
    show_path = False
    colors = ["\033[37m", "\033[32m", "\033[34m", "\033[31m"]
    color_names = ["white", "green", "blue", "red"]
    color_index = 0
    gen = MazeGenerator(width=width, height=height, seed=seed)
    gen.generate(start_pos=entry)
    path = get_path(gen, entry, exit_)
    while True:
        print(colors[color_index], end="")
        render(
            gen.grid,
            width,
            height,
            entry,
            exit_,
            path,
            show_path,
            colors[color_index]
        )
        print("\033[0m", end="")
        print(
            "\nCommands: "
            "[r] regenerate   "
            "[p] toggle path   "
            "[c] change color   "
            "[q] quit"
        )
        command = input("> ").strip().lower()
        if command == "q":
            print("Bye!")
            break
        elif command == "r":
            seed += 1
            gen = MazeGenerator(width=width, height=height, seed=seed)
            gen.generate(start_pos=entry)
            path = get_path(gen, entry, exit_)
            print("Maze regenerated!")
        elif command == "p":
            show_path = not show_path
            status = "shown" if show_path else "hidden"
            print(f"Path {status}.")
        elif command == "c":
            color_index = (color_index + 1) % len(colors)
            print(f"Color changed to {color_names[color_index]}.")
        else:
            print("Unknown command.")


if __name__ == "__main__":
    run()
