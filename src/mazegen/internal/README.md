# Maze Generation Internal Package

This package contains the core maze generation algorithms and utilities.

## Structure Overview

### Core Components

#### `maze_base.py`
- **`Cell`**: Represents a single maze cell with walls and visited state
- **`MazeGeneratorBase`**: Base class for all maze generation algorithms
  - Handles grid initialization
  - Provides common methods for cell neighbors
  - Manages pattern cell protection (e.g., "42" pattern)

#### Maze Generation Algorithms

##### `maze_generator_prim.py`
- **`PrimMazeGenerator`**: Implements Prim's frontier-based algorithm
- Creates mazes with many short dead ends
- Better for complex, less directional mazes

**How it works:**
1. Start with a random cell
2. Add its walls to a frontier list
3. Repeatedly pick random walls from frontier
4. If wall connects visited to unvisited cell, remove it
5. Add new walls to frontier

##### `maze_generator_dfs.py`
- **`DFSMazeGenerator`**: Implements Depth-First Search (recursive backtracker)
- Creates mazes with longer, winding passages
- Better for more linear, "river-like" mazes

**How it works:**
1. Start at a cell, mark as visited
2. Choose random unvisited neighbor
3. Remove wall and move to neighbor (recurse)
4. When stuck, backtrack (use stack)

#### Animation & Visualization

##### `maze_with_animation.py`
- **`MazeGeneratorWithAnimation`**: High-level wrapper for maze generation
- Captures animation frames during generation
- Provides rendering and visualization
- Handles pattern embedding (e.g., "42")
- Manages color schemes and path display

**Features:**
- Frame-by-frame animation capture
- Multiple color schemes (default, emerald, ocean, amber)
- Independent pattern colors (magenta, cyan, red, yellow, white)
- Path solving and visualization
- Hex file export

#### Utilities

##### `config_parser.py`
- Loads maze configuration from text files
- Parses WIDTH, HEIGHT, ENTRY, EXIT, SEED, PERFECT, OUTPUT_FILE

##### `pattern_embedder.py`
- Embeds patterns (like "42") into the maze
- Returns set of coordinates to protect during generation

##### `path_finder.py`
- Solves mazes using BFS
- Returns path as string of directions (N, E, S, W)

##### `file_writer.py`
- Exports mazes to hex format
- Includes entry, exit, and solution path

##### `leet_animation.py`
- Creates the "1337" startup animation
- Optional ASCII art display

## Usage Example

```python
from src.mazegen.internal.maze_with_animation import MazeGeneratorWithAnimation

# Create generator with 42 pattern
pattern_cells = {(5, 5), (5, 6), (6, 6)}  # Example pattern
gen = MazeGeneratorWithAnimation(
    width=20,
    height=15,
    pattern_cells=pattern_cells,
    seed=42,
    entry=(0, 0),
    exit_coords=(19, 14)
)

# Generate maze using Prim's algorithm
maze = gen.generate('prim')

# Or use DFS
maze = gen.generate('dfs')

# Play animation
gen.play_animation(fps=20.0)

# Export to file
gen.write_to_hex_file('output.txt', (0, 0), (19, 14))
```

## Algorithm Selection Guide

**Use Prim's when:**
- You want more complex, branching mazes
- You prefer shorter dead ends
- You want less predictable patterns

**Use DFS when:**
- You want longer, winding corridors
- You prefer more "river-like" flow
- You want simpler branching structure

## Pattern Protection

Both algorithms automatically avoid pattern cells during generation. Pattern cells are marked as "visited" from the start, so the algorithms never carve through them. This preserves patterns like the "42" design in the final maze.
