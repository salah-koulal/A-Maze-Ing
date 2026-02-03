"""
DFS (Depth-First Search) maze generation algorithm.
Uses recursive backtracking to create perfect mazes.
"""

import random
from typing import List, Set, Tuple
from .maze_base import MazeGeneratorBase, Cell


class DFSMazeGenerator(MazeGeneratorBase):
    """Generate mazes using Depth-First Search (recursive backtracker) algorithm."""
    
    def generate(self, start_x: int = 0, start_y: int = 0) -> List[List[Cell]]:
        """
        Generate maze using DFS algorithm.
        
        The algorithm:
        1. Start at a cell and mark it visited
        2. While there are unvisited neighbors:
           - Choose a random unvisited neighbor
           - Remove the wall between current and neighbor
           - Move to neighbor and repeat (recursion via stack)
        3. When stuck, backtrack (pop from stack)
        
        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            
        Returns:
            The generated maze grid
        """
        # Reset all non-pattern cells to unvisited
        for row in self.grid:
            for cell in row:
                if (cell.x, cell.y) not in self.pattern_cells:
                    cell.visited = False
        
        # Find a valid start cell (not in pattern)
        if (start_x, start_y) in self.pattern_cells:
            # Find first non-pattern cell
            for y in range(self.height):
                for x in range(self.width):
                    if (x, y) not in self.pattern_cells:
                        start_x, start_y = x, y
                        break
                else:
                    continue
                break
        
        # Start DFS
        start_cell = self.grid[start_y][start_x]
        stack = [start_cell]
        start_cell.visited = True
        
        while stack:
            current = stack[-1]
            neighbors = self.get_unvisited_neighbors(current)
            
            if not neighbors:
                # Dead end - backtrack
                stack.pop()
            else:
                # Choose random neighbor and carve passage
                neighbor, direction = random.choice(neighbors)
                self.remove_wall_between(current, neighbor, direction)
                neighbor.visited = True
                stack.append(neighbor)
        
        return self.grid
