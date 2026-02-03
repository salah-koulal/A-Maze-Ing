"""
Screen buffer for tracking what's drawn.
Avoids redrawing unchanged parts.
"""

class ScreenBuffer:
    def __init__(self, width, height):
        """
        Initialize buffer.
        
        Args:
            width: Screen width in characters
            height: Screen height in characters
        """
        self.width = width
        self.height = height
        
        # 2D array of characters
        self.buffer = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(' ')
            self.buffer.append(row)
    
    def set_char(self, x, y, char):
        """
        Set character at position.
        
        Args:
            x: Column (0-indexed)
            y: Row (0-indexed)
            char: Single character to set
        """
        if 0 <= y < self.height and 0 <= x < self.width:
            self.buffer[y][x] = char
    
    def set_string(self, x, y, string):
        """
        Set string starting at position.
        
        Args:
            x: Starting column
            y: Row
            string: String to write
        """
        for i in range(len(string)):
            self.set_char(x + i, y, string[i])
    
    def get_char(self, x, y):
        """Get character at position."""
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.buffer[y][x]
        return ' '
    
    def clear(self):
        """Clear buffer to spaces."""
        for y in range(self.height):
            for x in range(self.width):
                self.buffer[y][x] = ' '