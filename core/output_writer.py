from typing import List, Tuple


def save_maze_to_file(
    file_path: str,
    hex_grid: List[str],
    entry: Tuple[int, int],
    exit_pos: Tuple[int, int],
    path: str
) -> None:
    """
    Speichert das generierte Labyrinth im geforderten Format in eine Textdatei.

    Args:
        file_path (str): Der Pfad zur Ausgabedatei (z.B. 'maze.txt').
        hex_grid (List[str]): Das Labyrinth als Liste von Hex-Strings
        (aus generator.get_hex_layout()).
        entry (Tuple[int, int]): Die Koordinaten des Eingangs (x, y).
        exit_pos (Tuple[int, int]): Die Koordinaten des Ausgangs (x, y).
        path (str): Der vom Solver berechnete Pfad (z.B. 'SESSW').
    """
    with open(file_path, 'w') as f:
        # 1. Das Hex-Labyrinth schreiben (Zeile für Zeile)
        for row in hex_grid:
            f.write(row + "\n")
        # 2. Eintritts- und Austrittspunkte (Format: x,y)
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_pos[0]},{exit_pos[1]}\n")
        # 3. Den Lösungspfad schreiben
        f.write(path + "\n")
