"""
Maze generation animator.
"""

import time
import random
from ..utils.terminal_controls import clear_screen, hide_cursor, show_cursor
from .frame_renderer import FrameRenderer

class MazeAnimator:
    def __init__(self, maze_generator):
        """
        Initialize animator.
        
        Args:
            maze_generator: MazeGenerator instance
        """
        self.generator = maze_generator
        self.renderer = FrameRenderer(maze_generator)
    
    def animate_generation(self, start_x=0, start_y=0, delay=0.05):
        """
        Animate the maze generation process.
        
        Args:
            start_x: Starting cell X
            start_y: Starting cell Y
            delay: Delay between frames in seconds
        """
        grid = self.generator.grid
        
        # Reset
        for row in grid:
            for cell in row:
                if cell.walls != 15:
                    cell.visited = False
        
        # Setup
        clear_screen()
        hide_cursor()

        # Initial render - everything solid
        self.renderer.render_full(show_visited=False)
        self.renderer.display()
        time.sleep(0.5)
        
        def update_frame(current_cell):
            self.renderer.render_full(current_cell=current_cell, show_visited=True)
            self.renderer.display()
            time.sleep(delay)
            
        # Start generation using the generator's logic
        self.generator.generate(start_x=start_x, start_y=start_y, callback=update_frame)
            

        
        # Final render
        self.renderer.render_full(show_visited=True)
        self.renderer.display()
        
        show_cursor()
        print("\n")