import sys
from core.config_parser import parse_config
from mazegen.generator import MazeGenerator
from core.output_writer import write_output
from display.curses_display import run


def main() -> None:
    """Run the maze generator from a config file."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    config = parse_config(sys.argv[1])
    if config is None:
        sys.exit(1)

    gen = MazeGenerator(
        width=config["WIDTH"],
        height=config["HEIGHT"],
        seed=config.get("SEED"),
    )
    gen.generate(start_pos=config["ENTRY"])

    write_output(gen, config["OUTPUT_FILE"])

    run(
        width=config["WIDTH"],
        height=config["HEIGHT"],
        entry=config["ENTRY"],
        exit_=config["EXIT"],
    )


if __name__ == "__main__":
    main()
