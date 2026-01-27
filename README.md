# A-Maze-Ing
This project is about Creating your own maze generator and display its result!


## Will be updated later  
<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmoyampnYmt4ZWJmYmJubGRocnYwM3d5eXM3OHQyOGV4MXBwNTFjMCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/XZrUw9cTqJ0vi8bmV9/giphy.gif">


---
---


# A-Maze-ing

*This project has been created as part of the 42 curriculum by [skoulal] & [wabbad].*

## Description

A-Maze-ing is a maze generator that creates perfect mazes with a single unique path between entry and exit points. The project implements maze generation algorithms, provides visual representation, and outputs mazes in a hexadecimal wall encoding format.

## Features

- Random maze generation with reproducible seeds
- Perfect maze support (single path between entry and exit)
- Hexadecimal wall encoding output
- Visual representation (ASCII/MLX)
- "42" pattern embedded in maze structure
- Configurable via text files

## Instructions

### Installation
```bash
# Clone the repository
git clone https://github.com/salah-koulal/A-Maze-Ing
cd A-Maze-Ing

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make install
```

### Usage
```bash
# Run with default configuration
make run

# Run with custom configuration
python3 a_maze_ing.py config/my_config.txt
```

### Configuration File Format

The configuration file uses KEY=VALUE pairs, one per line:

WIDTH=20           # Maze width in cells
HEIGHT=15          # Maze height in cells
ENTRY=0,0          # Entry coordinates (x,y)
EXIT=19,14         # Exit coordinates (x,y)
OUTPUT_FILE=maze.txt  # Output filename
PERFECT=True       # Perfect maze flag
SEED=42            # Random seed (optional)

Lines starting with `#` are comments and will be ignored.

## Maze Generation Algorithm

**Algorithm:** Recursive Backtracker

**Why this algorithm:**
- Simple to implement and understand
- Guarantees perfect mazes (no loops, single path)
- Creates interesting long, winding passages
- Memory efficient with stack-based approach

**How it works:**
1. Start at a random cell, mark it as visited
2. While there are unvisited cells:
   - If current cell has unvisited neighbors:
     - Choose random unvisited neighbor
     - Remove wall between current and neighbor
     - Move to neighbor
   - Else backtrack to previous cell

## Reusable Code

The maze generation logic is packaged as `mazegen` and can be installed via pip:
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

**Usage example:**
```python
from mazegen import MazeGenerator

# Create a maze generator
generator = MazeGenerator(width=20, height=15, seed=42)

# Generate a perfect maze
maze = generator.generate(perfect=True)

# Get the solution path
path = generator.find_path(entry=(0,0), exit=(19,14))

# Access maze structure
for row in maze.grid:
    for cell in row:
        print(cell.walls)
```

See `docs/package_usage.md` for detailed documentation.

## Development

### Running Tests
```bash
make test
```

### Linting
```bash
make lint          # Standard linting
make lint-strict   # Strict type checking
```

### Cleaning
```bash
make clean
```

## Resources

### Classic References
- [Maze Generation Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Think Labyrinth: Maze Algorithms](http://www.astrolog.org/labyrnth/algrithm.htm)
- [Jamis Buck's Maze Generation Blog](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)

### AI Usage
- **Algorithm research:** Used AI to compare different maze generation algorithms
- **Code structure:** Discussed project organization and module design
- **Documentation:** Generated initial docstring templates
- **Debugging:** Asked for help with wall coherence validation logic

## Team & Project Management

### Team Members
- **Member 1 (Core Logic):** [Salah eddine Koulal/ skoulal] - Maze generation, algorithms, file I/O
- **Member 2 (Interface):** [walid / wabbad] - Visualization, packaging, integration


### What Worked Well
- Early agreement on data structures prevented integration issues
- Daily standups kept us aligned
- Pair programming on complex algorithms

### What Could Be Improved
- Should have started testing earlier
- Need better git branching strategy
- Documentation could be more detailed

### Tools Used
- **Git/GitHub:** Version control
- **Pytest:** Testing framework
- **Discord:** Daily communication

## License

This is an educational project for 42 School.