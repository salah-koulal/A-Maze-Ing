#!/usr/bin/env python3
"""
A-Maze-ing: Maze Generator and Visualizer
Main entry point for the program.
"""

import sys
from src.config_parser import load_config



def main() -> None:
    """Main program entry point."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    try:
            config = load_config(config_file)
            print(f"Config loaded: {config}")
            # TODO: - maze generation!
            
    except FileNotFoundError:
            print(f"Error: File not found")
            sys.exit(1)
    except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()