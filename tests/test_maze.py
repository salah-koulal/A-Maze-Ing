from src.maze_generator_prim import MazeGenerator

gen = MazeGenerator(width=3, height=3, seed=2)
gen.generate()

for y in range(gen.height):
    # Top walls
    for x in range(gen.width):
        print("+" if gen.grid[y][x].has_wall('N') else "+", end="")
        print("-" if gen.grid[y][x].has_wall('N') else " ", end="")
    print("+")
    
    # Side walls
    for x in range(gen.width):
        print("|" if gen.grid[y][x].has_wall('W') else " ", end=" ")
    print("|")

# Bottom
print("+" + "-+" * gen.width)