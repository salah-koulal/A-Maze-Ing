"""
Maps maze coordinates to screen coordinates.
"""

from typing import Tuple


class MazeScreenMapper:
    def __init__(self, offset_x: int = 0, offset_y: int = 0) -> None:
        """
        Initialize mapper.

        Args:
            offset_x: Screen X offset (top-left corner of maze)
            offset_y: Screen Y offset
        """
        self.offset_x = offset_x
        self.offset_y = offset_y

        # Each cell takes:
        # - 4 chars horizontally (corner + 3 for wall/content)
        # - 2 chars vertically (wall line + content line)
        self.cell_width = 4
        self.cell_height = 2

    def cell_to_screen(self, cell_x: int, cell_y: int) -> Tuple[int, int]:
        """
        Get screen position of cell's content area (center).

        Returns:
            (screen_x, screen_y) tuple (0-indexed)
        """
        screen_x = self.offset_x + cell_x * self.cell_width + 1
        screen_y = self.offset_y + cell_y * self.cell_height + 1
        return screen_x, screen_y

    def corner_to_screen(self, corner_x: int,
                         corner_y: int) -> Tuple[int, int]:
        """
        Get screen position of a corner.

        Returns:
            (screen_x, screen_y) tuple
        """
        screen_x = self.offset_x + corner_x * self.cell_width
        screen_y = self.offset_y + corner_y * self.cell_height
        return screen_x, screen_y

    def wall_north_to_screen(self, cell_x: int,
                             cell_y: int) -> Tuple[int, int]:
        """Get screen position of north wall of a cell."""
        screen_x = self.offset_x + cell_x * self.cell_width + 1
        screen_y = self.offset_y + cell_y * self.cell_height
        return screen_x, screen_y

    def wall_west_to_screen(self, cell_x: int,
                            cell_y: int) -> Tuple[int, int]:
        """Get screen position of west wall of a cell."""
        screen_x = self.offset_x + cell_x * self.cell_width
        screen_y = self.offset_y + cell_y * self.cell_height + 1
        return screen_x, screen_y
