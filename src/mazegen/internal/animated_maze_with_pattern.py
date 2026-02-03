import random
import time
from typing import List, Tuple, Set, Dict, Any
from dataclasses import dataclass
from .maze_generator_prim import MazeGenerator as PrimGenerator
from .maze_generator_BFS import MazeGenerator as BFSGenerator

@dataclass
class AnimationFrame:
    """Represents a single frame in the maze generation animation."""
    grid_state: List[List[int]]
    current_cell: Tuple[int, int] | None = None
    visited_cells: Set[Tuple[int, int]] = None
    pattern_cells: Set[Tuple[int, int]] = None
    description: str = ""

class AnimatedPrim(PrimGenerator):
    """Subclass of original Prim's to add animation hooks."""
    def __init__(self, width, height, seed, pattern_cells, on_step_callback):
        super().__init__(width, height, seed)
        self.pattern_cells = pattern_cells
        self.on_step_callback = on_step_callback
        
        # Pre-mark pattern cells as visited so Prim's skips them
        for x, y in self.pattern_cells:
            if 0 <= y < height and 0 <= x < width:
                self.grid[y][x].visited = True

    def remove_wall_between(self, cell1, cell2, direction):
        super().remove_wall_between(cell1, cell2, direction)
        self.on_step_callback(cell2.x, cell2.y, self.grid)

    def generate(self) -> List[List[Any]]:
        """Override generate to ensure we don't start on a pattern cell."""
        # Find a non-pattern cell to start from
        non_pattern_cells = []
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in self.pattern_cells:
                    non_pattern_cells.append((x, y))
        
        if not non_pattern_cells:
            return super().generate() # Fallback if whole grid is pattern (shouldn't happen)

        start_x, start_y = random.choice(non_pattern_cells)
        start_cell = self.grid[start_y][start_x]
        start_cell.visited = True
        
        frontier: List[Tuple[Any, Any, str]] = []
        for neighbor, direction in self.get_neighbors(start_cell):
            frontier.append((start_cell, neighbor, direction))
            
        while frontier:
            wall_index = random.randint(0, len(frontier) - 1)
            current_cell, neighbor_cell, direction = frontier.pop(wall_index)
            
            if not neighbor_cell.visited:
                self.remove_wall_between(current_cell, neighbor_cell, direction)
                neighbor_cell.visited = True
                for next_neighbor, next_dir in self.get_neighbors(neighbor_cell):
                    if not next_neighbor.visited:
                        frontier.append((neighbor_cell, next_neighbor, next_dir))
                        
        return self.grid

class AnimatedBFS(BFSGenerator):
    """Subclass of original BFS/DFS to add animation hooks."""
    def __init__(self, width, height, seed, pattern_cells, on_step_callback):
        # BFSGenerator takes (height, width)
        super().__init__(height, width, seed)
        self.pattern_cells = pattern_cells
        self.on_step_callback = on_step_callback
        
        # Pre-mark pattern cells as visited so BFS skips them
        for x, y in self.pattern_cells:
            if 0 <= y < self.height and 0 <= x < self.width:
                self.grid[y][x].visited = True

    def _carve_passage(self, current, neighbor, direction):
        super()._carve_passage(current, neighbor, direction)
        self.on_step_callback(neighbor.x, neighbor.y, self.grid)

    def generate(self, start_x=0, start_y=0):
        """Override generate to prevent wiping out pattern protection."""
        # The original generate resets all visited flags, so we must re-apply them
        # However, it resets them inside its own loop. 
        # So we reimplement the logic here with protection.
        for row in self.grid:
            for cell in row:
                cell.visited = False

        # Re-apply pattern protection
        for x, y in self.pattern_cells:
            if 0 <= y < self.height and 0 <= x < self.width:
                self.grid[y][x].visited = True

        # Find a non-pattern start cell if possible
        if (start_x, start_y) in self.pattern_cells:
            non_pattern_cells = []
            for y in range(self.height):
                for x in range(self.width):
                    if (x, y) not in self.pattern_cells:
                        non_pattern_cells.append((x, y))
            if non_pattern_cells:
                start_x, start_y = random.choice(non_pattern_cells)

        start_cell = self.grid[start_y][start_x]
        stack = []
        stack.append(start_cell)
        start_cell.visited = True

        while len(stack) > 0:
            current = stack[-1]
            neighbors = self._get_unvisited_neighbors(current)
            
            if len(neighbors) == 0:
                stack.pop()
            else:
                neighbor, direction = random.choice(neighbors)
                # Double check neighbor isn't in pattern (though _get_unvisited_neighbors should handle it)
                if (neighbor.x, neighbor.y) not in self.pattern_cells:
                    self._carve_passage(current, neighbor, direction)
                    neighbor.visited = True
                    stack.append(neighbor)
                else:
                    # If somehow we picked a visited/pattern cell, just ignore it
                    # (This is just safety, _get_unvisited_neighbors already filters)
                    pass
        return self.grid

class AnimatedMazeGeneratorWithPattern:
    """Wrapper that uses the original algorithms with animation and pattern support."""
    
    def __init__(self, width: int, height: int, pattern_cells: Set[Tuple[int, int]] = None, seed: int | None = None, entry: Tuple[int, int] = (0, 0), exit_coords: Tuple[int, int] = None, perfect: bool = True) -> None:
        self.width = width
        self.height = height
        self.pattern_cells = pattern_cells or set()
        self.entry = entry
        self.exit_coords = exit_coords or (width - 1, height - 1)
        self.perfect = perfect
        self.seed = seed
        
        self.show_path = False
        self.color_scheme = "default"
        self.colors = {
            "default": {"wall": "\033[0m█", "pattern": "\033[0m▓", "path": " ", "marker": "\033[93m◦\033[0m", "start": "\033[92mS\033[0m", "end": "\033[91mE\033[0m"},
            "emerald": {"wall": "\033[32m█", "pattern": "\033[92m▓\033[32m", "path": " ", "marker": "\033[92m◦\033[32m", "start": "\033[92mS\033[32m", "end": "\033[91mE\033[32m"},
            "ocean":   {"wall": "\033[34m█", "pattern": "\033[94m▓\033[34m", "path": " ", "marker": "\033[94m◦\033[34m", "start": "\033[94mS\033[34m", "end": "\033[91mE\033[34m"},
            "amber":   {"wall": "\033[33m█", "pattern": "\033[93m▓\033[33m", "path": " ", "marker": "\033[93m◦\033[33m", "start": "\033[93mS\033[33m", "end": "\033[91mE\033[33m"},
        }
        
        self.pattern_color_scheme = "default"
        self.pattern_colors = {
            "default": "\033[0m▓",       # Default gray
            "magenta": "\033[95m▓\033[0m",  # Bright magenta
            "cyan": "\033[96m▓\033[0m",     # Bright cyan  
            "red": "\033[91m▓\033[0m",      # Bright red
            "yellow": "\033[93m▓\033[0m",   # Bright yellow
            "white": "\033[97m▓\033[0m",    # Bright white
        }
        
        self.frames: List[AnimationFrame] = []
        self.final_grid_cells = None

    def capture_frame(self, current_pos: Tuple[int, int] | None, description: str, grid_source):
        grid_state = [[cell.walls for cell in row] for row in grid_source]
        visited = set()
        for y in range(len(grid_source)):
            for x in range(len(grid_source[y])):
                if grid_source[y][x].visited:
                    visited.add((x, y))
                    
        frame = AnimationFrame(
            grid_state=grid_state,
            current_cell=current_pos,
            visited_cells=visited,
            pattern_cells=self.pattern_cells,
            description=description
        )
        self.frames.append(frame)

    def generate(self, algorithm: str = "prim") -> List[List[Any]]:
        self.frames = []
        if algorithm.lower() == "prim":
            gen = AnimatedPrim(self.width, self.height, self.seed, self.pattern_cells, 
                             lambda x, y, g: self.capture_frame((x, y), "Prim's: Carving", g))
            self.capture_frame(None, "Prim's: Initial state", gen.grid)
            self.final_grid_cells = gen.generate()
        else:
            gen = AnimatedBFS(self.width, self.height, self.seed, self.pattern_cells, 
                            lambda x, y, g: self.capture_frame((x, y), "DFS: Carving", g))
            self.capture_frame(None, "DFS: Initial state", gen.grid)
            self.final_grid_cells = gen.generate()
            
        if not self.perfect:
            self.capture_frame(None, "Creating multiple paths...", self.final_grid_cells)
            self._remove_extra_walls()
            
        self.capture_frame(None, "Complete", self.final_grid_cells)
        return self.final_grid_cells

    def _remove_extra_walls(self):
        extra_walls_to_remove = (self.width * self.height) // 20
        removed = 0
        attempts = 0
        while removed < extra_walls_to_remove and attempts < 1000:
            attempts += 1
            rx, ry = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            cell = self.final_grid_cells[ry][rx]
            dirs = [('N', 0, -1), ('E', 1, 0), ('S', 0, 1), ('W', -1, 0)]
            d, dx, dy = random.choice(dirs)
            nx, ny = rx + dx, ry + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbor = self.final_grid_cells[ny][nx]
                has_wall_method = getattr(cell, "has_wall", None)
                if has_wall_method and has_wall_method(d) and (nx, ny) not in self.pattern_cells:
                    if hasattr(cell, "remove_wall"):
                        cell.remove_wall(d)
                        opp = {'N':'S', 'S':'N', 'E':'W', 'W':'E'}
                        if hasattr(neighbor, "remove_wall"):
                            neighbor.remove_wall(opp[d])
                            removed += 1
                            if removed % 5 == 0:
                                self.capture_frame(None, f"Removed extra wall at ({rx},{ry})", self.final_grid_cells)

    def get_frame_count(self) -> int:
        return len(self.frames)

    def render_frame_simple(self, index: int) -> str:
        """Render a frame using a grid-style display to show walls."""
        if not self.frames: return ""
        frame = self.frames[index]
        c = self.colors[self.color_scheme]
        WC, PC, MK, ST, EN = c["wall"], c["path"], c["marker"], c["start"], c["end"]
        # Use separate pattern color
        PT = self.pattern_colors.get(self.pattern_color_scheme, self.pattern_colors["default"])
        
        path_cells = set()
        if self.show_path and index == len(self.frames) - 1:
            from .path_finder import find_path
            path_str = find_path(frame.grid_state, self.entry, self.exit_coords)
            curr_x, curr_y = self.entry
            path_cells.add((curr_x, curr_y))
            dirs = {'N': (0, -1), 'E': (1,0), 'S': (0,1), 'W': (-1,0)}
            for move in path_str:
                dx, dy = dirs.get(move, (0,0))
                curr_x += dx
                curr_y += dy
                path_cells.add((curr_x, curr_y))

        output = []
        output.append(f"Step: {index+1}/{len(self.frames)} - {frame.description}")
        
        # Grid dimensions: (width * 2 + 1) x (height * 2 + 1)
        grid_display = [[" " for _ in range(self.width * 2 + 1)] for _ in range(self.height * 2 + 1)]
        
        # Draw cells and walls
        for y in range(self.height):
            for x in range(self.width):
                gy, gx = y * 2 + 1, x * 2 + 1
                
                # Cell character
                if (x, y) == self.entry: char = ST
                elif (x, y) == self.exit_coords: char = EN
                elif (x, y) in frame.pattern_cells: char = PT
                elif (x, y) in path_cells: char = MK
                elif (x, y) in frame.visited_cells: char = PC
                else: char = WC
                grid_display[gy][gx] = char
                
                # Walls
                walls = frame.grid_state[y][x]
                if walls & 1: grid_display[gy-1][gx] = WC # North
                if walls & 2: grid_display[gy][gx+1] = WC # East
                if walls & 4: grid_display[gy+1][gx] = WC # South
                if walls & 8: grid_display[gy][gx-1] = WC # West
                
                # Corners (filled if surrounded by walls)
                grid_display[gy-1][gx-1] = WC
                grid_display[gy-1][gx+1] = WC
                grid_display[gy+1][gx-1] = WC
                grid_display[gy+1][gx+1] = WC

        return "\n".join(["".join(row) for row in grid_display]) + "\033[0m"

    def play_animation(self, fps: float = 15.0):
        delay = 1.0 / fps
        for i in range(len(self.frames)):
            print("\033[2J\033[H", end="")
            print(self.render_frame_simple(i))
            time.sleep(delay)
        time.sleep(1)

    def write_to_hex_file(self, filename: str, entry: Tuple[int, int], exit_coords: Tuple[int, int]):
        from .path_finder import find_path
        grid_state = [[cell.walls for cell in row] for row in self.final_grid_cells]
        path_str = find_path(grid_state, entry, exit_coords)
        path_out = "".join(list(path_str))
        with open(filename, 'w') as f:
            for y in range(self.height):
                row_hex = "".join([format(self.final_grid_cells[y][x].walls, 'X') for x in range(self.width)])
                f.write(row_hex + "\n")
            f.write(f"\n{entry[0]},{entry[1]}\n{exit_coords[0]},{exit_coords[1]}\n{path_out}\n")
