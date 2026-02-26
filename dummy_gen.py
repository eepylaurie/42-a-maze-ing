# import random


# class MazeGenerator:
#     def __init__(self, width, height, seed=None):
#         self.width = width
#         self.height = height
#         if seed:
#             random.seed(seed)
#         self.grid = [[15 for _ in range(width)] for _ in range(height)]

#     def generate(self, start_pos=(0, 0)):
#         for y in range(self.height):
#             for x in range(self.width):
#                 walls = 15
#                 if random.random() > 0.5 and x + 1 < self.width:
#                     walls &= ~2
#                     self.grid[y][x+1] &= ~8
#                 if random.random() > 0.5 and y + 1 < self.height:
#                     walls &= ~4
#                     self.grid[y+1][x] &= ~1
#                 self.grid[y][x] = walls

#     def solve(self, start, end):
#         path = ""
#         x, y = start
#         while x < end[0]:
#             path += "E"
#             x += 1
#         return path

import random
from collections import deque
from typing import List, Tuple, Set, Optional

N, E, S, W = 1, 2, 4, 8
OPPOSITE = {N: S, S: N, E: W, W: E}
MOVE = {N: (0, -1), S: (0, 1), E: (1, 0), W: (-1, 0)}


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: Optional[int] = None):
        self.width = width
        self.height = height
        if seed is not None:
            random.seed(seed)

        self.grid = [[15 for _ in range(width)] for _ in range(height)]
        self.visited: Set[Tuple[int, int]] = set()

    def _apply_42_pattern(self) -> None:
        offset_x = max(0, self.width // 2 - 3)
        offset_y = max(0, self.height // 2 - 2)

        pattern = [
            (0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2),
            (2, 3), (2, 4), (4, 0), (5, 0), (6, 0), (6, 1), (6, 2),
            (5, 2), (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)
        ]

        for px, py in pattern:
            nx, ny = offset_x + px, offset_y + py
            if 0 <= nx < self.width and 0 <= ny < self.height:
                self.visited.add((nx, ny))

    def generate(self, start_pos: Tuple[int, int] = (0, 0)) -> None:
        self._apply_42_pattern()
        if start_pos in self.visited:
            for x in range(self.width):
                for y in range(self.height):
                    if (x, y) not in self.visited:
                        self._backtrack(x, y)
                        return
        self._backtrack(start_pos[0], start_pos[1])

    def _backtrack(self, x: int, y: int) -> None:
        self.visited.add((x, y))
        directions = [N, E, S, W]
        random.shuffle(directions)

        for direction in directions:
            dx, dy = MOVE[direction]
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < self.width
                and 0 <= ny < self.height
                and (nx, ny) not in self.visited
            ):
                self.grid[y][x] &= ~direction
                self.grid[ny][nx] &= ~OPPOSITE[direction]
                self._backtrack(nx, ny)

    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> str:
        queue = deque([(start, "")])
        visited_solve = {start}
        dir_map = {N: 'N', E: 'E', S: 'S', W: 'W'}

        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == end:
                return path

            for direction, (dx, dy) in MOVE.items():
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (
                        not (self.grid[y][x] & direction)
                        and (nx, ny) not in visited_solve
                    ):
                        visited_solve.add((nx, ny))
                        queue.append(((nx, ny), path + dir_map[direction]))
        return ""

    def get_hex_layout(self) -> List[str]:
        return ["".join(f"{cell:X}" for cell in row) for row in self.grid]

    def validate_no_3x3(self) -> bool:
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                cells = [
                    self.grid[y+dy][x+dx] == 0
                    for dy in range(3)
                    for dx in range(3)
                ]
                if all(cells):
                    return False
        return True
