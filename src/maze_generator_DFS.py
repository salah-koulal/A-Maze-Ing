import random


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = 15
        self.visited = False
        self.enabled = True

    def has_wall(self, point):
        wall = {'N': 0b0001, 'E': 0b0010, 'S': 0b0100, 'W': 0b1000}
        return bool(self.walls & wall[point])

    def remove_wall(self, point):
        wall = {'N': 0b0001, 'E': 0b0010, 'S': 0b0100, 'W': 0b1000}
        self.walls = self.walls & ~wall[point]

class MazeGenerator:
    def __init__(self, width, height, seed = 42):
        self.height = height
        self.width = width
        self.seed = seed;
        random.seed(seed)

        self.grid = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(Cell(x,y))
            self.grid.append(row)


    def _get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None


    def _get_unvisited_neighbors(self, cell):
        neighbors = []
        directions = {
            'N':(0, -1),
            'E':(1, 0),
            'S':(0, 1),
            'W':(-1, 0)
        }
        for direction in directions:
            dx, dy = directions[direction]
            nx = cell.x + dx
            ny = cell.y + dy
            neighbor = self._get_cell(nx, ny)
            if neighbor and neighbor.enabled and not neighbor.visited:
                neighbors.append((neighbor, direction))
        return neighbors

    def _carve_passage(self, current, neighbor, direction):
        current.remove_wall(direction)

        opposits = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        neighbor.remove_wall(opposits[direction])
    def apply_42_pattern(self):
 
        pattern = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]

        pattern_height = 5
        pattern_width = 7


        try :
            if self.width < pattern_width or self.height < pattern_height:
                raise ValueError("Maze too small for pattern")
        except ValueError:
            print("The maze IS too small !")   
            return False

        center_x = (self.width - pattern_width) // 2
        center_y = (self.height - pattern_height) // 2


        for py in range(pattern_height):
            for px in range(pattern_width):
                if pattern[py][px] == 1:
                    x = center_x + px
                    y = center_y + py

                    self.grid[y][x].walls = 15 
                    self.grid[y][x].visited = True
                    self.grid[y][x].enabled = False

        return True

    
    def generate(self, start_x= 0, start_y= 0):
        for row in self.grid:
            for cell in row:
                if cell.walls != 15:
                    cell.visited = False

        start_cell = self.grid[start_y][start_x]
        stack = []
        stack.append(start_cell)
        start_cell.visited = True

        while len(stack) > 0:
            start_cell = stack[-1]
            neighbors = self._get_unvisited_neighbors(start_cell)
            
            if len(neighbors) == 0:
                stack.pop()
            else:
                neighbor, direction = random.choice(neighbors)
                self._carve_passage(start_cell, neighbor, direction)
                neighbor.visited = True
                stack.append(neighbor)
        return self.grid

