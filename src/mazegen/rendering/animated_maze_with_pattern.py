from typing import List, Tuple, Optional, Any, Set, Union
from ..algorithms.prim import MazeGenerator as PrimGenerator
from ..algorithms.dfs import MazeGenerator as DFSGenerator
from .animator import MazeAnimator
from .frame_renderer import FrameRenderer
from ..utils.file_writer import save_to_file
import random
from ..algorithms.path_finder import find_path


class AnimatedMazeGeneratorWithPattern:
    def __init__(self, width: int, height: int,
                 pattern_cells: List[Tuple[int, int]],
                 seed: Optional[str] = None,
                 entry: Tuple[int, int] = (0, 0),
                 exit_coords: Optional[Tuple[int, int]] = None,
                 perfect: bool = True) -> None:
        self.width = width
        self.height = height
        self.pattern_cells = pattern_cells

        if seed is not None:
            try:
                self.seed = int(seed)
            except (ValueError, TypeError):
                import random
                self.seed = random.randint(0, 1000000)
        else:
            import random
            self.seed = random.randint(0, 1000000)

        self.entry = entry
        self.exit_coords = exit_coords or (width - 1, height - 1)
        self.perfect = perfect

        self.grid: Optional[List[List[Any]]] = None
        self.animator: Optional[MazeAnimator] = None
        self._renderer: Optional[FrameRenderer] = None
        self._show_path = False
        self._color_scheme = "default"
        self.generator: Any = None

        self._init_generator_stub()

    @property
    def show_path(self) -> bool:
        return self._show_path

    @show_path.setter
    def show_path(self, value: bool) -> None:
        self._show_path = value
        self._renderer = None

    @property
    def color_scheme(self) -> str:
        return self._color_scheme

    @color_scheme.setter
    def color_scheme(self, value: str) -> None:
        self._color_scheme = value
        self._renderer = None
        if hasattr(self, 'generator') and self.generator:
            self.generator.color_scheme = value

    def _init_generator_stub(self) -> None:
        temp_gen = PrimGenerator(self.width, self.height, self.seed)
        self.grid = temp_gen.grid
        for row in self.grid:
            for cell in row:
                cell.enabled = True

        if self.pattern_cells:
            for (px, py) in self.pattern_cells:
                if 0 <= px < self.width and 0 <= py < self.height:
                    self.grid[py][px].enabled = False

    def generate(self, algorithm: str = "prim") -> List[List[Any]]:
        gen_class: Union[type[PrimGenerator], type[DFSGenerator]] = (
            PrimGenerator if algorithm.lower() == "prim" else DFSGenerator
        )

        import random
        random.seed(self.seed)

        generator: Any = gen_class(self.width, self.height, self.seed)
        self.generator = generator
        generator.entry = self.entry
        generator.exit = self.exit_coords
        self.grid = generator.grid

        if self.grid:
            for row in self.grid:
                for cell in row:
                    cell.enabled = True

        if self.pattern_cells and self.grid:
            for (px, py) in self.pattern_cells:
                if 0 <= px < self.width and 0 <= py < self.height:
                    self.grid[py][px].enabled = False
                    self.grid[py][px].visited = True

        generator.color_scheme = self.color_scheme
        self.animator = MazeAnimator(generator)
        self._renderer = FrameRenderer(generator)

        generator.generate(start_x=self.entry[0], start_y=self.entry[1])

        if not self.perfect:
            self._make_imperfect()

        return self.grid if self.grid else []

    def _make_imperfect(self) -> None:
        if not self.grid:
            return

        grid_state = [[c.walls for c in row] for row in self.grid]
        path_str = find_path(grid_state, self.entry, self.exit_coords)

        path_coords = [(self.entry[0], self.entry[1])]
        cx, cy = self.entry
        for direction in path_str:
            dx, dy = {
                'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)
            }[direction]
            cx, cy = cx + dx, cy + dy
            path_coords.append((cx, cy))

        path_set = set(path_coords)
        shortcuts = []
        for i, (x, y) in enumerate(path_coords):
            cell = self.grid[y][x]
            for direction, (dx, dy) in {
                'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)
            }.items():
                nx, ny = x + dx, y + dy
                if (nx, ny) in path_set:
                    try:
                        ni = path_coords.index((nx, ny))
                        if abs(ni - i) > 1 and cell.has_wall(direction):
                            shortcuts.append(
                                (cell, self.grid[ny][nx], direction)
                            )
                    except ValueError:
                        pass

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
        if shortcuts:
            to_remove.append(random.choice(shortcuts))

        count_to_remove = max(1, int(len(all_candidates) * 0.05))
        if all_candidates:
            already_removed = set(to_remove)
            remaining = [c for c in all_candidates if c not in already_removed]
            if remaining:
                picks = random.sample(
                    remaining, min(len(remaining), count_to_remove)
                )
                to_remove.extend(picks)

        for cell, neighbor, direction in to_remove:
            if self.generator:
                self.generator.remove_wall_between(cell, neighbor, direction)

    def write_to_hex_file(self, output_file: str, entry: Tuple[int, int],
                          exit_coords: Tuple[int, int],
                          path: str = "") -> None:
        if self.grid:
            save_to_file(self.grid, output_file, entry, exit_coords, path=path)

    def play_animation(self, fps: float = 15.0) -> None:
        if not self.animator or not self.grid:
            return

        for row in self.grid:
            for cell in row:
                cell.walls = 15
                cell.visited = False

        if self.pattern_cells:
            for (px, py) in self.pattern_cells:
                if 0 <= px < self.width and 0 <= py < self.height:
                    self.grid[py][px].walls = 15
                    self.grid[py][px].visited = True
                    self.grid[py][px].enabled = False

        import random
        random.seed(self.seed)
        self.animator.animate_generation(delay=1.0 / fps)

        if not self.perfect:
            self._make_imperfect()

    def render_frame_simple(self, frame_idx: int) -> str:
        path_cells: Set[Tuple[int, int]] = set()
        path_directions: dict[Tuple[int, int], Tuple[str, ...]] = {}

        if self.show_path and self.grid:
            from ..algorithms.path_finder import find_path
            grid_state = [[c.walls for c in row] for row in self.grid]
            path_str = find_path(grid_state, self.entry, self.exit_coords)

            # Build path coordinates list
            path_coords = [self.entry]
            cx, cy = self.entry
            for direction in path_str:
                dx, dy = {
                    'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)
                }[direction]
                cx, cy = cx + dx, cy + dy
                path_coords.append((cx, cy))

            # Compute directions for each cell
            opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
            for i, coord in enumerate(path_coords):
                dirs: List[str] = []
                # Direction we came from (previous cell -> this cell)
                if i > 0:
                    prev = path_coords[i - 1]
                    dx, dy = coord[0] - prev[0], coord[1] - prev[1]
                    from_dir = {(0, -1): 'N', (1, 0): 'E',
                                (0, 1): 'S', (-1, 0): 'W'}[(dx, dy)]
                    dirs.append(opposite[from_dir])  # came FROM this direction
                # Direction we're going to (this cell -> next cell)
                if i < len(path_coords) - 1:
                    next_c = path_coords[i + 1]
                    dx, dy = next_c[0] - coord[0], next_c[1] - coord[1]
                    to_dir = {(0, -1): 'N', (1, 0): 'E',
                              (0, 1): 'S', (-1, 0): 'W'}[(dx, dy)]
                    dirs.append(to_dir)

                path_cells.add(coord)
                path_directions[coord] = tuple(dirs)

        if self.grid:
            class GenWrapper:
                def __init__(self, grid: List[List[Any]], width: int,
                             height: int, entry: Tuple[int, int],
                             exit_coords: Tuple[int, int],
                             p_cells: Set[Tuple[int, int]],
                             p_dirs: dict[Tuple[int, int], Tuple[str, ...]],
                             color_scheme: str):
                    self.grid, self.width, self.height = grid, width, height
                    self.entry, self.exit = entry, exit_coords
                    self.path_cells = p_cells
                    self.path_directions = p_dirs
                    self.color_scheme = color_scheme
            self._renderer = FrameRenderer(GenWrapper(
                self.grid, self.width, self.height, self.entry,
                self.exit_coords, path_cells, path_directions,
                self.color_scheme
            ))

        if self._renderer:
            self._renderer.render_full(show_visited=True)
            return self._renderer.render_to_string()
        return ""

    def animate_path(self, delay: float = 0.05) -> None:
        """
        Animate the path finding from entry to exit.
        Shows the path being drawn cell by cell smoothly.
        """
        if not self.grid:
            return

        from ..utils.terminal_controls import (
            hide_cursor, show_cursor, move_cursor
        )
        from ..algorithms.path_finder import find_path
        import time

        grid_state = [[c.walls for c in row] for row in self.grid]
        path_str = find_path(grid_state, self.entry, self.exit_coords)

        # Build full path coordinates
        path_coords = [self.entry]
        cx, cy = self.entry
        for direction in path_str:
            dx, dy = {
                'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)
            }[direction]
            cx, cy = cx + dx, cy + dy
            path_coords.append((cx, cy))

        hide_cursor()

        # Animate path cell by cell
        animated_cells: Set[Tuple[int, int]] = set()
        animated_dirs: dict[Tuple[int, int], Tuple[str, ...]] = {}
        opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

        for i, coord in enumerate(path_coords):
            # Skip entry and exit (they have their own markers)
            if coord == self.entry or coord == self.exit_coords:
                continue

            # Compute direction for this cell
            dirs: List[str] = []
            if i > 0:
                prev = path_coords[i - 1]
                dx, dy = coord[0] - prev[0], coord[1] - prev[1]
                from_dir = {(0, -1): 'N', (1, 0): 'E',
                            (0, 1): 'S', (-1, 0): 'W'}[(dx, dy)]
                dirs.append(opposite[from_dir])
            if i < len(path_coords) - 1:
                next_c = path_coords[i + 1]
                dx, dy = next_c[0] - coord[0], next_c[1] - coord[1]
                to_dir = {(0, -1): 'N', (1, 0): 'E',
                          (0, 1): 'S', (-1, 0): 'W'}[(dx, dy)]
                dirs.append(to_dir)

            animated_cells.add(coord)
            animated_dirs[coord] = tuple(dirs)

            # Create wrapper with current animated cells
            class GenWrapper:
                def __init__(self, grid: List[List[Any]], width: int,
                             height: int, entry: Tuple[int, int],
                             exit_coords: Tuple[int, int],
                             p_cells: Set[Tuple[int, int]],
                             p_dirs: dict[Tuple[int, int], Tuple[str, ...]],
                             color_scheme: str):
                    self.grid, self.width, self.height = grid, width, height
                    self.entry, self.exit = entry, exit_coords
                    self.path_cells = p_cells
                    self.path_directions = p_dirs
                    self.color_scheme = color_scheme

            renderer = FrameRenderer(GenWrapper(
                self.grid, self.width, self.height, self.entry,
                self.exit_coords, animated_cells.copy(), animated_dirs.copy(),
                self.color_scheme
            ))
            renderer.render_full(show_visited=True)
            move_cursor(1, 1)
            print(renderer.render_to_string(), end='', flush=True)
            time.sleep(delay)

        show_cursor()
        print()

    def get_frame_count(self) -> int:
        return 1
