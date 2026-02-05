from typing import List, Tuple, Any


def save_to_file(grid: List[List[Any]],
                 filename: str,
                 entry: Tuple[int, int],
                 exit_coords: Tuple[int, int],
                 path: str = "") -> None:
    """Write maze in hex format to file."""
    try:
        with open(filename, 'w') as f:
            for row in grid:
                line = ''.join(format(cell.walls, 'X') for cell in row)
                f.write(line + '\n')

            f.write('\n')

            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_coords[0]},{exit_coords[1]}\n")
            if path:
                f.write(f"{path}\n")
    except Exception as e:
        print(f"Error writing to file {filename}: {e}")
