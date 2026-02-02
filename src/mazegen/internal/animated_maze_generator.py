"""
Animated Maze Generator
Extends the base MazeGenerator to capture animation frames during generation.
"""

import random
from typing import List, Tuple, Dict, Set
from dataclasses import dataclass


@dataclass
class AnimationFrame:
    """Represents a single frame in the maze generation animation."""
    grid_state: List[List[int]]  # Wall states for each cell
    visited_cells: Set[Tuple[int, int]]  # Cells that have been visited
    current_cell: Tuple[int, int] | None  # Currently active cell
    frontier_cells: Set[Tuple[int, int]]  # Cells in the frontier
    step_description: str  # Description of what's happening


class Cell:
    """Represents a single cell in the maze."""
    
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.walls = 15  # 0b1111 - all walls present (N=1, E=2, S=4, W=8)
        self.visited = False
    
    def has_wall(self, direction: str) -> bool:
        """Check if wall exists in given direction."""
        wall_bits = {'N': 0b0001, 'E': 0b0010, 'S': 0b0100, 'W': 0b1000}
        return bool(self.walls & wall_bits[direction])
    
    def remove_wall(self, direction: str) -> None:
        """Remove wall in given direction."""
        wall_bits = {'N': 0b0001, 'E': 0b0010, 'S': 0b0100, 'W': 0b1000}
        self.walls = self.walls & ~wall_bits[direction]


class AnimatedMazeGenerator:
    """Generate mazes using Prim's algorithm with frame-by-frame animation capture."""
    
    def __init__(self, width: int, height: int, seed: int | None = None) -> None:
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
        
        self.frames: List[AnimationFrame] = []
        self.visited_set: Set[Tuple[int, int]] = set()
        self.frontier_set: Set[Tuple[int, int]] = set()

    def get_cell(self, x: int, y: int) -> Cell | None:
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
    
    def remove_wall_between(self, cell1: Cell, cell2: Cell, direction: str) -> None:
        """Remove wall between two cells."""
        cell1.remove_wall(direction)
        
        opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        cell2.remove_wall(opposite[direction])
    
    def capture_frame(self, current_cell: Tuple[int, int] | None, description: str) -> None:
        """Capture the current state as an animation frame."""
        # Copy grid state
        grid_state = [[cell.walls for cell in row] for row in self.grid]
        
        # Create frame
        frame = AnimationFrame(
            grid_state=grid_state,
            visited_cells=self.visited_set.copy(),
            current_cell=current_cell,
            frontier_cells=self.frontier_set.copy(),
            step_description=description
        )
        self.frames.append(frame)
    
    def generate(self) -> List[List[Cell]]:
        """Generate maze using Prim's algorithm with animation capture."""
        
        # Capture initial state
        self.capture_frame(None, "Initial state - all walls intact")
        
        # Pick random start
        start_x = random.randint(0, self.width - 1)
        start_y = random.randint(0, self.height - 1)
        
        start_cell = self.grid[start_y][start_x]
        start_cell.visited = True
        self.visited_set.add((start_x, start_y))
        
        self.capture_frame((start_x, start_y), f"Starting at cell ({start_x}, {start_y})")
        
        # List that connects VISITED rooms to UNVISITED rooms
        frontier: List[Tuple[Cell, Cell, str]] = []
        
        for neighbor, direction in self.get_neighbors(start_cell):
            frontier.append((start_cell, neighbor, direction))
            self.frontier_set.add((neighbor.x, neighbor.y))
        
        self.capture_frame((start_x, start_y), f"Added {len(frontier)} walls to frontier")
        
        step_count = 0
        while frontier:
            # Pick random wall
            wall_index = random.randint(0, len(frontier) - 1)
            current_cell, neighbor_cell, direction = frontier.pop(wall_index)
            
            # Remove from frontier set
            if (neighbor_cell.x, neighbor_cell.y) in self.frontier_set:
                # Check if this cell has other frontier entries
                still_in_frontier = any(
                    (n.x, n.y) == (neighbor_cell.x, neighbor_cell.y)
                    for _, n, _ in frontier
                )
                if not still_in_frontier:
                    self.frontier_set.discard((neighbor_cell.x, neighbor_cell.y))
            
            if not neighbor_cell.visited:
                step_count += 1
                
                # Carve passage
                self.remove_wall_between(current_cell, neighbor_cell, direction)
                neighbor_cell.visited = True
                self.visited_set.add((neighbor_cell.x, neighbor_cell.y))
                
                self.capture_frame(
                    (neighbor_cell.x, neighbor_cell.y),
                    f"Step {step_count}: Carved {direction} from ({current_cell.x},{current_cell.y}) to ({neighbor_cell.x},{neighbor_cell.y})"
                )
                
                # Add new frontiers
                new_frontiers = 0
                for next_neighbor, next_dir in self.get_neighbors(neighbor_cell):
                    if not next_neighbor.visited:
                        frontier.append((neighbor_cell, next_neighbor, next_dir))
                        self.frontier_set.add((next_neighbor.x, next_neighbor.y))
                        new_frontiers += 1
                
                if new_frontiers > 0:
                    self.capture_frame(
                        (neighbor_cell.x, neighbor_cell.y),
                        f"Added {new_frontiers} new frontier walls"
                    )
        
        self.capture_frame(None, "Maze generation complete!")
        return self.grid
    
    def render_frame_ascii(self, frame_index: int) -> str:
        """Render a specific frame as ASCII art."""
        if frame_index < 0 or frame_index >= len(self.frames):
            return "Invalid frame index"
        
        frame = self.frames[frame_index]
        lines = []
        
        # Header
        lines.append("=" * (self.width * 2 + 1))
        lines.append(f"Frame {frame_index + 1}/{len(self.frames)}: {frame.step_description}")
        lines.append("=" * (self.width * 2 + 1))
        
        # Top border
        lines.append("█" * (self.width * 2 + 1))
        
        # Render each row
        for y in range(self.height):
            row_line = "█"
            
            for x in range(self.width):
                walls = frame.grid_state[y][x]
                is_current = frame.current_cell == (x, y)
                is_visited = (x, y) in frame.visited_cells
                is_frontier = (x, y) in frame.frontier_cells
                
                # Determine cell symbol
                if is_current:
                    cell_char = "@"
                elif is_frontier:
                    cell_char = "?"
                elif is_visited:
                    cell_char = "·"
                else:
                    cell_char = " "
                
                row_line += cell_char
                
                # East wall
                if walls & 0b0010:  # East wall present
                    row_line += "█"
                else:
                    row_line += " "
            
            lines.append(row_line)
            
            # South wall row
            wall_row = "█"
            for x in range(self.width):
                walls = frame.grid_state[y][x]
                
                # South wall
                if walls & 0b0100:  # South wall present
                    wall_row += "█"
                else:
                    wall_row += " "
                
                # Corner (always wall for simplicity)
                wall_row += "█"
            
            lines.append(wall_row)
        
        # Legend
        lines.append("")
        lines.append("Legend: @ = current | ? = frontier | · = visited | █ = wall")
        
        return "\n".join(lines)
    
    def get_frame_count(self) -> int:
        """Get total number of captured frames."""
        return len(self.frames)
