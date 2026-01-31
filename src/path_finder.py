from typing import List, Tuple
from collections import deque
from src.maze_generator_prim import Cell


def find_path(grid: List[List[Cell]], entry: Tuple[int, int], exit: Tuple[int, int]) -> str:
    """
    Find the shortest path using the bfs algorithm
    and return the path as string
    """
    width = len(grid[0])
    height = len(grid)
    
    queue = deque([(entry[0], entry[1], "")])
    visited = {entry} # using set to avoid duplucating cells

    # Direction mappings
    directions = {
        'N': (0, -1),
        'E': (1, 0),
        'S': (0, 1),
        'W': (-1, 0)
    }
    
    
    while queue:
        x,y, path = queue.popleft()
        
        if (x , y) == exit :
            return path
        
        cell = grid[y][x]
        
        for dir_char , (dx, dy) in directions.items():
            # check if wall is open
            if not cell.has_wall(dir_char):
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + dir_char))
    return ""
