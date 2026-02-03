"""
Prim's maze generation algorithm.
Uses a frontier-based approach to create perfect mazes.
"""

import random
from typing import List, Set, Tuple
from .maze_base import MazeGeneratorBase, Cell


class PrimMazeGenerator(MazeGeneratorBase):
    """Generate mazes using Prim's algorithm (frontier-based)."""
    
    def generate(self) -> List[List[Cell]]:
        """
        Generate maze using Prim's algorithm.
        
        The algorithm:
        1. Start with a random cell, mark it visited
        2. Add all its walls to a frontier list
        3. While frontier is not empty:
           - Pick a random wall from frontier
           - If the wall connects visited to unvisited cell:
             - Remove the wall
             - Mark the unvisited cell as visited  
             - Add its walls to the frontier
        
        Returns:
            The generated maze grid
        """
        # Find a valid start cell (not in pattern)
        non_pattern_cells = [(x, y) for y in range(self.height) 
                            for x in range(self.width) 
                            if (x, y) not in self.pattern_cells]
        
        if not non_pattern_cells:
            return self.grid
        
        start_x, start_y = random.choice(non_pattern_cells)
        start_cell = self.grid[start_y][start_x]
        start_cell.visited = True
        
        # Frontier: list of (current_cell, neighbor_cell, direction) tuples
        frontier: List[Tuple[Cell, Cell, str]] = []
        
        for neighbor, direction in self.get_neighbors(start_cell):
            if not neighbor.visited:
                frontier.append((start_cell, neighbor, direction))
        
        while frontier:
            # Pick random wall from frontier
            wall_index = random.randint(0, len(frontier) - 1)
            current_cell, neighbor_cell, direction = frontier.pop(wall_index)
            
            # If neighbor hasn't been visited, carve passage
            if not neighbor_cell.visited:
                self.remove_wall_between(current_cell, neighbor_cell, direction)
                neighbor_cell.visited = True
        
                # Add new walls to frontier
                for next_neighbor, next_dir in self.get_neighbors(neighbor_cell):
                    if not next_neighbor.visited:
                        frontier.append((neighbor_cell, next_neighbor, next_dir))
            
        return self.grid
