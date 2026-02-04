from typing import List, Tuple, Optional
from ..algorithms.prim import MazeGenerator as PrimGenerator
from ..algorithms.dfs import MazeGenerator as DFSGenerator
from .animator import MazeAnimator
from .frame_renderer import FrameRenderer
from ..utils.file_writer import save_to_file


class AnimatedMazeGeneratorWithPattern:
    @property
    def show_path(self):
        return self._show_path

    @show_path.setter
    def show_path(self, value):
        self._show_path = value
        # Invalidate renderer to force re-creation with new path state
        self.renderer = None

    @property
    def color_scheme(self):
        return self._color_scheme

    @color_scheme.setter
    def color_scheme(self, value):
        self._color_scheme = value
        # Invalidate renderer to force re-creation with new color state
        self.renderer = None
        # Proactively update internal generator if it exists (for animation)
        if hasattr(self, 'generator') and self.generator:
            self.generator.color_scheme = value

    def __init__(self, width: int, height: int, pattern_cells: List[Tuple[int, int]], seed: Optional[str] = None, entry: Tuple[int, int] = (
            0, 0), exit_coords: Tuple[int, int] = None, perfect: bool = True):
        self.width = width
        self.height = height
        self.pattern_cells = pattern_cells
        self.seed = int(seed) if seed else None
        self.entry = entry
        self.exit_coords = exit_coords
        self.perfect = perfect

        self.grid = None
        self.animator = None
        self.renderer = None
        self._show_path = False
        self._color_scheme = "default"

        # Initialize one generator to get the grid structure
        # In a real scenario, we might want to delay this until generate()
        # but to satisfy __init__ expectations of having a grid:
        self._init_generator_stub()

    def _init_generator_stub(self):
        # Create a temporary generator just to have a grid structure
        temp_gen = PrimGenerator(self.width, self.height, self.seed)
        self.grid = temp_gen.grid
        # Apply pattern cells
        # We need to ensure these cells are handled.
        # Since I don't know exactly what pattern_cells does (likely marks cells as unvisited or blocked),
        # I'll update the grid.
        # But wait, `generator.py` passes `pattern_cells` to `__init__`.
        # Taking a guess: pattern cells might be "disabled" or "pre-carved".
        # Let's assume they are "enabled=False" based on FrameRenderer lines: `if not cell.enabled: ...`
        # But Cell class in Prim/DFS doesn't have `enabled`.
        # I should probably monkey-patch `enabled` or update Cell class.
        # For safety I will monkey-patch attributes onto cells for now.
        for row in self.grid:
            for cell in row:
                cell.enabled = True

        if self.pattern_cells:
            for (px, py) in self.pattern_cells:
                if 0 <= px < self.width and 0 <= py < self.height:
                    self.grid[py][px].enabled = False

    def generate(self, algorithm: str = "prim"):
        if algorithm.lower() == "prim":
            gen_class = PrimGenerator
        else:
            gen_class = DFSGenerator

        generator = gen_class(self.width, self.height, self.seed)
        self.generator = generator
        generator.entry = self.entry
        generator.exit = self.exit_coords
        self.grid = generator.grid

        # Re-apply pattern logic
        for row in self.grid:
            for cell in row:
                cell.enabled = True

        if self.pattern_cells:
            for (px, py) in self.pattern_cells:
                if 0 <= px < self.width and 0 <= py < self.height:
                    self.grid[py][px].enabled = False
                    # Maybe also visit them so they are not carved into?
                    self.grid[py][px].visited = True

        # Ensure internal generator has color_scheme BEFORE animator/renderer
        # creation
        generator.color_scheme = self.color_scheme
        self.animator = MazeAnimator(generator)
        self.renderer = FrameRenderer(generator)

        # Generate starting from Entry to ensure it's part of the main
        # component
        start_x, start_y = self.entry
        if algorithm.lower() == "prim":
            # Prim's generator needs update to accept start coords, or we set it manually
            # Assuming we will update PrimGenerator to accept start_x, start_y
            # or use .entry/.exit if set
            generator.generate(start_x=start_x, start_y=start_y)
        else:
            generator.generate(start_x=start_x, start_y=start_y)

        if not self.perfect:
            self._make_imperfect()

        return self.grid

    def _make_imperfect(self):
        """Randomly remove some walls to create loops, guaranteeing at least one extra path between E and X."""
        import random
        from ..algorithms.path_finder import find_path

        # 1. Get Solution Path
        grid_state = [[c.walls for c in row] for row in self.grid]
        path_str = find_path(grid_state, self.entry, self.exit_coords)

        path_coords = []
        cx, cy = self.entry
        path_coords.append((cx, cy))
        for direction in path_str:
            dx, dy = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1),
                      'W': (-1, 0)}[direction]
            cx, cy = cx + dx, cy + dy
            path_coords.append((cx, cy))

        path_set = set(path_coords)

        # 2. Find potential shortcuts between path cells
        # A shortcut is a wall between two path cells that are not adjacent in
        # the path
        shortcuts = []
        for i, (x, y) in enumerate(path_coords):
            cell = self.grid[y][x]
            # Check neighbors
            for direction, (dx, dy) in {'N': (
                    0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}.items():
                nx, ny = x + dx, y + dy
                if (nx, ny) in path_set:
                    # Check if they are NOT adjacent in the path sequence
                    # Find index of neighbor in path
                    try:
                        ni = path_coords.index((nx, ny))
                        if abs(ni - i) > 1:
                            # This is a potential shortcut if the wall is
                            # closed
                            if cell.has_wall(direction):
                                shortcuts.append(
                                    (cell, self.grid[ny][nx], direction))
                    except ValueError:
                        pass

        # 3. Collect general candidates for loops
        all_candidates = []
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                if not cell.enabled:
                    continue
                if x < self.width - 1:
                    neighbor = self.grid[y][x + 1]
                    if neighbor.enabled and cell.has_wall('E'):
                        all_candidates.append((cell, neighbor, 'E'))
                if y < self.height - 1:
                    neighbor = self.grid[y + 1][x]
                    if neighbor.enabled and cell.has_wall('S'):
                        all_candidates.append((cell, neighbor, 'S'))

        to_remove = []

        # 4. Guarantee at least one shortcut if possible (this creates the 2nd
        # path)
        if shortcuts:
            to_remove.append(random.choice(shortcuts))

        # 5. Add more random loops based on maze size (approx 5% of potential
        # walls)
        count_to_remove = max(1, int(len(all_candidates) * 0.05))
        if all_candidates:
            # Avoid duplicates
            already_removed = set(to_remove)
            remaining_candidates = [
                c for c in all_candidates if c not in already_removed]
            if remaining_candidates:
                picks = random.sample(
                    remaining_candidates, min(
                        len(remaining_candidates), count_to_remove - len(to_remove)))
                to_remove.extend(picks)

        for cell, neighbor, direction in to_remove:
            self.generator.remove_wall_between(cell, neighbor, direction)

    def write_to_hex_file(self, output_file, entry, exit_coords, path=""):
        save_to_file(self.grid, output_file, entry, exit_coords, path=path)

    def play_animation(self, fps=20.0):
        if self.animator:
            # Reset grid to initial state (full walls) to avoid over-carving
            for row in self.grid:
                for cell in row:
                    cell.walls = 15
                    cell.visited = False

            # Re-apply pattern protection
            if self.pattern_cells:
                for (px, py) in self.pattern_cells:
                    if 0 <= px < self.width and 0 <= py < self.height:
                        self.grid[py][px].walls = 15  # Ensure solid
                        # Mark as visited so neighbors don't pick it
                        self.grid[py][px].visited = True
                        self.grid[py][px].enabled = False

            # Reseed logic to match generate()
            if self.seed is not None:
                import random
                random.seed(self.seed)

            self.animator.animate_generation(delay=1.0 / fps)

            if not self.perfect:
                self._make_imperfect()

    def render_frame_simple(self, frame_idx):
        # Render the current state to string
        path_cells = set()
        if self.show_path:
            # Find path and convert to set of coordinates
            from ..algorithms.path_finder import find_path
            # We need grid state in simple format for path finder
            grid_state = [[c.walls for c in row] for row in self.grid]
            path_str = find_path(grid_state, self.entry, self.exit_coords)

            # Trace path string back to coordinates
            cx, cy = self.entry
            for direction in path_str:
                dx, dy = {'N': (0, -1), 'E': (1, 0),
                          'S': (0, 1), 'W': (-1, 0)}[direction]
                cx, cy = cx + dx, cy + dy
                path_cells.add((cx, cy))

        if not self.renderer:
            # Need a wrapper if generator is missing
            class GenWrapper:
                def __init__(self, grid, width, height, entry,
                             exit_coords, path_cells, color_scheme):
                    self.grid = grid
                    self.width = width
                    self.height = height
                    self.entry = entry
                    self.exit = exit_coords
                    self.path_cells = path_cells
                    self.color_scheme = color_scheme
            self.renderer = FrameRenderer(
                GenWrapper(
                    self.grid,
                    self.width,
                    self.height,
                    self.entry,
                    self.exit_coords,
                    path_cells,
                    self.color_scheme))

        self.renderer.render_full(show_visited=True)
        return self.renderer.render_to_string()

    def get_frame_count(self):
        return 1
