"""
Prim's algorithm maze generation animator.
Uses real-time rendering with screen buffer and terminal controls.
"""

import time
import random
from terminal_controls import clear_screen, hide_cursor, show_cursor
from frame_renderer import FrameRenderer


class PrimMazeAnimator:
    def __init__(self, maze_generator):
        """
        Initialize animator for Prim's algorithm.
        
        Args:
            maze_generator: MazeGenerator instance with Prim's algorithm
        """
        self.generator = maze_generator
        self.renderer = FrameRenderer(maze_generator)
    
    def animate_generation(self, delay=0.03):
        """
        Animate the maze generation process using Prim's algorithm.
        
        Args:
            delay: Delay between frames in seconds
        """
        grid = self.generator.grid
        width = self.generator.width
        height = self.generator.height
        
        # Reset all cells
        for row in grid:
            for cell in row:
                if cell.enabled:  # Don't reset pattern cells
                    cell.visited = False
        
        # Setup terminal
        clear_screen()
        hide_cursor()

        # Initial render - everything solid
        self.renderer.render_full(show_visited=False)
        self.renderer.display()
        time.sleep(0.5)
        
        # Find a valid start cell (not a pattern cell)
        start_cell = None
        for y in range(height):
            for x in range(width):
                if grid[y][x].enabled and not start_cell:
                    start_cell = grid[y][x]
                    break
            if start_cell:
                break
        
        if not start_cell:
            show_cursor()
            return
        
        # Mark start cell as visited
        start_cell.visited = True
        
        # Frontier: list of (current_cell, neighbor_cell, direction) tuples
        frontier = []
        
        # Add initial frontier walls
        for neighbor, direction in self._get_unvisited_neighbors(start_cell):
            frontier.append((start_cell, neighbor, direction))
        
        # Render initial state
        self.renderer.render_full(current_cell=start_cell, show_visited=True)
        self.renderer.display()
        time.sleep(delay)
        
        # Main Prim's algorithm loop
        while frontier:
            # Pick random wall from frontier
            wall_index = random.randint(0, len(frontier) - 1)
            current_cell, neighbor_cell, direction = frontier.pop(wall_index)
            
            # If neighbor hasn't been visited, carve passage
            if not neighbor_cell.visited:
                # Carve passage
                self._carve_passage(current_cell, neighbor_cell, direction)
                neighbor_cell.visited = True
                
                # Render current state with neighbor as current cell
                self.renderer.render_full(current_cell=neighbor_cell, show_visited=True)
                self.renderer.display()
                time.sleep(delay)
                
                # Add new walls to frontier
                for next_neighbor, next_dir in self._get_unvisited_neighbors(neighbor_cell):
                    frontier.append((neighbor_cell, next_neighbor, next_dir))
        
        # Final render
        self.renderer.render_full(show_visited=True)
        self.renderer.display()
        
        show_cursor()
        print("\n")
    
    def _get_unvisited_neighbors(self, cell):
        """
        Get all unvisited neighbors of a cell.
        
        Args:
            cell: Cell to get neighbors for
            
        Returns:
            List of (neighbor_cell, direction) tuples
        """
        neighbors = []
        directions = {
            'N': (0, -1),
            'E': (1, 0),
            'S': (0, 1),
            'W': (-1, 0)
        }
        
        for direction, (dx, dy) in directions.items():
            nx = cell.x + dx
            ny = cell.y + dy
            
            if 0 <= nx < self.generator.width and 0 <= ny < self.generator.height:
                neighbor = self.generator.grid[ny][nx]
                if neighbor.enabled and not neighbor.visited:
                    neighbors.append((neighbor, direction))
        
        return neighbors
    
    def _carve_passage(self, current, neighbor, direction):
        """
        Carve passage between two cells.
        
        Args:
            current: Current cell
            neighbor: Neighbor cell
            direction: Direction from current to neighbor
        """
        current.remove_wall(direction)
        
        opposites = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        neighbor.remove_wall(opposites[direction])
