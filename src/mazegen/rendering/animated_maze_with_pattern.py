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
        if self.show_path and self.grid:
            from ..algorithms.path_finder import find_path
            grid_state = [[c.walls for c in row] for row in self.grid]
            path_str = find_path(grid_state, self.entry, self.exit_coords)
            cx, cy = self.entry
            for direction in path_str:
                dx, dy = {
                    'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)
                }[direction]
                cx, cy = cx + dx, cy + dy
                path_cells.add((cx, cy))

        if not self._renderer and self.grid:
            class GenWrapper:
                def __init__(self, grid: List[List[Any]], width: int,
                             height: int, entry: Tuple[int, int],
                             exit_coords: Tuple[int, int],
                             path_cells: Set[Tuple[int, int]],
                             color_scheme: str):
                    self.grid, self.width, self.height = grid, width, height
                    self.entry, self.exit = entry, exit_coords
                    self.path_cells = path_cells
                    self.color_scheme = color_scheme
            self._renderer = FrameRenderer(GenWrapper(
                self.grid, self.width, self.height, self.entry,
                self.exit_coords, path_cells, self.color_scheme
            ))

        if self._renderer:
            self._renderer.render_full(show_visited=True)
            return self._renderer.render_to_string()
        return ""

    def get_frame_count(self) -> int:
        return 1
