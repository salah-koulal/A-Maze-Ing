import random
from typing import List, Tuple, Optional, Any, Callable


class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.walls = 15
        self.visited = False
        self.enabled = True

    def has_wall(self, point: str) -> bool:
        wall = {'N': 0b0001, 'E': 0b0010, 'S': 0b0100, 'W': 0b1000}
        return bool(self.walls & wall[point])

    def remove_wall(self, point: str) -> None:
        wall = {'N': 0b0001, 'E': 0b0010, 'S': 0b0100, 'W': 0b1000}
        self.walls = self.walls & ~wall[point]


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: Any = 42) -> None:
        self.height = height
        self.width = width
        self.seed = seed
        random.seed(seed)

        self.grid: List[List[Cell]] = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(Cell(x, y))
            self.grid.append(row)

    def _get_cell(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def _get_unvisited_neighbors(self, cell: Cell) -> List[Tuple[Cell, str]]:
        neighbors = []
        directions = {
            'N': (0, -1),
            'E': (1, 0),
            'S': (0, 1),
            'W': (-1, 0)
        }
        for direction in directions:
            dx, dy = directions[direction]
            nx = cell.x + dx
            ny = cell.y + dy
            neighbor = self._get_cell(nx, ny)
            if neighbor and neighbor.enabled and not neighbor.visited:
                neighbors.append((neighbor, direction))
        return neighbors

    def _carve_passage(self, current: Cell, neighbor: Cell,
                       direction: str) -> None:
        current.remove_wall(direction)

        opposits = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        neighbor.remove_wall(opposits[direction])

    def remove_wall_between(
        self, cell1: Cell, cell2: Cell, direction: str
    ) -> None:
        """Alias for _carve_passage to match interface."""
        self._carve_passage(cell1, cell2, direction)

    def generate(self, start_x: int = 0, start_y: int = 0,
                 callback: Optional[Callable[[Cell], None]] = None) -> (
                     List[List[Cell]]
                 ):
        for row in self.grid:
            for cell in row:
                if cell.walls != 15:
                    cell.visited = False

        start_cell = self.grid[start_y][start_x]
        stack = []
        stack.append(start_cell)
        start_cell.visited = True

        if callback:
            callback(start_cell)

        while len(stack) > 0:
            current_cell = stack[-1]
            neighbors = self._get_unvisited_neighbors(current_cell)

            if len(neighbors) == 0:
                stack.pop()
            else:
                neighbor, direction = random.choice(neighbors)
                self._carve_passage(current_cell, neighbor, direction)
                neighbor.visited = True
                if callback:
                    callback(neighbor)
                stack.append(neighbor)
        return self.grid
