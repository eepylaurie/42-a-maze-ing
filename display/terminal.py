from dummy_gen import MazeGenerator


def render(grid, width, height, entry, exit_, path=None):
    if path is None:
        path = []
    print("+" + ("---+" * width))
    for y in range(height):
        row = "|"
        for x in range(width):
            cell = grid[y][x]
            if (x, y) == entry:
                interior = " E "
            elif (x, y) == exit_:
                interior = " X "
            elif (x, y) in path:
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


if __name__ == "__main__":
    gen = MazeGenerator(width=20, height=15, seed=42)
    gen.generate(start_pos=(0, 0))
    path = []
    x, y = 0, 0
    directions = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    solution = gen.solve(start=(0, 0), end=(19, 14))
    for move in solution:
        dx, dy = directions[move]
        x, y = x + dx, y + dy
        path.append((x, y))
    render(
        gen.grid,
        gen.width,
        gen.height,
        entry=(0, 0),
        exit_=(19, 14),
        path=path
    )
