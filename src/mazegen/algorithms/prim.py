import random
from typing import List, Tuple, Optional, Callable


class Cell:
    """Represents a single cell in the maze."""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.walls = 15
        self.visited = False
        self.enabled = True

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

    def __init__(self, width: int, height: int,
                 seed: Optional[int] = None) -> None:
        self.width = width
        self.height = height

        if seed is not None:
            random.seed(seed)

        self.grid: List[List[Cell]] = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(Cell(x, y))
            self.grid.append(row)

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """Get cell at coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def get_neighbors(self, cell: Cell) -> List[Tuple[Cell, str]]:
        """Get all neighbors with their directions."""
        neighbors = []

        if cell.y > 0:
            neighbors.append((self.grid[cell.y - 1][cell.x], 'N'))

        if cell.x < self.width - 1:
            neighbors.append((self.grid[cell.y][cell.x + 1], 'E'))

        if cell.y < self.height - 1:
            neighbors.append((self.grid[cell.y + 1][cell.x], 'S'))

        if cell.x > 0:
            neighbors.append((self.grid[cell.y][cell.x - 1], 'W'))

        return neighbors

    def _get_unvisited_neighbors(self, cell: Cell) -> List[Tuple[Cell, str]]:
        """
        Get unvisited neighbors (for animation compatibility).
        Checks for bounds, 'enabled' status, and visited status.
        """
        neighbors = []
        directions = {
            'N': (0, -1),
            'E': (1, 0),
            'S': (0, 1),
            'W': (-1, 0)
        }

        for direction, (dx, dy) in directions.items():
            nx, ny = cell.x + dx, cell.y + dy
            neighbor = self.get_cell(nx, ny)
            if neighbor and getattr(neighbor, 'enabled',
                                    True) and not neighbor.visited:
                neighbors.append((neighbor, direction))
        return neighbors

    def _carve_passage(self, cell1: Cell, cell2: Cell, direction: str) -> None:
        """Alias for remove_wall_between for animation compatibility."""
        self.remove_wall_between(cell1, cell2, direction)

    def remove_wall_between(
        self, cell1: Cell, cell2: Cell, direction: str
    ) -> None:
        """Remove wall between two cells."""
        cell1.remove_wall(direction)

        opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        cell2.remove_wall(opposite[direction])

    def generate(self, start_x: Optional[int] = None,
                 start_y: Optional[int] = None,
                 callback: Optional[Callable[[Cell], None]] = None) -> (
                     List[List[Cell]]
                 ):
        """The core Part is here :Generate maze using Prim's algorithm."""

        if start_x is None:
            sx = random.randint(0, self.width - 1)
        else:
            sx = start_x

        if start_y is None:
            sy = random.randint(0, self.height - 1)
        else:
            sy = start_y

        start_cell = self.grid[sy][sx]
        start_cell.visited = True

        frontier: List[Tuple[Cell, Cell, str]] = []

        for neighbor, direction in self.get_neighbors(start_cell):
            frontier.append((start_cell, neighbor, direction))

        if callback:
            callback(start_cell)

        while frontier:
            wall_index = random.randint(0, len(frontier) - 1)
            current_cell, neighbor_cell, direction = frontier.pop(wall_index)

            if not neighbor_cell.visited:
                self.remove_wall_between(
                    current_cell, neighbor_cell, direction)
                neighbor_cell.visited = True

                if callback:
                    callback(neighbor_cell)

            for next_neighbor, next_dir in self.get_neighbors(neighbor_cell):
                if not next_neighbor.visited:
                    frontier.append((neighbor_cell, next_neighbor, next_dir))

        return self.grid
