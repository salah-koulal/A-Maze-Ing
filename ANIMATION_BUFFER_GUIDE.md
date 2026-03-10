# Animation Buffer Guide: How We Fill and Display Animation Frames

This document explains how the A-Maze-Ing project handles animation buffers and frame rendering.

## Overview

The project has **two animation approaches**:

1. **Frame-Capture Approach** (older, in `maze_with_animation.py`)
2. **Real-Time Rendering Approach** (current, in `maze_animator.py` + `frame_renderer.py`)

Both serve different purposes and use different buffering strategies.

---

## Approach 1: Frame-Capture Animation Buffer

**Location**: `src/mazegen/internal/maze_with_animation.py`

### How It Works

This approach **captures and stores** animation frames during maze generation, then **replays** them later.

### Key Components

#### 1. AnimationFrame Data Structure
```python
@dataclass
class AnimationFrame:
    grid_state: List[List[int]]  # Wall state for each cell
    visited_cells: Set[Tuple[int, int]]  # Cells visited
    pattern_cells: Set[Tuple[int, int]]  # Pattern cells ("42")
    current_cell: Tuple[int, int] | None  # Active cell
    description: str  # Frame description
```

#### 2. Frame Buffer (List of Frames)
```python
self.frames: List[AnimationFrame] = []
```

This list stores **all captured frames** during generation.

### How the Buffer is Filled

**Step 1: Initialization**
```python
def generate(self, algorithm: str = "prim") -> List[List[Any]]:
    self.frames = []  # Clear previous frames
    
    # Create generator
    generator = PrimMazeGenerator(self.width, self.height, self.seed, self.pattern_cells)
    
    # Capture initial state
    self._capture_frame(generator, "Prim's: Initial state")
```

**Step 2: Capture During Generation**
```python
def _capture_frame(self, generator: Any, description: str, current_pos: Tuple[int, int] | None = None) -> None:
    # Read current grid state
    grid_state = [[cell.walls for cell in row] for row in generator.grid]
    
    # Collect visited cells
    visited = {(cell.x, cell.y) for row in generator.grid 
              for cell in row if cell.visited}
    
    # Create frame snapshot
    frame = AnimationFrame(
        grid_state=grid_state,
        visited_cells=visited,
        pattern_cells=self.pattern_cells,
        current_cell=current_pos,
        description=description
    )
    
    # ADD TO BUFFER
    self.frames.append(frame)
```

**Step 3: Generation with Periodic Captures**
```python
# During maze generation, capture frames at key points:
generator.generate()  # Generate maze
self._capture_frame(generator, "Generation complete")

# Capture during wall removal
if removed % 5 == 0:
    self._capture_frame(generator, f"Removed {removed} extra walls")
```

### How Frames are Played Back

**Replay from Buffer**:
```python
def play_animation(self, fps: float = 15.0) -> None:
    delay = 1.0 / fps
    
    # Loop through stored frames
    for i in range(len(self.frames)):
        print("\033[2J\033[H", end="")  # Clear screen
        print(self.render_frame_simple(i))  # Render frame i
        time.sleep(delay)
```

**Rendering a Single Frame**:
```python
def render_frame_simple(self, index: int) -> str:
    frame = self.frames[index]  # Get frame from buffer
    
    # Create display grid
    grid_display = [[" " for _ in range(self.width * 2 + 1)] 
                   for _ in range(self.height * 2 + 1)]
    
    # Fill display grid from frame data
    for y in range(self.height):
        for x in range(self.width):
            walls = frame.grid_state[y][x]
            # Draw walls based on frame's grid_state
            if walls & 1:  # North wall
                grid_display[gy-1][gx] = WC
            # ... etc
    
    return "\n".join(["".join(row) for row in grid_display])
```

### Advantages
- ✅ Can replay animation multiple times
- ✅ Can pause, rewind, or step through frames
- ✅ Frame data can be saved to disk
- ✅ Good for debugging and analysis

### Disadvantages
- ❌ High memory usage (stores every frame)
- ❌ Two-pass process (generate, then display)
- ❌ Not real-time

---

## Approach 2: Real-Time Rendering with Screen Buffer

**Location**: `src/frame_renderer.py`, `src/screen_buffer.py`, `src/maze_animator.py`

### How It Works

This approach **renders directly** during generation using a **reusable screen buffer**. No frame history is kept.

### Key Components

#### 1. ScreenBuffer (2D Character Array)
```python
class ScreenBuffer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # 2D array to store characters
        self.buffer = []
        for y in range(height):
            row = [' '] * width
            self.buffer.append(row)
```

This is a **single buffer** that gets **overwritten** each frame.

#### 2. FrameRenderer
```python
class FrameRenderer:
    def __init__(self, maze_generator):
        # Calculate screen size
        screen_width = self.width * 4 + 1
        screen_height = self.height * 2 + 1
        
        # Create ONE buffer for rendering
        self.buffer = ScreenBuffer(screen_width, screen_height)
```

### How the Buffer is Filled and Displayed

**Step 1: Rendering to Buffer**
```python
def render_full(self, current_cell=None, show_visited=True):
    # CLEAR buffer (reuse same memory)
    self.buffer.clear()
    
    # FILL buffer with current maze state
    for y in range(self.height + 1):
        for x in range(self.width):
            # Get corner character
            corner_char = self.get_corner_char(x, y)
            
            # WRITE to buffer
            sx, sy = self.mapper.corner_to_screen(x, y)
            self.buffer.set_char(sx, sy, corner_char)
            
            # Draw horizontal walls
            wx, wy = self.mapper.wall_north_to_screen(x, y)
            if self.grid[y][x].has_wall('N'):
                self.buffer.set_string(wx, wy, "═══")
    
    # Draw cell contents
    for y in range(self.height):
        for x in range(self.width):
            cell = self.grid[y][x]
            cx, cy = self.mapper.cell_to_screen(x, y)
            
            # Write cell content to buffer
            if not cell.enabled:
                self.buffer.set_string(cx, cy, "███")
            elif current_cell and (x, y) == (current_cell.x, current_cell.y):
                self.buffer.set_string(cx, cy, "■■■")
            elif cell.visited:
                self.buffer.set_string(cx, cy, " · ")
```

**Step 2: Buffer Operations**
```python
def set_char(self, x, y, char):
    """Write single character to buffer."""
    if 0 <= y < self.height and 0 <= x < self.width:
        self.buffer[y][x] = char

def set_string(self, x, y, string):
    """Write string starting at position."""
    for i in range(len(string)):
        self.set_char(x + i, y, string[i])

def get_char(self, x, y):
    """Read character from buffer."""
    if 0 <= y < self.height and 0 <= x < self.width:
        return self.buffer[y][x]
    return ' '
```

**Step 3: Display Buffer to Screen**
```python
def display(self):
    """Output buffer contents to terminal."""
    for y in range(self.buffer.height):
        move_cursor(1, y + 1)  # Position cursor
        
        line = ""
        for x in range(self.buffer.width):
            char = self.buffer.get_char(x, y)  # READ from buffer
            
            # Apply colors
            if char != ' ' and char != '·':
                set_fg(r, g, b)
                line += char
                reset_color()
            else:
                line += char
        
        print(line, end='', flush=True)  # OUTPUT to terminal
```

**Step 4: Animation Loop**
```python
def animate_generation(self, start_x=0, start_y=0, delay=0.05):
    # Initial render
    self.renderer.render_full(show_visited=False)
    self.renderer.display()
    
    # Generation loop
    while len(stack) > 0:
        current = stack[-1]
        # ... maze generation logic ...
        
        # Render CURRENT state (overwrites buffer)
        self.renderer.render_full(current_cell=current, show_visited=True)
        self.renderer.display()  # Show to screen
        
        time.sleep(delay)  # Animate
    
    # Final render
    self.renderer.render_full(show_visited=True)
    self.renderer.display()
```

### Buffer Lifecycle

```
┌─────────────────────────────────────────────────┐
│ 1. Create ScreenBuffer (allocate 2D array)     │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 2. Clear buffer (fill with spaces)             │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 3. Render: Fill buffer with maze characters    │
│    - set_char() writes characters               │
│    - set_string() writes strings                │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 4. Display: Read buffer and print to screen    │
│    - get_char() reads each position             │
│    - print() outputs to terminal                │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 5. Loop: Clear and repeat for next frame       │
│    (reuse same buffer memory)                   │
└─────────────────────────────────────────────────┘
```

### Advantages
- ✅ Low memory usage (only current frame)
- ✅ Real-time rendering
- ✅ Immediate visual feedback
- ✅ Simple and efficient

### Disadvantages
- ❌ Cannot replay (no history)
- ❌ Cannot pause or rewind
- ❌ Frame data not saved

---

## Comparison

| Feature | Frame-Capture | Real-Time Rendering |
|---------|--------------|---------------------|
| **Memory Usage** | High (stores all frames) | Low (single buffer) |
| **Speed** | Two-pass | Single-pass |
| **Replay** | ✅ Yes | ❌ No |
| **Real-time** | ❌ No | ✅ Yes |
| **Implementation** | `maze_with_animation.py` | `maze_animator.py` + `frame_renderer.py` |
| **Buffer Type** | List of AnimationFrame objects | Single ScreenBuffer (2D array) |
| **Current Status** | Legacy (still available) | Primary method |

---

## Code Examples

### Example 1: Using Frame-Capture Animation

```python
from src.mazegen.internal.maze_with_animation import MazeGeneratorWithAnimation

# Create generator
gen = MazeGeneratorWithAnimation(width=10, height=8)

# Generate maze (fills frame buffer)
maze = gen.generate(algorithm="prim")

# Check how many frames were captured
print(f"Captured {gen.get_frame_count()} frames")

# Play animation (replay from buffer)
gen.play_animation(fps=15)

# Access individual frames
frame_5 = gen.frames[5]
print(f"Frame 5: {frame_5.description}")
print(f"Visited cells: {len(frame_5.visited_cells)}")
```

### Example 2: Using Real-Time Rendering

```python
from src.animatable_maze_adapter import AnimatableMazeGenerator
from src.maze_animator_prim import PrimMazeAnimator

# Create generator
gen = AnimatableMazeGenerator('prim', width=10, height=8)

# Create animator with renderer
animator = PrimMazeAnimator(gen)

# Animate (renders in real-time, no buffering)
animator.animate_generation(delay=0.05)

# After animation, can re-render final state
animator.renderer.render_full(show_visited=True)
animator.renderer.display()
```

---

## Technical Details

### ScreenBuffer Memory Layout

```
For a 6x4 maze:
- Maze cells: 6 columns × 4 rows
- Screen buffer: (6 * 4 + 1) × (4 * 2 + 1) = 25 × 9 characters

Buffer structure (2D array):
buffer[0] = [' ', '╔', '═', '═', '═', '╦', ...]  # Row 0
buffer[1] = [' ', '║', ' ', ' ', ' ', '║', ...]  # Row 1
buffer[2] = [' ', '╠', '═', '═', '═', '╬', ...]  # Row 2
...

Each cell occupies 4×2 character positions plus borders.
```

### AnimationFrame Memory Layout

```
For a 6x4 maze, each frame stores:

frame = AnimationFrame(
    grid_state=[
        [15, 7, 11, ...],  # Row 0: walls as integers (4 bits each)
        [13, 5, 9, ...],   # Row 1
        ...
    ],
    visited_cells={(0,0), (1,0), (0,1), ...},  # Set of tuples
    pattern_cells={(3,2), (4,2)},              # Set of tuples
    current_cell=(2, 1),                        # Single tuple
    description="Step 15: Exploring..."        # String
)

Approximate memory per frame: ~500 bytes for small maze
For 100 frames: ~50 KB
```

---

## Summary

**Question: "How did we fill the animation buffer to print them again?"**

**Answer**:

1. **Frame-Capture Approach** (`maze_with_animation.py`):
   - During generation, we call `_capture_frame()` at key moments
   - Each call creates an `AnimationFrame` object with current state
   - Frames are appended to `self.frames` list (the "buffer")
   - Later, `play_animation()` loops through the list and renders each frame
   - This is how we "fill the buffer" and "print them again"

2. **Real-Time Rendering** (`maze_animator.py`):
   - Uses a single `ScreenBuffer` (2D character array)
   - During generation loop, we call `render_full()` to fill buffer
   - Then call `display()` to print buffer contents
   - Buffer is cleared and refilled each iteration
   - No frame history - we render directly, not "print them again"

The current implementation primarily uses **real-time rendering**, but the **frame-capture** approach is still available in the codebase for use cases that require frame history (debugging, analysis, creating GIFs, etc.).
