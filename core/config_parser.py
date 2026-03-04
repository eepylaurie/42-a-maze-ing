"""Configuration file parser for A-Maze-ing."""

REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


def parse_config(filename: str) -> dict[str, object] | None:
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

    return config
