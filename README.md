*This project has been created as part of the 42 curriculum by [skoulal] & [wabbad].*

# A-Maze-ing

---

<img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXkzc2kzbHJ6YnBmaGpwdWM0cGFvcndpejR0c2RnMnFwaGtiNmw4dyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3j9eE7bkTgHU8yS5BS/giphy.gif">

---

## Description

A-Maze-ing is a maze generator that creates perfect mazes with a single unique path between entry and exit points. The project implements Prim's algorithm for maze generation, provides a highly animated visual representation in ASCII, and outputs mazes in a hexadecimal wall encoding format as required by the 42 curriculum.

## Instructions

### Installation
```bash
# Clone the repository
git clone https://github.com/salah-koulal/A-Maze-Ing
cd A-Maze-Ing

# Install dependencies and set up environment
make install
```

### Usage
```bash
# Run with default configuration
python3 a_maze_ing.py config/default_config.txt
```

### Configuration File Format
The configuration file must contain one `KEY=VALUE` pair per line.
- `WIDTH`: Maze width (number of cells)
- `HEIGHT`: Maze height
- `ENTRY`: Entry coordinates (x,y)
- `EXIT`: Exit coordinates (x,y)
- `OUTPUT_FILE`: Output filename
- `PERFECT`: Is the maze perfect? (True/False)
- `SEED`: Random seed for reproducibility (optional)

## Maze Generation Algorithm

**Algorithm:** Prim's Algorithm (Frontier-based)

**Why this algorithm:**
- Produces mazes with many short dead ends and a more complex, less "directional" look than Recursive Backtracker.
- Easily adaptable for embedding patterns like "42" by marking cells as pre-visited.
- Efficiency: Uses a frontier set to grow the maze from a starting point, ensuring full connectivity.

**How it works:**
1. Start with a grid full of walls.
2. Pick a random cell, mark it as part of the maze.
3. Add the walls of that cell to the frontier list.
4. While the frontier list is not empty:
   - Pick a random wall from the frontier.
   - If the cell on the other side of the wall is not in the maze:
     - Remove the wall and mark the cell as part of the maze.
     - Add the new cell's walls to the frontier.
   - Remove the wall from the frontier.

## Reusable Module: `mazegen`

The maze generation logic is packaged as a standalone, pip-installable module named `mazegen`.

### Installation
You can install the package from the root of the repository:
```bash
pip install .
```
Or use the pre-built package:
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Documentation & Usage

#### 1. Instantiation
To use the generator, instantiate the `MazeGenerator` class. You can pass a configuration file path, and optionally override the seed and size.

```python
from mazegen import MazeGenerator

# Initialize from config file, size and seed are optional
generator = MazeGenerator("config/default_config.txt", seed="42", size=(53, 53))
```

#### 2. Generating the Maze
The `generate_maze()` method generates the maze structure using the selected algorithm (defaults to Prim's).

```python
# Generate maze
maze = generator.generate_maze()
```

#### 3. Accessing the Structure
The generated maze structure is returned as a 2D list of `Cell` objects (or internal representation). You can also draw it to the terminal.

```python
# Display the maze in ASCII
generator.draw_maze(maze)

# The structure is also accessible via:
# maze[y][x].walls  <- Bitmask of walls (N=1, E=2, S=4, W=8)
```

#### 4. Getting a Solution
You can retrieve the shortest path from the entry to the exit.

```python
# Get solution path as a string of movements (e.g., "EENSSW")
solution_path = generator.get_solution(maze)
print(f"Solution: {solution_path}")
```

#### 5. Interactive Mode
Run the full interactive generation and animation loop.

```python
generator.run()
```

## Team & Project Management

### Roles
- **[skoulal] (Salah eddine Koulal)**: Core algorithm implementation, Prim's logic, and hex output formatting, BFS path finding algorithm.
- **[wabbad] (walid)**: Visualization system, animation playback, and Maze generation using DFS.

### Project Evolution
- **Initial Plan**: Focus on basic Recusrive Backtracker.
- **Evolution**: Switched to Prim's Algorithm to better support the "42" pattern requirement and create more visually interesting mazes. Added a frame-by-frame animation system as a bonus feature.

### Resources

#### Documentation
- [Prim's Algorithm - Maze Generation](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim's_algorithm)
- [Box-Drawing Characters](https://en.wikipedia.org/wiki/Box-drawing_characters)
- [Mazes for Programmers (Jamis Buck)](https://www.kufunda.net/publicdocs/Mazes%20for%20Programmers%20Code%20Your%20Own%20Twisty%20Little%20Passages%20(Jamis%20Buck).pdf)
- [42 Subject PDF](A-maze-ing_subject.pdf)

#### Video Tutorials
- [Maze Generation Algorithm Visualization](https://www.youtube.com/watch?v=p9m2LHBW81M)
- [Prim's Algorithm Explained](https://www.youtube.com/watch?v=JavJqJHLo_M)
- [Maze Solving Algorithms](https://www.youtube.com/watch?v=u4QmAIoo4i0)

#### AI Usage
AI tools were used for guidance and debugging assistance during development.

### Tools Used
- **Git**: Version control
- **Make**: Automation
- **Python 3.10+**: Core language
- **Flake8/Mypy**: Linting and static analysis
