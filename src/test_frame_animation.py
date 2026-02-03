from maze_generator_DFS import MazeGenerator
from maze_animator import MazeAnimator

# Create maze
gen = MazeGenerator(20, 12, 9)
gen.apply_42_pattern()

# Animate
animator = MazeAnimator(gen)
animator.animate_generation(delay=0.05)