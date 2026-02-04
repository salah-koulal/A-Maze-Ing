from src.mazegen import MazeGenerator
import os

# Create a dummy config if one doesn't exist for testing
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
# Solve
solution_path = generator.get_solution(maze)
print(f"Entry: {generator.config.get('ENTRY')}")
print(f"Exit: {generator.config.get('EXIT')}")
print(f"Solution path: {solution_path}")

# Write to file
# Write to file
generator.generator.write_to_hex_file("maze_output.txt", generator.config['ENTRY'], generator.config['EXIT'], path=solution_path)

# Verify visual path
print("Drawing maze with path:")
generator.generator.show_path = True
generator.draw_maze()


# run the interactive menu
# generator.run()