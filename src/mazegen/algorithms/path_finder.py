from typing import List, Tuple, Any
from collections import deque

def find_path(grid: List[List[Any]], entry: Tuple[int, int], exit: Tuple[int, int]) -> str:
    """
    Find the shortest path using the bfs algorithm
    and return the path as string (N, E, S, W)
    """
    width = len(grid[0])
    height = len(grid)
    
    queue = deque([(entry[0], entry[1], "")])
    visited = {entry}

    directions = {
        'N': (0, -1),
        'E': (1, 0),
        'S': (0, 1),
        'W': (-1, 0)
    }
    
    while queue:
        x, y, path = queue.popleft()
        
        if (x, y) == exit:
            return path
        
        cell = grid[y][x]
        
        for dir_char, (dx, dy) in directions.items():
            # Check if wall is open - handles both Cell objects and raw bitmasks
            wall_bits = {'N': 0b0001, 'E': 0b0010, 'S': 0b0100, 'W': 0b1000}
            
            # If it's a Cell object, call has_wall, otherwise use bitwise logic
            if hasattr(cell, 'has_wall'):
                has_wall = cell.has_wall(dir_char)
            else:
                has_wall = bool(cell & wall_bits[dir_char])
                
            if not has_wall:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + dir_char))
    return ""