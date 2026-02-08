"""
Frame-based maze renderer.
Renders maze state to a screen buffer.
"""

from typing import Dict, Tuple, Any, Optional, Set, List
from .screen_buffer import ScreenBuffer
from .screen_mapper import MazeScreenMapper

BOX_CHARS = {
    0: ' ', 1: '║', 2: '║', 3: '║',
    4: '═', 5: '╚', 6: '╔', 7: '╠',
    8: '═', 9: '╝', 10: '╗', 11: '╣',
    12: '═', 13: '╩', 14: '╦', 15: '╬',
}

COLORS: Dict[str, Dict[str, str]] = {
    "default": {
        "wall": "\033[0m", "path": "\033[0m",
        "entry": "\033[0m", "exit": "\033[0m"
    },
    "subject": {
        "wall": "\033[36m", "path": "\033[93m",
        "entry": "\033[92m", "exit": "\033[91m"
    },
    "vivid": {
        "wall": "\033[44m\033[37m", "path": "\033[43m\033[30m",
        "entry": "\033[42m\033[30m", "exit": "\033[41m\033[37m"
    },
    "emerald": {
        "wall": "\033[32m", "path": "\033[92m",
        "entry": "\033[42m\033[30m", "exit": "\033[42m\033[30m"
    },
    "ocean": {
        "wall": "\033[34m", "path": "\033[94m",
        "entry": "\033[44m\033[37m", "exit": "\033[44m\033[37m"
    },
    "amber": {
        "wall": "\033[33m", "path": "\033[93m",
        "entry": "\033[43m\033[30m", "exit": "\033[43m\033[30m"
    },
}
RESET = "\033[0m"


class FrameRenderer:
    def __init__(self, maze_generator: Any) -> None:
        """
        Initialize renderer.

        Args:
            maze_generator: MazeGenerator instance
        """
        self.generator = maze_generator
        self.width: int = maze_generator.width
        self.height: int = maze_generator.height
        self.grid: List[List[Any]] = maze_generator.grid

        screen_width = self.width * 4 + 1
        screen_height = self.height * 2 + 1

        self.buffer = ScreenBuffer(screen_width, screen_height)
        self.color_buffer: Dict[Tuple[int, int], str] = {}
        self.mapper = MazeScreenMapper(offset_x=0, offset_y=0)

        self.entry: Optional[Tuple[int, int]] = getattr(
            maze_generator, 'entry', None
        )
        self.exit: Optional[Tuple[int, int]] = getattr(
            maze_generator, 'exit', None
        )
        self.path_cells: Set[Tuple[int, int]] = getattr(
            maze_generator, 'path_cells', set()
        )
        self.color_scheme: str = getattr(
            maze_generator, 'color_scheme', 'default'
        )

    def get_corner_char(self, cx: int, cy: int) -> str:
        """Calculate corner character."""
        grid = self.grid
        width = self.width
        height = self.height

        mask = 0

        if cy > 0:
            if cx < width and grid[cy - 1][cx].has_wall('W'):
                mask |= 1
            elif cx > 0 and grid[cy - 1][cx - 1].has_wall('E'):
                mask |= 1

        if cy < height:
            if cx < width and grid[cy][cx].has_wall('W'):
                mask |= 2
            elif cx > 0 and grid[cy][cx - 1].has_wall('E'):
                mask |= 2

        if cx < width:
            if cy < height and grid[cy][cx].has_wall('N'):
                mask |= 4
            elif cy > 0 and grid[cy - 1][cx].has_wall('S'):
                mask |= 4

        if cx > 0:
            if cy < height and grid[cy][cx - 1].has_wall('N'):
                mask |= 8
            elif cy > 0 and grid[cy - 1][cx - 1].has_wall('S'):
                mask |= 8

        return BOX_CHARS[mask]

    def set_color(self, x: int, y: int, type_key: str) -> None:
        """Set color type for a coordinate."""
        self.color_buffer[(x, y)] = type_key

    def set_string_color(self, x: int, y: int, s: str, type_key: str) -> None:
        """Set color type for a string starting at x,y."""
        for i in range(len(s)):
            self.color_buffer[(x + i, y)] = type_key

    def render_full(self, current_cell: Optional[Any] = None,
                    show_visited: bool = True) -> None:
        """
        Render complete maze to buffer.

        Args:
            current_cell: Cell to highlight as current
            show_visited: Whether to show visited cells
        """
        self.buffer.clear()
        self.color_buffer.clear()

        for y in range(self.height + 1):
            for x in range(self.width):
                sx, sy = self.mapper.corner_to_screen(x, y)
                corner_char = self.get_corner_char(x, y)
                self.buffer.set_char(sx, sy, corner_char)
                self.set_color(sx, sy, "wall")

                wx, wy = self.mapper.wall_north_to_screen(x, y)
                if y < self.height and self.grid[y][x].has_wall('N'):
                    s = "═══"
                    self.buffer.set_string(wx, wy, s)
                    self.set_string_color(wx, wy, s, "wall")
                elif y > 0 and self.grid[y - 1][x].has_wall('S'):
                    s = "═══"
                    self.buffer.set_string(wx, wy, s)
                    self.set_string_color(wx, wy, s, "wall")
                else:
                    self.buffer.set_string(wx, wy, "   ")

            sx, sy = self.mapper.corner_to_screen(self.width, y)
            corner_char = self.get_corner_char(self.width, y)
            self.buffer.set_char(sx, sy, corner_char)
            self.set_color(sx, sy, "wall")

        for y in range(self.height):
            for x in range(self.width + 1):
                if x < self.width:
                    wx, wy = self.mapper.wall_west_to_screen(x, y)
                    if self.grid[y][x].has_wall('W'):
                        self.buffer.set_char(wx, wy, '║')
                        self.set_color(wx, wy, "wall")
                    elif x > 0 and self.grid[y][x - 1].has_wall('E'):
                        self.buffer.set_char(wx, wy, '║')
                        self.set_color(wx, wy, "wall")
                    else:
                        self.buffer.set_char(wx, wy, ' ')

                if x < self.width:
                    cell = self.grid[y][x]
                    cx, cy = self.mapper.cell_to_screen(x, y)

                    if not cell.enabled:
                        s = "███"
                        self.buffer.set_string(cx, cy, s)
                        self.set_string_color(cx, cy, s, "wall")
                    elif self.entry and (x, y) == self.entry:
                        s = " E "
                        self.buffer.set_string(cx, cy, s)
                        self.set_string_color(cx, cy, s, "entry")
                    elif self.exit and (x, y) == self.exit:
                        s = " X "
                        self.buffer.set_string(cx, cy, s)
                        self.set_string_color(cx, cy, s, "exit")
                    elif (hasattr(self, 'path_cells') and self.path_cells and
                          (x, y) in self.path_cells):
                        s = " █ "
                        self.buffer.set_string(cx, cy, s)
                        self.set_string_color(cx, cy, s, "path")
                    elif (current_cell and
                          (x, y) == (current_cell.x, current_cell.y)):
                        self.buffer.set_string(cx, cy, "■■■")
                    elif show_visited and cell.visited:
                        self.buffer.set_string(cx, cy, " · ")
                    elif not show_visited or not cell.visited:
                        s = "███"
                        self.buffer.set_string(cx, cy, s)
                        self.set_string_color(cx, cy, s, "wall")
                    else:
                        self.buffer.set_string(cx, cy, "   ")

                if x == self.width:
                    wx = self.mapper.offset_x + x * self.mapper.cell_width
                    wy = self.mapper.offset_y + y * self.mapper.cell_height + 1
                    if self.grid[y][x - 1].has_wall('E'):
                        self.buffer.set_char(wx, wy, '║')
                        self.set_color(wx, wy, "wall")
                    else:
                        self.buffer.set_char(wx, wy, ' ')

    def render_to_string(self) -> str:
        """Return the buffer content as a string with ANSI colors."""
        scheme_name = getattr(
            self.generator,
            'color_scheme',
            self.color_scheme)
        scheme = COLORS.get(scheme_name, COLORS["default"])

        lines = []
        current_color_code = None

        for y in range(self.buffer.height):
            line = ""
            for x in range(self.buffer.width):
                char = self.buffer.get_char(x, y)
                type_key = self.color_buffer.get((x, y))
                color_code = (
                    scheme.get(type_key, "\033[0m")
                    if type_key else "\033[0m"
                )

                if color_code != current_color_code:
                    if current_color_code:
                        line += RESET
                    if color_code != "\033[0m":
                        line += color_code
                    current_color_code = color_code

                line += char

            if current_color_code and current_color_code != "\033[0m":
                line += RESET
            current_color_code = None
            lines.append(line)

        return "\n".join(lines)

    def display(self) -> None:
        """Display the buffer to screen."""
        from ..utils.terminal_controls import move_cursor

        for y, line in enumerate(self.render_to_string().split('\n')):
            move_cursor(1, y + 1)
            print(line, end='', flush=True)
