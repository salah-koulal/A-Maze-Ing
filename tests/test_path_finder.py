# test_pathfinder.py
from src.maze_generator_prim import MazeGenerator
from src.path_finder import find_path
from src.file_writer import write_maze_to_file

gen = MazeGenerator(3, 3, seed=1)
gen.generate()

# Find REAL path
path = find_path(gen.grid, (0, 0), (1, 1))
print(f"Path found: {path}")

# Write with real path
write_maze_to_file(gen.grid, (0, 0), (1, 1), path, "output.txt")
