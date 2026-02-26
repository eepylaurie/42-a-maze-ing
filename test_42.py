from dummy_gen import MazeGenerator

print("=== Test 1: Small maze (should print warning) ===")
gen_small = MazeGenerator(width=5, height=5, seed=1)
gen_small.generate()

print("\n=== Test 2: Large maze (should show 42 pattern) ===")
gen_large = MazeGenerator(width=20, height=15, seed=42)
gen_large.generate()

for y, row in enumerate(gen_large.grid):
    for x, cell in enumerate(row):
        if cell == 15:
            print("X", end=" ")
        else:
            print(".", end=" ")
    print()
