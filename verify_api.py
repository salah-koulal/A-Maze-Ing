from src.mazegen import MazeGenerator
import os

# Create a dummy config if one doesn't exist for testing
config_path = "config/default_config.txt"

# Initialize from config file, size and seed are optional
generator = MazeGenerator(config_path, seed="42", size=(15, 10))

# Generate maze
print("Generating maze via API...")
maze = generator.generate_maze()

# Display
print("Drawing maze via API:")
generator.draw_maze(maze)

# Solve
solution_path = generator.get_solution(maze)
print(f"Solution path: {solution_path}")


# run the interactive menu
# generator.run()