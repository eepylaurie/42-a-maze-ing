"""Configuration file parser for A-Maze-ing."""

from typing import Any

REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


def parse_config(filename: str) -> dict[str, Any] | None:
    """Read and validate the configuration file.

    Args:
        filename: Path to the configuration file.

    Returns:
        Dictionary with configuration values, or None on error.
    """
    config: dict[str, object] = {}

    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                key, value = line.split("=", 1)
                key = key.strip().upper()
                value = value.strip()

                if key in ("WIDTH", "HEIGHT", "SEED"):
                    config[key] = int(value)
                elif key in ("ENTRY", "EXIT"):
                    config[key] = tuple(map(int, value.split(",")))
                elif key == "PERFECT":
                    config[key] = value.lower() == "true"
                else:
                    config[key] = value

    except FileNotFoundError:
        print(f"Error: Config file '{filename}' not found.")
        return None
    except ValueError as e:
        print(f"Error: Invalid value in config file: {e}")
        return None

    missing = REQUIRED_KEYS - config.keys()
    if missing:
        print(f"Error: Missing required keys: {', '.join(sorted(missing))}")
        return None

    width = config.get("WIDTH")
    height = config.get("HEIGHT")
    if not isinstance(width, int) or not isinstance(height, int):
        print("Error: WIDTH and HEIGHT must be integers.")
        return None
    if width < 1 or height < 1:
        print(
            f"Error: Dimensions must be positive "
            f"(got {width}x{height})."
        )
        return None

    entry = config.get("ENTRY")
    exit_ = config.get("EXIT")
    if not isinstance(entry, tuple) or not isinstance(exit_, tuple):
        print("Error: ENTRY/EXIT must be coordinate pairs.")
        return None
    ex, ey = entry
    ox, oy = exit_
    bounds = f"{width}x{height}"
    if not (0 <= ex < width and 0 <= ey < height):
        print(f"Error: ENTRY {entry} out of bounds ({bounds}).")
        return None
    if not (0 <= ox < width and 0 <= oy < height):
        print(f"Error: EXIT {exit_} out of bounds ({bounds}).")
        return None
    if entry == exit_:
        print("Error: ENTRY and EXIT must differ.")
        return None

    return config
