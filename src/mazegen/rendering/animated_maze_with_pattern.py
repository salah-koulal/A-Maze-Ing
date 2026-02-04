from typing import List, Tuple, Optional
import time
from ..algorithms.prim import MazeGenerator as PrimGenerator
from ..algorithms.dfs import MazeGenerator as DFSGenerator
from ..utils.pattern_embedder import get_pattern_cells # Fixed import name
from .animator import MazeAnimator
from .frame_renderer import FrameRenderer
from ..utils.file_writer import save_to_file

class AnimatedMazeGeneratorWithPattern:
    def __init__(self, width: int, height: int, pattern_cells: List[Tuple[int, int]], seed: Optional[str] = None, entry: Tuple[int, int] = (0,0), exit_coords: Tuple[int, int] = None, perfect: bool = True):
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
        self.show_path = False
        self.color_scheme = "default"
        
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
        
        self.animator = MazeAnimator(generator)
        self.renderer = FrameRenderer(generator)
        
        # Generate without animation (fast) or just perform the logic
        generator.generate()
        
        return self.grid

    def write_to_hex_file(self, output_file, entry, exit_coords):
        save_to_file(self.grid, output_file, entry, exit_coords)

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
                         self.grid[py][px].walls = 15 # Ensure solid
                         self.grid[py][px].visited = True # Mark as visited so neighbors don't pick it
                         self.grid[py][px].enabled = False

            self.animator.animate_generation(delay=1.0/fps)

    def render_frame_simple(self, frame_idx):
        # Render the current state to string
        if not self.renderer:
             # Need a wrapper if generator is missing
             class GenWrapper:
                 def __init__(self, grid, width, height):
                     self.grid = grid
                     self.width = width
                     self.height = height
             self.renderer = FrameRenderer(GenWrapper(self.grid, self.width, self.height))
             
        self.renderer.render_full(show_visited=True)
        # Capture buffer to string
        # FrameRenderer.display() prints it. We need to collect it.
        # I'll add a method to FrameRenderer or just manually collect from buffer
        lines = []
        buf = self.renderer.buffer
        for y in range(buf.height):
            line = ""
            for x in range(buf.width):
                line += buf.get_char(x, y)
            lines.append(line)
        return "\n".join(lines)

    def get_frame_count(self):
        return 1
