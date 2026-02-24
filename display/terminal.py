from dummy_gen import MazeGenerator


def render(grid, width, height, entry, exit_):
    print("+" + ("---+" * width))
    for y in range(height):
        row = "|"
        for x in range(width):
            cell = grid[y][x]
            if (x, y) == entry:
                interior = " E "
            elif (x, y) == exit_:
                interior = " X "
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
    render(gen.grid, gen.width, gen.height, entry=(0, 0), exit_=(19, 14))
