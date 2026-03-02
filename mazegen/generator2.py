"""Labyrinth-Generator mit rekursivem Backtracking und BFS-Solver.

Dieses Modul stellt die MazeGenerator-Klasse bereit, die Labyrinthe
mit dem randomisierten rekursiven Backtracking-Algorithmus generiert,
ein '42'-Muster einbettet und Labyrinthe per Breitensuche löst.
"""


import random
from collections import deque
from typing import Optional

# Himmelsrichtungen als Bit-Konstanten
N, E, S, W = 1, 2, 4, 8
OPPOSITE = {N: S, S: N, E: W, W: E}
MOVE = {N: (0, -1), S: (0, 1), E: (1, 0), W: (-1, 0)}
DIR_MAP = {N: 'N', E: 'E', S: 'S', W: 'W'}

MIN_SIZE_FOR_42 = 10


class MazeGenerator:
    """Modularer Labyrinth-Generator mit Bit-Logik, 42-Muster und BFS."""

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None,
    ) -> None:
        """Initialisiert den Generator.

        Args:
            width: Breite des Labyrinths in Zellen.
            height: Höhe des Labyrinths in Zellen.
            seed: Optionaler Seed für reproduzierbare Ergebnisse.
        """
        self.width = width
        self.height = height
        self.seed = seed
        self.grid: list[list[int]] = []
        self.visited: set[tuple[int, int]] = set()

    def _apply_42_pattern(self) -> None:
        """Reserviert Zellen für das '42'-Muster vor dem Generieren.

        Gibt eine Warnung aus wenn das Labyrinth zu klein ist.
        """
        if self.width < MIN_SIZE_FOR_42 or self.height < MIN_SIZE_FOR_42:
            print("Warning: Maze too small to display '42' pattern.")
            return

        offset_x = max(0, self.width // 2 - 3)
        offset_y = max(0, self.height // 2 - 2)

        # Koordinaten für die Ziffern "4" und "2"
        pattern = [
            (0, 0), (0, 1), (0, 2), (1, 2), (2, 0),
            (2, 1), (2, 2), (2, 3), (2, 4), (4, 0),
            (5, 0), (6, 0), (6, 1), (6, 2), (5, 2),
            (4, 2), (4, 3), (4, 4), (5, 4), (6, 4),
        ]
        for px, py in pattern:
            nx, ny = offset_x + px, offset_y + py
            if 0 <= nx < self.width and 0 <= ny < self.height:
                self.visited.add((nx, ny))

    def generate(self, start_pos: tuple[int, int] = (0, 0)) -> None:
        """Generiert das Labyrinth mit dem Backtracking-Algorithmus.

        Args:
            start_pos: Startkoordinaten für den Algorithmus.
        """
        # Reset für saubere Generierung
        if self.seed is not None:
            random.seed(self.seed)

        self.grid = [
            [15 for _ in range(self.width)]
            for _ in range(self.height)
        ]
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
        """Rekursiver Backtracking-Algorithmus zum Generieren der Gänge.

        Args:
            x: Aktuelle X-Koordinate.
            y: Aktuelle Y-Koordinate.
        """
        self.visited.add((x, y))
        directions = list(MOVE.keys())
        random.shuffle(directions)

        for direction in directions:
            dx, dy = MOVE[direction]
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < self.width
                and 0 <= ny < self.height
                and (nx, ny) not in self.visited
            ):
                # Mauern zwischen aktueller und nächster Zelle entfernen
                self.grid[y][x] &= ~direction
                self.grid[ny][nx] &= ~OPPOSITE[direction]
                self._backtrack(nx, ny)

    def solve(self, start: tuple[int, int], end: tuple[int, int]) -> str:
        """Findet den kürzesten Weg von Start zu Ende mittels BFS.

        Args:
            start: Startpunkt als (x, y).
            end: Zielpunkt als (x, y).

        Returns:
            Pfad als String aus N/E/S/W, oder leerer String, wenn kein Pfad.
        """
        queue: deque[tuple[tuple[int, int], str]] = deque([(start, "")])
        visited_solve: set[tuple[int, int]] = {start}

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
        """Prüft ob ein 2x2 offener Bereich im Labyrinth existiert.

        Returns:
            True wenn kein Verstoß gefunden, False wenn doch.
        """
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                # Check ob die inneren Wände eines 2x2 Blocks alle fehlen
                if (
                    not (self.grid[y][x] & S)
                    and not (self.grid[y][x] & E)
                    and not (self.grid[y + 1][x + 1] & N)
                    and not (self.grid[y + 1][x + 1] & W)
                ):
                    return False
        return True

    def get_hex_layout(self) -> list[str]:
        """Gibt das Labyrinth als Liste von Hex-Strings zurück.

        Returns:
            Liste von Strings, eine pro Zeile, jede Zelle als Hex-Ziffer.
        """
        return ["".join(f"{cell:X}" for cell in row) for row in self.grid]
