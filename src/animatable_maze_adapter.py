"""
Adapter to connect unified maze generators with frame-based animators.
This allows using FrameRenderer with the new PrimMazeGenerator and DFSMazeGenerator.
"""

import sys
import os

# Import generators directly without going through __init__.py
src_path = os.path.dirname(__file__)
mazegen_path = os.path.join(src_path, 'mazegen')
if mazegen_path not in sys.path:
    sys.path.insert(0, mazegen_path)

from internal.maze_generator_prim import PrimMazeGenerator
from internal.maze_generator_dfs import DFSMazeGenerator


class AnimatableMazeGenerator:
    """
    Adapter class that makes unified generators compatible with FrameRenderer.
    Adds the `enabled` attribute that FrameRenderer expects for pattern cells.
    """
    
    def __init__(self, algorithm='prim', width=20, height=15, seed=None, pattern_cells=None):
        """
        Initialize the animatable maze generator.
        
        Args:
            algorithm: 'prim' or 'dfs'
            width: Maze width in cells
            height: Maze height in cells
            seed: Random seed
            pattern_cells: Set of (x, y) tuples for pattern cells
        """
        self.width = width
        self.height = height
        self.seed = seed
        self.pattern_cells = pattern_cells or set()
        self.algorithm = algorithm
        
        # Create the underlying generator
        if algorithm == 'prim':
            self.generator = PrimMazeGenerator(width, height, seed, self.pattern_cells)
        else:  # dfs
            self.generator = DFSMazeGenerator(width, height, seed, self.pattern_cells)
        
        # Get reference to the grid
        self.grid = self.generator.grid
        
        # Add 'enabled' attribute to all cells for FrameRenderer compatibility
        # Pattern cells have enabled=False, others have enabled=True
        for y in range(height):
            for x in range(width):
                cell = self.grid[y][x]
                if not hasattr(cell, 'enabled'):
                    cell.enabled = (x, y) not in self.pattern_cells
    
    def _get_unvisited_neighbors(self, cell):
        """
        Get unvisited neighbors - required by animator.
        
        Args:
            cell: Current cell
            
        Returns:
            List of (neighbor, direction) tuples
        """
        return [(n, d) for n, d in self.generator.get_neighbors(cell) if not n.visited]
    
    def _carve_passage(self, current, neighbor, direction):
        """
        Carve passage between cells - required by animator.
        
        Args:
            current: Current cell
            neighbor: Neighbor cell
            direction: Direction from current to neighbor
        """
        self.generator.remove_wall_between(current, neighbor, direction)
    
    def generate_without_animation(self):
        """
        Generate the maze without animation (for final output).
        
        Returns:
            The generated grid
        """
        return self.generator.generate()
