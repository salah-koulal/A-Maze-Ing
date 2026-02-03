from maze_generator_DFS import MazeGenerator
import time
import os

BOX_CHARS = {
    0: ' ',
    1: '║',
    2: '║',
    3: '║',
    4: '═',
    5: '╚',
    6: '╔',
    7: '╠',
    8: '═',
    9: '╝',
    10: '╗',
    11: '╣',
    12: '═',
    13: '╩',
    14: '╦',
    15: '╬',
}


def get_corner_char(grid, cx, cy, width, height):
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


def render_maze(maze_generator, entry=None, exit_pos=None):
    grid = maze_generator.grid
    width = maze_generator.width
    height = maze_generator.height

    for y in range(height + 1):

        # Horizontal walls
        line = ""
        for x in range(width):
            line += get_corner_char(grid, x, y, width, height)

            if y < height and grid[y][x].has_wall('N'):
                line += "═══"
            elif y > 0 and grid[y - 1][x].has_wall('S'):
                line += "═══"
            else:
                line += "   "

        line += get_corner_char(grid, width, y, width, height)
        print(line)

        # Vertical walls + cell content
        if y < height:
            line = ""
            for x in range(width + 1):

                if x < width and grid[y][x].has_wall('W'):
                    line += "║"
                elif x > 0 and grid[y][x - 1].has_wall('E'):
                    line += "║"
                else:
                    line += " "

                if x < width:
                    if entry and (x, y) == entry:
                        line += " E "
                    elif exit_pos and (x, y) == exit_pos:
                        line += " X "
                    elif grid[y][x].walls == 15:
                        line += "███"
                    else:
                        line += "   "

            print(line)

def animate_text_slide(filepath, delay=0.03):
    with open(filepath,'r',encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]
    max_len = max(len(l) for l in lines)
    for i in range(max_len):
        os.system('clear')
        for line in lines:
            if i < len(line): print(line[:i+1])
            else: print(line)
        time.sleep(delay)
