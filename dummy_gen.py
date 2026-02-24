import random


class MazeGenerator:
    def __init__(self, width, height, seed=None):
        self.width = width
        self.height = height
        if seed:
            random.seed(seed)
        self.grid = [[15 for _ in range(width)] for _ in range(height)]

    def generate(self, start_pos=(0, 0)):
        for y in range(self.height):
            for x in range(self.width):
                walls = 15
                if random.random() > 0.5 and x + 1 < self.width:
                    walls &= ~2
                    self.grid[y][x+1] &= ~8
                if random.random() > 0.5 and y + 1 < self.height:
                    walls &= ~4
                    self.grid[y+1][x] &= ~1
                self.grid[y][x] = walls
