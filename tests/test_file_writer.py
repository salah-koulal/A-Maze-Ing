from src.maze_generator_prim import MazeGenerator
from src.file_writer import write_maze_to_file

# Generate small maze
gen = MazeGenerator(5, 5, seed=42)
gen.generate()

write_maze_to_file(
    grid=gen.grid,
    entry=(0, 0),
    exit=(4, 4),
    path="EESSEENN",  # Dummy path just for testing
    filename="test_output.txt"
)

print("✅ File written! Check test_output.txt")

with open("test_output.txt") as f:
    print(f.read())