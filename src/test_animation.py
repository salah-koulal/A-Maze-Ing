from maze_generator_BFS import MazeGenerator
from maze_renderer import animate_text_slide, render_maze
gen = MazeGenerator(20, 10, 45)
pattern = animate_text_slide("/home/wabbad/A_maze_IN/Maze-salah/src/1337.txt")
gen.apply_42_pattern()
gen.generate()
render_maze(gen)



