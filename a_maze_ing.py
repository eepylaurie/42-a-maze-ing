"""Entry point for the A-Maze-ing maze generator."""

import sys

from core.config_parser import parse_config
from core.output_writer import write_output
from display.curses_display import run
from mazegen.generator import MazeGenerator


def main() -> None:
    """Run the maze generator from a config file."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    config = parse_config(sys.argv[1])
    if config is None:
        sys.exit(1)

    seed = config.get("SEED")
    gen = MazeGenerator(
        width=config["WIDTH"],
        height=config["HEIGHT"],
        seed=seed,
        perfect=config["PERFECT"],
    )
    gen.generate(start_pos=config["ENTRY"])

    write_output(
        config["OUTPUT_FILE"],
        gen.get_hex_layout(),
        config["ENTRY"],
        config["EXIT"],
        gen.solve(start=config["ENTRY"], end=config["EXIT"]),
    )

    run(
        width=config["WIDTH"],
        height=config["HEIGHT"],
        entry=config["ENTRY"],
        exit_=config["EXIT"],
        seed=seed,
    )


if __name__ == "__main__":
    main()
