# from typing import List, Tuple
# from .maze_generator_prim import Cell

# def write_maze_to_file(grid: List[List[Cell]], 
#                        entry: Tuple[int, int], 
#                        exit: Tuple[int, int], 
#                        path: str,
#                        filename: str) -> None:
#     """Write maze in hex format to file."""
#     with open(filename, 'w') as f:
#         for row in grid:
#             line = ''.join(format(cell.walls, 'X') for cell in row)
#             f.write(line + '\n')
        
#         f.write('\n')
        
#         f.write(f"{entry[0]},{entry[1]}\n")
#         f.write(f"{exit[0]},{exit[1]}\n")
#         f.write(f"{path}\n")