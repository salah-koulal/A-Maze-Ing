# How to Test New Features

## Quick Start (Choose One)

### 1. 🚀 Fastest: Quick Test Script
```bash
python3 tests/quick_test.py
```
Runs in ~5 seconds, shows visual output, tests all features.

### 2. 🧪 Complete: Pytest Suite
```bash
pytest tests/ -v
```
Runs 54 automated tests covering all features.

### 3. 🎮 Interactive: Run the Application
```bash
python3 a_maze_ing.py config/default_config.txt
```
Test features manually through the interactive menu.

### 4. 💻 Developer: Python REPL
```bash
python3
>>> from src.mazegen.generator import MazeGenerator
>>> gen = MazeGenerator('config/default_config.txt', size=(10, 8))
>>> gen.generate_maze()
```

## What Can You Test?

### ✓ Unified Base Classes
- **Cell** class: Wall manipulation, initialization
- **MazeGeneratorBase**: Grid setup, pattern protection

```python
from src.mazegen.internal.maze_base import Cell
cell = Cell(0, 0)
cell.remove_wall('N')
assert not cell.has_wall('N')
```

### ✓ Maze Algorithms
- **Prim's Algorithm**: Frontier-based, complex mazes
- **DFS Algorithm**: Recursive backtracker, long corridors

```python
from src.mazegen.internal.maze_generator_prim import PrimMazeGenerator
from src.mazegen.internal.maze_generator_dfs import DFSMazeGenerator

prim = PrimMazeGenerator(10, 10, seed=42)
prim_maze = prim.generate()

dfs = DFSMazeGenerator(10, 10, seed=42)
dfs_maze = dfs.generate()
```

### ✓ Animation System
- Frame capture during generation
- Both algorithms use same system

```python
from src.mazegen.internal.maze_with_animation import MazeGeneratorWithAnimation

gen = MazeGeneratorWithAnimation(10, 8, seed=42)
maze = gen.generate('prim')  # or 'dfs'
print(f"Captured {gen.get_frame_count()} frames")
```

### ✓ Color Schemes
- **4 Wall Colors**: default, emerald, ocean, amber
- **6 Pattern Colors**: default, magenta, cyan, red, yellow, white

```python
from src.mazegen.generator import MazeGenerator

gen = MazeGenerator('config/default_config.txt', size=(10, 8))
gen.generate_maze()

# Test wall colors
gen.generator.color_scheme = "emerald"

# Test pattern colors
gen.generator.pattern_color_scheme = "magenta"
```

### ✓ Pattern Protection
The "42" pattern is automatically protected during generation.

```python
pattern_cells = {(2, 2), (3, 2), (4, 2)}
gen = PrimMazeGenerator(10, 8, seed=42, pattern_cells=pattern_cells)
maze = gen.generate()
# Pattern cells remain protected
```

## Test Results

### Quick Test Output
```
======================================================================
  Testing Base Classes
======================================================================
✓ Cell class working
✓ Wall manipulation working

======================================================================
  Testing Maze Generation Algorithms
======================================================================
✓ Generated 8x10 maze with Prim's
✓ Generated 8x10 maze with DFS
✓ Pattern cells protected

✅ ALL TESTS PASSED!
```

### Pytest Output
```bash
$ pytest tests/ -v

tests/test_maze_base.py::TestCell .................. PASSED [  35%]
tests/test_algorithms.py::TestPrim ................ PASSED [  70%]
tests/test_animation.py::TestAnimation ............ PASSED [ 100%]

======================== 54 passed in 0.12s =======================
```

## Documentation

- **`TESTING_GUIDE.md`**: Complete testing guide with examples
- **`src/mazegen/internal/README.md`**: Architecture and usage docs
- **`REFACTORING_SUMMARY.md`**: What changed and why

## Interactive Testing

Run the application and use the menu:
1. **[1]** Regenerate maze → Cycles between Prim's and DFS
2. **[2]** Show/hide path → Toggle solution path
3. **[3]** Change wall colors → Cycle through 4 schemes
4. **[4]** Change pattern colors → Cycle through 6 colors
5. **[5]** Quit

## Need Help?

1. Read `TESTING_GUIDE.md` for detailed examples
2. Run `python3 tests/quick_test.py` to verify everything works
3. Check test files in `tests/` for more examples

## Summary

| Method | Time | Output | Best For |
|--------|------|--------|----------|
| quick_test.py | 5s | Visual | Quick verification |
| pytest | 0.12s | Pass/Fail | Automated testing |
| Interactive | Manual | Live demo | Feature showcase |
| Python REPL | Manual | Custom | Development |

**Recommended Start**: `python3 tests/quick_test.py` 🚀
