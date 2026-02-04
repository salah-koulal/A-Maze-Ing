#!/usr/bin/env python3
"""
A-Maze-ing: Maze Generator and Visualizer
Main entry point for the program using the mazegen package.
"""

import sys
from src.mazegen import MazeGenerator


def main() -> None:
    """Main program entry point."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        generator = MazeGenerator(config_file)
        generator.run()
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error in configuration: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
