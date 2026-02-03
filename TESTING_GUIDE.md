# Testing Guide for A-Maze-Ing

This guide explains how to test the newly refactored features in the A-Maze-Ing project.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Running Existing Tests](#running-existing-tests)
3. [Manual Testing](#manual-testing)
4. [Testing New Features](#testing-new-features)
5. [Writing New Tests](#writing-new-tests)

## Quick Start

### Run All Tests
```bash
# Using make (recommended)
make test

# Or directly with pytest
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_maze_base.py -v
pytest tests/test_algorithms.py -v
pytest tests/test_animation.py -v
```

### Run the Application
```bash
# Interactive mode
python3 a_maze_ing.py config/default_config.txt

# With custom size
python3 -c "
from src.mazegen.generator import MazeGenerator
gen = MazeGenerator('config/default_config.txt', size=(10, 8))
gen.generate_maze()
gen.draw_maze()
"
```

## Running Existing Tests

The project uses `pytest` for testing. Tests are located in the `tests/` directory.

### Install Testing Dependencies
```bash
pip install pytest pytest-cov
```

### Run Tests with Coverage
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

### Run Specific Tests
```bash
# Test path finder
pytest tests/test_path_finder.py -v

# Test file writer
pytest tests/test_file_writer.py -v

# Test with verbose output
pytest tests/ -vv
```

## Manual Testing

### 1. Testing Both Algorithms

```python
from src.mazegen.generator import MazeGenerator

# Create generator
gen = MazeGenerator('config/default_config.txt', size=(10, 8), seed=42)

# Test Prim's algorithm
print("Testing Prim's...")
gen.current_algo_idx = 0  # Prim's
maze = gen.generate_maze()
print(f"✓ Generated {len(maze)}x{len(maze[0])} maze")

# Test DFS algorithm
print("Testing DFS...")
gen.current_algo_idx = 1  # DFS
gen.config['SEED'] = 43
maze = gen.generate_maze()
print(f"✓ Generated {len(maze)}x{len(maze[0])} maze")
```

### 2. Testing Pattern Colors

```python
from src.mazegen.generator import MazeGenerator

gen = MazeGenerator('config/default_config.txt', size=(10, 8))
gen.generate_maze()

# Test all pattern colors
pattern_colors = ["default", "magenta", "cyan", "red", "yellow", "white"]
for color in pattern_colors:
    gen.generator.pattern_color_scheme = color
    output = gen.generator.render_frame_simple(gen.generator.get_frame_count()-1)
    print(f"✓ Pattern color '{color}' rendered successfully")
```

### 3. Testing Wall Color Schemes

```python
from src.mazegen.generator import MazeGenerator

gen = MazeGenerator('config/default_config.txt', size=(10, 8))
gen.generate_maze()

# Test all color schemes
color_schemes = ["default", "emerald", "ocean", "amber"]
for scheme in color_schemes:
    gen.generator.color_scheme = scheme
    output = gen.generator.render_frame_simple(gen.generator.get_frame_count()-1)
    print(f"✓ Color scheme '{scheme}' rendered successfully")
```

### 4. Testing Path Visualization

```python
from src.mazegen.generator import MazeGenerator

gen = MazeGenerator('config/default_config.txt', size=(10, 8))
gen.generate_maze()

# Test path display
print("Testing path visualization...")
gen.generator.show_path = False
output1 = gen.generator.render_frame_simple(gen.generator.get_frame_count()-1)
print("✓ Maze without path")

gen.generator.show_path = True
output2 = gen.generator.render_frame_simple(gen.generator.get_frame_count()-1)
print("✓ Maze with path")

assert output1 != output2, "Path display should change output"
```

### 5. Testing Animation Frames

```python
from src.mazegen.internal.maze_with_animation import MazeGeneratorWithAnimation

gen = MazeGeneratorWithAnimation(10, 8, seed=42)
maze = gen.generate('prim')

print(f"Total frames captured: {gen.get_frame_count()}")
print(f"✓ Animation frames: {gen.get_frame_count()} frames")

# Render each frame
for i in range(gen.get_frame_count()):
    frame_output = gen.render_frame_simple(i)
    print(f"✓ Frame {i+1} rendered")
```

## Testing New Features

### Testing the Unified Base Classes

```python
from src.mazegen.internal.maze_base import Cell, MazeGeneratorBase

# Test Cell class
print("Testing Cell class...")
cell = Cell(0, 0)
assert cell.walls == 15, "All walls should be present initially"
assert cell.has_wall('N'), "Should have north wall"
assert cell.has_wall('E'), "Should have east wall"

cell.remove_wall('N')
assert not cell.has_wall('N'), "North wall should be removed"
assert cell.walls == 14, "Walls should be 14 after removing north"
print("✓ Cell class working correctly")

# Test MazeGeneratorBase with pattern cells
pattern_cells = {(1, 1), (2, 2)}
class TestGenerator(MazeGeneratorBase):
    def generate(self):
        return self.grid

gen = TestGenerator(5, 5, seed=42, pattern_cells=pattern_cells)
for x, y in pattern_cells:
    assert gen.grid[y][x].visited, f"Pattern cell ({x}, {y}) should be visited"
print("✓ Pattern cell protection working")
```

### Testing Prim's Algorithm

```python
from src.mazegen.internal.maze_generator_prim import PrimMazeGenerator

print("Testing Prim's algorithm...")
gen = PrimMazeGenerator(10, 10, seed=42)
maze = gen.generate()

# Check maze is generated
assert maze is not None, "Maze should be generated"
assert len(maze) == 10, "Should have 10 rows"
assert len(maze[0]) == 10, "Should have 10 columns"

# Check all cells are visited
for row in maze:
    for cell in row:
        assert cell.visited, "All cells should be visited after generation"

print("✓ Prim's algorithm working correctly")
```

### Testing DFS Algorithm

```python
from src.mazegen.internal.maze_generator_dfs import DFSMazeGenerator

print("Testing DFS algorithm...")
gen = DFSMazeGenerator(10, 10, seed=42)
maze = gen.generate()

# Check maze is generated
assert maze is not None, "Maze should be generated"
assert len(maze) == 10, "Should have 10 rows"
assert len(maze[0]) == 10, "Should have 10 columns"

# Check all cells are visited
for row in maze:
    for cell in row:
        assert cell.visited, "All cells should be visited after generation"

print("✓ DFS algorithm working correctly")
```

### Testing Pattern Protection

```python
from src.mazegen.internal.maze_generator_prim import PrimMazeGenerator
from src.mazegen.internal.maze_generator_dfs import DFSMazeGenerator

pattern_cells = {(2, 2), (2, 3), (3, 3)}

# Test with Prim's
print("Testing pattern protection with Prim's...")
gen_prim = PrimMazeGenerator(6, 6, seed=42, pattern_cells=pattern_cells)
maze = gen_prim.generate()
for x, y in pattern_cells:
    assert maze[y][x].visited, f"Pattern cell ({x}, {y}) should remain protected"
print("✓ Prim's respects pattern cells")

# Test with DFS
print("Testing pattern protection with DFS...")
gen_dfs = DFSMazeGenerator(6, 6, seed=42, pattern_cells=pattern_cells)
maze = gen_dfs.generate()
for x, y in pattern_cells:
    assert maze[y][x].visited, f"Pattern cell ({x}, {y}) should remain protected"
print("✓ DFS respects pattern cells")
```

## Writing New Tests

### Test File Structure

Create test files in the `tests/` directory following this pattern:

```python
# tests/test_feature.py
"""Test suite for [feature description]."""

import pytest
from src.mazegen.internal.module_name import ClassName


class TestClassName:
    """Test cases for ClassName."""
    
    def test_basic_functionality(self):
        """Test basic functionality works."""
        obj = ClassName()
        result = obj.method()
        assert result is not None
    
    def test_edge_case(self):
        """Test edge cases are handled."""
        obj = ClassName()
        # Test edge case
        pass


def test_standalone_function():
    """Test standalone function."""
    result = function_call()
    assert result == expected_value
```

### Running Your New Tests

```bash
# Run your new test file
pytest tests/test_feature.py -v

# Run with coverage
pytest tests/test_feature.py --cov=src.mazegen.internal.module_name -v
```

## Common Testing Patterns

### Testing Maze Generation

```python
def test_maze_generation():
    """Test that maze generates correctly."""
    from src.mazegen.internal.maze_generator_prim import PrimMazeGenerator
    
    gen = PrimMazeGenerator(5, 5, seed=42)
    maze = gen.generate()
    
    # Check dimensions
    assert len(maze) == 5
    assert len(maze[0]) == 5
    
    # Check all cells visited
    for row in maze:
        for cell in row:
            assert cell.visited
```

### Testing Animation

```python
def test_animation_frames():
    """Test that animation frames are captured."""
    from src.mazegen.internal.maze_with_animation import MazeGeneratorWithAnimation
    
    gen = MazeGeneratorWithAnimation(5, 5, seed=42)
    maze = gen.generate('prim')
    
    # Check frames were captured
    assert gen.get_frame_count() > 0
    
    # Check frames can be rendered
    for i in range(gen.get_frame_count()):
        output = gen.render_frame_simple(i)
        assert len(output) > 0
```

### Testing Colors

```python
def test_color_schemes():
    """Test that color schemes work."""
    from src.mazegen.generator import MazeGenerator
    
    gen = MazeGenerator('config/default_config.txt', size=(5, 5))
    gen.generate_maze()
    
    schemes = ["default", "emerald", "ocean", "amber"]
    for scheme in schemes:
        gen.generator.color_scheme = scheme
        output = gen.generator.render_frame_simple(gen.generator.get_frame_count()-1)
        assert len(output) > 0
```

## Debugging Tips

### Print Debug Information

```python
# Enable verbose output
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug prints in your code
print(f"Debug: Variable = {variable}")
```

### Use Python Debugger

```bash
# Run with debugger
python3 -m pdb a_maze_ing.py config/default_config.txt

# Or add breakpoint in code
breakpoint()  # Python 3.7+
```

### Test with Different Seeds

```python
# Test reproducibility with same seed
gen1 = MazeGenerator('config/default_config.txt', size=(10, 8), seed=42)
maze1 = gen1.generate_maze()

gen2 = MazeGenerator('config/default_config.txt', size=(10, 8), seed=42)
maze2 = gen2.generate_maze()

# Should generate identical mazes
assert maze1 == maze2, "Same seed should produce same maze"
```

## Continuous Integration

To run tests automatically on each commit, ensure:

1. Tests pass locally: `make test`
2. Linting passes: `make lint`
3. Code coverage is acceptable: `pytest --cov=src tests/`

## Troubleshooting

### Import Errors

```python
# If you get import errors, check your Python path
import sys
sys.path.insert(0, '/home/runner/work/A-Maze-Ing/A-Maze-Ing')
```

### Test Failures

```bash
# Run with verbose output to see details
pytest tests/ -vv

# Run specific test with print statements
pytest tests/test_file.py::test_function -v -s
```

## Additional Resources

- **Internal README**: See `src/mazegen/internal/README.md` for module documentation
- **Refactoring Summary**: See `REFACTORING_SUMMARY.md` for architecture details
- **Main README**: See `README.md` for general project information

## Example: Complete Test Session

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run existing tests
make test

# 3. Test manually
python3 -c "
from src.mazegen.generator import MazeGenerator
gen = MazeGenerator('config/default_config.txt', size=(10, 8))
gen.generate_maze()
print('✓ Maze generated successfully')
"

# 4. Test both algorithms
python3 tests/test_both_algorithms.py

# 5. Run the interactive application
python3 a_maze_ing.py config/default_config.txt
# Try menu options: 1 (regenerate), 3 (colors), 4 (pattern colors), 5 (quit)
```

## Summary

The new features can be tested at multiple levels:
- **Unit tests**: Individual components (Cell, algorithms)
- **Integration tests**: Combined features (animation with algorithms)
- **Manual tests**: Interactive application testing
- **Visual tests**: Check colors and rendering

Always test both Prim's and DFS algorithms, verify pattern protection, and check that all color schemes work correctly.
