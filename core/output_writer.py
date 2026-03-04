"""Output writer for A-Maze-ing."""


def write_output(
    file_path: str,
    hex_grid: list[str],
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
    path: str,
) -> None:
    """Speichert das generierte Labyrinth im geforderten Format in eine
    Textdatei.

    Args:
        file_path: Der Pfad zur Ausgabedatei (z.B. 'maze.txt').
        hex_grid: Das Labyrinth als Liste von Hex-Strings aus get_hex_layout().
        entry: Die Koordinaten des Eingangs (x, y).
        exit_pos: Die Koordinaten des Ausgangs (x, y).
        path: Der vom Solver berechnete Pfad (z.B. 'SESSW').
    """
    try:
        with open(file_path, "w") as f:
            # 1. Das Hex-Labyrinth schreiben (Zeile für Zeile)
            for row in hex_grid:
                f.write(row + "\n")
            # 2. Eintritts- und Austrittspunkte (Format: x,y)
            f.write("\n")
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_pos[0]},{exit_pos[1]}\n")
            # 3. Den Lösungspfad schreiben
            f.write(path + "\n")
    except IOError as e:
        print(f"Error writing output file: {e}")
