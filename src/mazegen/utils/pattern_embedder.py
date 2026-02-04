"""
Pattern embedding for maze generation.
Allows embedding custom patterns (like "42") into the maze structure.
"""

from typing import List, Set, Tuple


# "42" pattern definition - represents the shape as OPEN PATHS
# Looking at the reference image, "42" appears as light paths in the center
# 1 = part of "42" (keep as open path), 0 = normal maze cell
# Compact "42" pattern (7x5) - fits even in 10x10 mazes
# 1 = Unbreakable wall, 0 = Normal maze cell
PATTERN_42 = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]


def get_pattern_cells(width: int, height: int, pattern: List[List[int]] = PATTERN_42, entry: Tuple[int, int] = None, exit_coords: Tuple[int, int] = None) -> Set[Tuple[int, int]]:
    """
    Get the set of cells that should form the unbreakable wall pattern.
    Ensures that entry and exit points are NOT walls.
    """
    pattern_height = len(pattern)
    pattern_width = len(pattern[0]) if pattern else 0
    
    if pattern_width == 0 or pattern_height == 0:
        return set()

    # Check if pattern fits in maze
    if pattern_width > width or pattern_height > height:
        return set()
    
    center_x, center_y = width // 2, height // 2
    offset_x, offset_y = center_x - pattern_width // 2, center_y - pattern_height // 2
    
    wall_cells = set()
    protected = {entry, exit_coords}
    
    for py in range(pattern_height):
        for px in range(pattern_width):
            maze_x, maze_y = offset_x + px, offset_y + py
            if 0 <= maze_x < width and 0 <= maze_y < height:
                if pattern[py][px] == 1 and (maze_x, maze_y) not in protected:
                    wall_cells.add((maze_x, maze_y))
    
    return wall_cells


def is_pattern_cell(x: int, y: int, pattern_cells: Set[Tuple[int, int]]) -> bool:
    """
    Check if a cell is part of the pattern.
    
    Args:
        x: Cell x coordinate
        y: Cell y coordinate
        pattern_cells: Set of pattern cell coordinates
        
    Returns:
        True if cell is part of pattern
    """
    return (x, y) in pattern_cells

