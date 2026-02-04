"""
Frame-based maze renderer.
Renders maze state to a screen buffer.
"""

from .screen_buffer import ScreenBuffer
from .screen_mapper import MazeScreenMapper

BOX_CHARS = {
    0: ' ', 1: '║', 2: '║', 3: '║',
    4: '═', 5: '╚', 6: '╔', 7: '╠',
    8: '═', 9: '╝', 10: '╗', 11: '╣',
    12: '═', 13: '╩', 14: '╦', 15: '╬',
}

class FrameRenderer:
    def __init__(self, maze_generator):
        """
        Initialize renderer.
        
        Args:
            maze_generator: MazeGenerator instance
        """
        self.generator = maze_generator
        self.width = maze_generator.width
        self.height = maze_generator.height
        self.grid = maze_generator.grid
        
        # Calculate screen size needed
        # Each cell is 4x2, plus borders
        screen_width = self.width * 4 + 1
        screen_height = self.height * 2 + 1
        
        self.buffer = ScreenBuffer(screen_width, screen_height)
        self.mapper = MazeScreenMapper(offset_x=0, offset_y=0)
    
    def get_corner_char(self, cx, cy):
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
    
    def render_full(self, current_cell=None, show_visited=True):
        """
        Render complete maze to buffer.
        
        Args:
            current_cell: Cell to highlight as current
            show_visited: Whether to show visited cells
        """
        # Clear buffer
        self.buffer.clear()
        
        # Draw all corners and walls
        for y in range(self.height + 1):
            for x in range(self.width):
                # Corner
                sx, sy = self.mapper.corner_to_screen(x, y)
                corner_char = self.get_corner_char(x, y)
                self.buffer.set_char(sx, sy, corner_char)
                
                # Horizontal wall
                wx, wy = self.mapper.wall_north_to_screen(x, y)
                if y < self.height and self.grid[y][x].has_wall('N'):
                    self.buffer.set_string(wx, wy, "═══")
                elif y > 0 and self.grid[y - 1][x].has_wall('S'):
                    self.buffer.set_string(wx, wy, "═══")
                else:
                    self.buffer.set_string(wx, wy, "   ")
            
            # Last corner on right
            sx, sy = self.mapper.corner_to_screen(self.width, y)
            corner_char = self.get_corner_char(self.width, y)
            self.buffer.set_char(sx, sy, corner_char)
        
        # Draw cell contents and vertical walls
        for y in range(self.height):
            for x in range(self.width + 1):
                # Vertical wall
                if x < self.width:
                    wx, wy = self.mapper.wall_west_to_screen(x, y)
                    if self.grid[y][x].has_wall('W'):
                        self.buffer.set_char(wx, wy, '║')
                    elif x > 0 and self.grid[y][x - 1].has_wall('E'):
                        self.buffer.set_char(wx, wy, '║')
                    else:
                        self.buffer.set_char(wx, wy, ' ')
                
                # Cell content
                if x < self.width:
                    cell = self.grid[y][x]
                    cx, cy = self.mapper.cell_to_screen(x, y)
                    
                    if not cell.enabled:
                        # Pattern cell
                        self.buffer.set_string(cx, cy, "███")
                    elif current_cell and (x, y) == (current_cell.x, current_cell.y):
                        # Current cell
                        self.buffer.set_string(cx, cy, "■■■")
                    elif show_visited and cell.visited:
                        # Visited cell
                        self.buffer.set_string(cx, cy, " · ")
                    elif not show_visited or not cell.visited:
                        # Hidden/unvisited
                        self.buffer.set_string(cx, cy, "███")
                    else:
                        # Empty
                        self.buffer.set_string(cx, cy, "   ")
                
                # Right edge wall
                if x == self.width:
                    wx = self.mapper.offset_x + x * self.mapper.cell_width
                    wy = self.mapper.offset_y + y * self.mapper.cell_height + 1
                    if self.grid[y][x - 1].has_wall('E'):
                        self.buffer.set_char(wx, wy, '║')
                    else:
                        self.buffer.set_char(wx, wy, ' ')
    
    def display(self):
        """Display the buffer to screen."""
        from ..utils.terminal_controls import move_cursor
        
        for y in range(self.buffer.height):
            move_cursor(1, y + 1)
            line = ""
            for x in range(self.buffer.width):
                line += self.buffer.get_char(x, y)
            print(line, end='', flush=True)