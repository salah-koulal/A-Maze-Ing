from maze_generator_BFS import MazeGenerator
from maze_renderer import animate_text_slide, render_maze
gen = MazeGenerator(20, 10, 45)
gen.apply_42_pattern()
gen.generate()
render_maze(gen)



