"""
Maze generation animator.
"""

import time
import random
from terminal_controls import clear_screen, hide_cursor, show_cursor
from frame_renderer import FrameRenderer

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
        
        This shows the REAL-TIME ANIMATION LOOP:
        1. Render initial state to buffer
        2. Display buffer to screen
        3. Loop: generate one step, render to buffer, display
        4. Buffer is reused (cleared and refilled) each iteration
        
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

        # STEP 1: Initial render - everything solid
        self.renderer.render_full(show_visited=False)  # Fill buffer
        self.renderer.display()  # Display buffer
        time.sleep(0.5)
        
        # Start generation
        start_cell = grid[start_y][start_x]
        stack = [start_cell]
        start_cell.visited = True

        # ANIMATION LOOP: Generate and render each step
        while len(stack) > 0:
            current = stack[-1]
            neighbors = self.generator._get_unvisited_neighbors(current)

            if len(neighbors) == 0:
                stack.pop()
            else:
                neighbor, direction = random.choice(neighbors)
                self.generator._carve_passage(current, neighbor, direction)
                neighbor.visited = True
                stack.append(neighbor)
            
            # STEP 2: Render current state (fills buffer with new content)
            self.renderer.render_full(current_cell=current, show_visited=True)
            
            # STEP 3: Display buffer to screen
            self.renderer.display()
            
            # STEP 4: Wait (creates animation effect)
            time.sleep(delay)
        
        # Final render
        self.renderer.render_full(show_visited=True)
        self.renderer.display()
        
        show_cursor()
        print("\n")