class ScreenBuffer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = [[' ' for _ in range(width)] for _ in range(height)]

    def clear(self):
        self.buffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]

    def set_char(self, x, y, char):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y][x] = char

    def set_string(self, x, y, s):
        for i, char in enumerate(s):
            self.set_char(x + i, y, char)

    def get_char(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.buffer[y][x]
        return ' '
