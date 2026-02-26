import random
from collections import deque
from typing import Optional

# Konstanten für die Himmelsrichtungen (Bits)
N, E, S, W = 1, 2, 4, 8
OPPOSITE = {N: S, S: N, E: W, W: E}
MOVE = {N: (0, -1), S: (0, 1), E: (1, 0), W: (-1, 0)}
DIR_MAP = {N: 'N', E: 'E', S: 'S', W: 'W'}


class MazeGenerator:
    """
    Ein modularer Labyrinth-Generator mit Bit-Logik, 42-Muster und BFS-Solver.
    """

    def __init__(self, width: int, height: int, seed: Optional[int] = None):
        """
        Initialisiert den Generator.

        Args:
            width (int): Breite des Labyrinths.
            height (int): Höhe des Labyrinths.
            seed (Optional[int]): Optionaler Seed für reproduzierbare
            Ergebnisse.
        """
        self.width = width
        self.height = height
        if seed is not None:
            random.seed(seed)
        # Initialisierung der Datenstrukturen
        self.grid: list[list[int]] = []
        self.visited: set[tuple[int, int]] = set()

    def _apply_42_pattern(self) -> None:
        """
        Markiert Zellen für das '42'-Muster als besucht,
        um Platz zu reservieren.
        Gibt eine Warnung aus, wenn das Labyrinth kleiner als 10x10 ist.
        """
        if self.width < 10 or self.height < 10:
            print("Warning: Maze too small to display '42' pattern.")
            return

        offset_x = max(0, self.width // 2 - 3)
        offset_y = max(0, self.height // 2 - 2)
        # Koordinaten für die Ziffern "4" und "2"
        pattern = [
            (0, 0), (0, 1), (0, 2), (1, 2), (2, 0),
            (2, 1), (2, 2), (2, 3), (2, 4),
            (4, 0), (5, 0), (6, 0), (6, 1), (6, 2),
            (5, 2), (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)
        ]
        for px, py in pattern:
            nx, ny = offset_x + px, offset_y + py
            if 0 <= nx < self.width and 0 <= ny < self.height:
                self.visited.add((nx, ny))

    def generate(self, start_pos: tuple[int, int] = (0, 0)) -> None:
        """
        Generiert das Labyrinth mit Randomized Backtracking.

        Args:
            start_pos (tuple[int, int]): Startkoordinaten für den Algorithmus.
        """
        # Reset für saubere Generierung
        self.grid = [[15 for _ in range(self.width)]
                     for _ in range(self.height)]
        self.visited = set()

        # Muster reservieren
        self._apply_42_pattern()

        # Startpunkt finden (darf nicht im 42-Muster liegen)
        actual_start = start_pos
        if actual_start in self.visited:
            for y in range(self.height):
                for x in range(self.width):
                    if (x, y) not in self.visited:
                        actual_start = (x, y)
                        break
        self._backtrack(actual_start[0], actual_start[1])

    def _backtrack(self, x: int, y: int) -> None:
        """
        Interner rekursiver Backtracking-Algorithmus.

        Args:
            x (int): Aktuelle X-Koordinate.
            y (int): Aktuelle Y-Koordinate.
        """
        self.visited.add((x, y))
        directions = list(MOVE.keys())
        random.shuffle(directions)

        for direction in directions:
            dx, dy = MOVE[direction]
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < self.width and 0 <= ny < self.height
                and (nx, ny) not in self.visited
            ):
                # Mauern zwischen aktueller und nächster Zelle entfernen
                self.grid[y][x] &= ~direction
                self.grid[ny][nx] &= ~OPPOSITE[direction]
                self._backtrack(nx, ny)

    def solve(self, start: tuple[int, int], end: tuple[int, int]) -> str:
        """
        Findet den kürzesten Weg von Start zu Ende mittels BFS.

        Args:
            start (Tuple[int, int]): Startpunkt (x, y).
            end (Tuple[int, int]): Zielpunkt (x, y).

        Returns:
            str: Pfad als String (z.B. "EENSSW") oder leerer String.
        """
        queue = deque([(start, "")])
        visited_solve = {start}

        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == end:
                return path
            for direction, (dx, dy) in MOVE.items():
                nx, ny = x + dx, y + dy
                # Prüfen, ob Weg offen ist (Bit nicht gesetzt)
                # und innerhalb der Grenzen
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (
                        not (self.grid[y][x] & direction)
                        and (nx, ny) not in visited_solve
                    ):
                        visited_solve.add((nx, ny))
                        queue.append(((nx, ny), path + DIR_MAP[direction]))
        return ""

    def validate_no_2x2_area(self) -> bool:
        """
        Prüft auf 2x2 Bereiche ohne innere Wände.

        Returns:
            bool: True, wenn keine 2x2 Freiflächen existieren, sonst False.
        """
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                # Check ob die inneren Wände eines 2x2 Blocks alle fehlen
                if not (self.grid[y][x] & S) and \
                   not (self.grid[y][x] & E) and \
                   not (self.grid[y+1][x+1] & N) and \
                   not (self.grid[y+1][x+1] & W):
                    return False
        return True

    def get_hex_layout(self) -> list[str]:
        """
        Gibt das Labyrinth als Liste von Hexadezimal-Strings zurück.

        Returns:
            List[str]: Jede Zeile als Hex-String.
        """
        return ["".join(f"{cell:X}" for cell in row) for row in self.grid]