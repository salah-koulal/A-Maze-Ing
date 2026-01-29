import random
from typing import List, Tuple



class Cell:
    """Represents a single cell in the maze."""
    
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.walls = 15
        self.visited = False
    
    def has_wall(self, direction: str) -> bool:
        """Check if wall exists in given direction."""
        wall_bits = {'N': 0b0001, 'E': 0b0010, 'S': 0b0100, 'W': 0b1000}
        return bool(self.walls & wall_bits[direction])
    
    def remove_wall(self, direction: str) -> None:
        """Remove wall in given direction."""
        wall_bits = {'N': 0b0001, 'E': 0b0010, 'S': 0b0100, 'W': 0b1000}
        self.walls = self.walls & ~wall_bits[direction]
    
    
class MazeGenerator:
    """Generate mazes using Prim's algorithm."""
    def __init__(self, width: int, height: int, seed: int | None = None) -> None:
        self.width = width
        self.height = height
        
        if seed is not None:
            random.seed(seed)
            
        # Create grid using your Cell class
        self.grid: List[List[Cell]] = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(Cell(x,y))
            self.grid.append(row)

    def get_cell(self, x: int, y: int) -> Cell | None:
        """Get cell at coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
    
    def get_neighbors(self, cell: Cell) -> List[Tuple[Cell, str]]:
        """Get all neighbors with their directions."""
        neighbors = []
        
        if cell.y > 0:
            neighbors.append( (self.grid[cell.y - 1][cell.x], 'N') )
        
        if cell.x > 0:
            neighbors.append( (self.grid[cell.y][cell.x + 1] , 'E') )
        
        if cell.y > 0:
            neighbors.append( (self.grid[cell.y + 1][cell.x] , 'S') )

        if cell.x > 0:
            neighbors.append( (self.grid[cell.y][cell.x - 1], 'W') )

        return neighbors


cell = Cell(0, 0)
print(cell.walls)

cell.remove_wall('N')
print(cell.walls)

cell.remove_wall('E')
print(cell.walls)

print(cell.has_wall('W'))
print(cell.has_wall('E'))