"""
Maze generator with animation frames, pattern support, and rendering.
This class coordinates maze generation algorithms with visualization.
"""

import random
import time
from typing import List, Tuple, Set, Any
from dataclasses import dataclass
from .maze_generator_prim import PrimMazeGenerator
from .maze_generator_dfs import DFSMazeGenerator
from .path_finder import find_path


@dataclass
class AnimationFrame:
    """Represents a single frame in the maze generation animation."""
    grid_state: List[List[int]]  # Wall state for each cell
    visited_cells: Set[Tuple[int, int]]  # Cells that have been visited
    pattern_cells: Set[Tuple[int, int]]  # Pattern cells (e.g., "42")
    current_cell: Tuple[int, int] | None = None  # Currently active cell
    description: str = ""  # Description of this frame


class MazeGeneratorWithAnimation:
    """
    High-level maze generator that coordinates algorithms, animation, and rendering.
    Supports pattern embedding and visualization features.
    """
    
    def __init__(self, width: int, height: int, pattern_cells: Set[Tuple[int, int]] = None,
                 seed: int | None = None, entry: Tuple[int, int] = (0, 0),
                 exit_coords: Tuple[int, int] = None, perfect: bool = True) -> None:
        """
        Initialize the maze generator.
        
        Args:
            width: Width of maze in cells
            height: Height of maze in cells
            pattern_cells: Set of (x, y) coordinates for pattern (e.g., "42")
            seed: Random seed for reproducibility
            entry: Entry point coordinates
            exit_coords: Exit point coordinates
            perfect: If True, generates a perfect maze (single path)
        """
        self.width = width
        self.height = height
        self.pattern_cells = pattern_cells or set()
        self.entry = entry
        self.exit_coords = exit_coords or (width - 1, height - 1)
        self.perfect = perfect
        self.seed = seed
        
        # Display settings
        self.show_path = False
        self.color_scheme = "default"
        self.colors = {
            "default": {"wall": "\033[0m█", "path": " ", "marker": "\033[93m◦\033[0m", 
                       "start": "\033[92mS\033[0m", "end": "\033[91mE\033[0m"},
            "emerald": {"wall": "\033[32m█", "path": " ", "marker": "\033[92m◦\033[32m", 
                       "start": "\033[92mS\033[32m", "end": "\033[91mE\033[32m"},
            "ocean":   {"wall": "\033[34m█", "path": " ", "marker": "\033[94m◦\033[34m", 
                       "start": "\033[94mS\033[34m", "end": "\033[91mE\033[34m"},
            "amber":   {"wall": "\033[33m█", "path": " ", "marker": "\033[93m◦\033[33m", 
                       "start": "\033[93mS\033[33m", "end": "\033[91mE\033[33m"},
        }
        
        self.pattern_color_scheme = "default"
        self.pattern_colors = {
            "default": "\033[0m▓",
            "magenta": "\033[95m▓\033[0m",
            "cyan": "\033[96m▓\033[0m",
            "red": "\033[91m▓\033[0m",
            "yellow": "\033[93m▓\033[0m",
            "white": "\033[97m▓\033[0m",
        }
        
        self.frames: List[AnimationFrame] = []
        self.final_grid = None
    
    def _capture_frame(self, generator: Any, description: str, current_pos: Tuple[int, int] | None = None) -> None:
        """
        Capture current state as an animation frame.
        
        Args:
            generator: The maze generator instance
            description: Description of this frame
            current_pos: Current cell being processed
        """
        grid_state = [[cell.walls for cell in row] for row in generator.grid]
        visited = {(cell.x, cell.y) for row in generator.grid 
                  for cell in row if cell.visited}
        
        frame = AnimationFrame(
            grid_state=grid_state,
            visited_cells=visited,
            pattern_cells=self.pattern_cells,
            current_cell=current_pos,
            description=description
        )
        self.frames.append(frame)
    
    def generate(self, algorithm: str = "prim") -> List[List[Any]]:
        """
        Generate maze using specified algorithm.
        
        Args:
            algorithm: "prim" or "dfs"
            
        Returns:
            The generated maze grid
        """
        self.frames = []
        
        # Create generator with pattern cells
        if algorithm.lower() == "prim":
            generator = PrimMazeGenerator(self.width, self.height, self.seed, self.pattern_cells)
            self._capture_frame(generator, "Prim's: Initial state")
        else:  # dfs
            generator = DFSMazeGenerator(self.width, self.height, self.seed, self.pattern_cells)
            self._capture_frame(generator, "DFS: Initial state")
        
        # Generate maze
        self.final_grid = generator.generate()
        self._capture_frame(generator, f"{algorithm.upper()}: Generation complete")
        
        # Remove extra walls if not perfect
        if not self.perfect:
            self._capture_frame(generator, "Creating multiple paths...")
            self._remove_extra_walls(generator)
        
        self._capture_frame(generator, "Complete")
        return self.final_grid
    
    def _remove_extra_walls(self, generator: Any) -> None:
        """Remove some walls to create multiple paths."""
        extra_walls_to_remove = (self.width * self.height) // 20
        removed = 0
        attempts = 0
        
        while removed < extra_walls_to_remove and attempts < 1000:
            attempts += 1
            rx, ry = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            
            if (rx, ry) in self.pattern_cells:
                continue
                
            cell = generator.grid[ry][rx]
            dirs = [('N', 0, -1), ('E', 1, 0), ('S', 0, 1), ('W', -1, 0)]
            d, dx, dy = random.choice(dirs)
            nx, ny = rx + dx, ry + dy
            
            if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in self.pattern_cells:
                neighbor = generator.grid[ny][nx]
                if cell.has_wall(d):
                    generator.remove_wall_between(cell, neighbor, d)
                    removed += 1
                    
                    if removed % 5 == 0:
                        self._capture_frame(generator, f"Removed {removed} extra walls")
    
    def get_frame_count(self) -> int:
        """Get total number of captured frames."""
        return len(self.frames)
    
    def render_frame_simple(self, index: int) -> str:
        """
        Render a frame as a simple ASCII grid.
        
        Args:
            index: Frame index to render
            
        Returns:
            String representation of the frame
        """
        if not self.frames:
            return ""
            
        frame = self.frames[index]
        c = self.colors[self.color_scheme]
        WC, PC, MK, ST, EN = c["wall"], c["path"], c["marker"], c["start"], c["end"]
        PT = self.pattern_colors.get(self.pattern_color_scheme, self.pattern_colors["default"])
        
        # Calculate path if needed
        path_cells = set()
        if self.show_path and index == len(self.frames) - 1:
            path_str = find_path(frame.grid_state, self.entry, self.exit_coords)
            curr_x, curr_y = self.entry
            path_cells.add((curr_x, curr_y))
            dirs = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
            for move in path_str:
                dx, dy = dirs.get(move, (0, 0))
                curr_x += dx
                curr_y += dy
                path_cells.add((curr_x, curr_y))
        
        # Build output
        output = [f"Step: {index+1}/{len(self.frames)} - {frame.description}"]
        
        # Create grid display (width * 2 + 1) x (height * 2 + 1)
        grid_display = [[" " for _ in range(self.width * 2 + 1)] 
                       for _ in range(self.height * 2 + 1)]
        
        # Draw cells and walls
        for y in range(self.height):
            for x in range(self.width):
                gy, gx = y * 2 + 1, x * 2 + 1
                
                # Determine cell character
                if (x, y) == self.entry:
                    char = ST
                elif (x, y) == self.exit_coords:
                    char = EN
                elif (x, y) in frame.pattern_cells:
                    char = PT
                elif (x, y) in path_cells:
                    char = MK
                elif (x, y) in frame.visited_cells:
                    char = PC
                else:
                    char = WC
                
                grid_display[gy][gx] = char
                
                # Draw walls
                walls = frame.grid_state[y][x]
                if walls & 1:  # North
                    grid_display[gy-1][gx] = WC
                if walls & 2:  # East
                    grid_display[gy][gx+1] = WC
                if walls & 4:  # South
                    grid_display[gy+1][gx] = WC
                if walls & 8:  # West
                    grid_display[gy][gx-1] = WC
                
                # Corners
                grid_display[gy-1][gx-1] = WC
                grid_display[gy-1][gx+1] = WC
                grid_display[gy+1][gx-1] = WC
                grid_display[gy+1][gx+1] = WC
        
        return "\n".join(["".join(row) for row in grid_display]) + "\033[0m"
    
    def play_animation(self, fps: float = 15.0) -> None:
        """
        Play the captured animation frames.
        
        Args:
            fps: Frames per second
        """
        delay = 1.0 / fps
        for i in range(len(self.frames)):
            print("\033[2J\033[H", end="")  # Clear screen and move to top
            print(self.render_frame_simple(i))
            time.sleep(delay)
        time.sleep(1)
    
    def write_to_hex_file(self, filename: str, entry: Tuple[int, int], exit_coords: Tuple[int, int]) -> None:
        """
        Write maze to file in hexadecimal format with solution.
        
        Args:
            filename: Output filename
            entry: Entry coordinates
            exit_coords: Exit coordinates
        """
        if not self.final_grid:
            return
            
        grid_state = [[cell.walls for cell in row] for row in self.final_grid]
        path_str = find_path(grid_state, entry, exit_coords)
        path_out = "".join(list(path_str))
        
        with open(filename, 'w') as f:
            for y in range(self.height):
                row_hex = "".join([format(self.final_grid[y][x].walls, 'X') 
                                  for x in range(self.width)])
                f.write(row_hex + "\n")
            f.write(f"\n{entry[0]},{entry[1]}\n{exit_coords[0]},{exit_coords[1]}\n{path_out}\n")
