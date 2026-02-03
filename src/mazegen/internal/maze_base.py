"""
Base classes for maze generation.
Provides common Cell class and base functionality for all maze generators.
"""

import random
from typing import List, Tuple, Set


class Cell:
    """Represents a single cell in the maze."""
    
    def __init__(self, x: int, y: int) -> None:
        """
        Initialize a cell at given coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.x = x
        self.y = y
        self.walls = 15  # 0b1111 - all walls present (N=1, E=2, S=4, W=8)
        self.visited = False
    
    def has_wall(self, direction: str) -> bool:
        """
        Check if wall exists in given direction.
        
        Args:
            direction: Direction to check ('N', 'E', 'S', 'W')
            
        Returns:
            True if wall exists, False otherwise
        """
        wall_bits = {'N': 0b0001, 'E': 0b0010, 'S': 0b0100, 'W': 0b1000}
        return bool(self.walls & wall_bits[direction])
    
    def remove_wall(self, direction: str) -> None:
        """
        Remove wall in given direction.
        
        Args:
            direction: Direction to remove wall ('N', 'E', 'S', 'W')
        """
        wall_bits = {'N': 0b0001, 'E': 0b0010, 'S': 0b0100, 'W': 0b1000}
        self.walls = self.walls & ~wall_bits[direction]


class MazeGeneratorBase:
    """Base class for all maze generation algorithms."""
    
    def __init__(self, width: int, height: int, seed: int | None = None, 
                 pattern_cells: Set[Tuple[int, int]] = None) -> None:
        """
        Initialize the maze generator.
        
        Args:
            width: Width of maze in cells
            height: Height of maze in cells  
            seed: Random seed for reproducibility
            pattern_cells: Set of (x, y) coordinates to protect from generation
        """
        self.width = width
        self.height = height
        self.pattern_cells = pattern_cells or set()
        
        if seed is not None:
            random.seed(seed)
            
        # Create grid of cells
        self.grid: List[List[Cell]] = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(Cell(x, y))
            self.grid.append(row)
        
        # Mark pattern cells as visited to protect them
        for x, y in self.pattern_cells:
            if 0 <= y < height and 0 <= x < width:
                self.grid[y][x].visited = True

    def get_cell(self, x: int, y: int) -> Cell | None:
        """
        Get cell at coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Cell at coordinates or None if out of bounds
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
    
    def get_neighbors(self, cell: Cell) -> List[Tuple[Cell, str]]:
        """
        Get all adjacent neighbors with their directions.
        
        Args:
            cell: Cell to get neighbors for
            
        Returns:
            List of (neighbor_cell, direction) tuples
        """
        neighbors = []
        
        # North
        if cell.y > 0:
            neighbors.append((self.grid[cell.y - 1][cell.x], 'N'))
        
        # East
        if cell.x < self.width - 1:
            neighbors.append((self.grid[cell.y][cell.x + 1], 'E'))
        
        # South
        if cell.y < self.height - 1:
            neighbors.append((self.grid[cell.y + 1][cell.x], 'S'))
        
        # West
        if cell.x > 0:
            neighbors.append((self.grid[cell.y][cell.x - 1], 'W'))
        
        return neighbors
    
    def get_unvisited_neighbors(self, cell: Cell) -> List[Tuple[Cell, str]]:
        """
        Get all unvisited adjacent neighbors.
        
        Args:
            cell: Cell to get neighbors for
            
        Returns:
            List of (neighbor_cell, direction) tuples for unvisited neighbors
        """
        return [(neighbor, direction) 
                for neighbor, direction in self.get_neighbors(cell) 
                if not neighbor.visited]
    
    def remove_wall_between(self, cell1: Cell, cell2: Cell, direction: str) -> None:
        """
        Remove wall between two adjacent cells.
        
        Args:
            cell1: First cell
            cell2: Second cell (adjacent to cell1)
            direction: Direction from cell1 to cell2
        """
        # Remove wall from first cell
        cell1.remove_wall(direction)
        
        # Remove opposite wall from second cell
        opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        cell2.remove_wall(opposite[direction])
    
    def generate(self) -> List[List[Cell]]:
        """
        Generate the maze. Must be implemented by subclasses.
        
        Returns:
            The generated maze grid
        """
        raise NotImplementedError("Subclasses must implement generate()")
