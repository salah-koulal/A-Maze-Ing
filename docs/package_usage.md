# Mazegen Package - Usage Guide

## Installation
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

## Quick Start
```python
from mazegen import MazeGenerator

# Create generator
gen = MazeGenerator(width=20, height=15, seed=42)

# Generate maze
grid = gen.generate()

# Access cells
for row in grid:
    for cell in row:
        print(f"Cell ({cell.x},{cell.y}): walls={cell.walls}")
```

## API Reference

### MazeGenerator

**Parameters:**
- `width` (int): Maze width in cells
- `height` (int): Maze height in cells  
- `seed` (int, optional): Random seed for reproducibility

**Methods:**
- `generate()`: Returns List[List[Cell]]
- `get_cell(x, y)`: Get cell at coordinates
- `get_neighbors(cell)`: Get cell neighbors

### Cell

**Attributes:**
- `x` (int): X coordinate
- `y` (int): Y coordinate
- `walls` (int): Bit-encoded walls (0-15)
- `visited` (bool): Whether cell visited

**Methods:**
- `has_wall(direction)`: Check if wall exists ('N', 'E', 'S', 'W')
- `remove_wall(direction)`: Remove a wall