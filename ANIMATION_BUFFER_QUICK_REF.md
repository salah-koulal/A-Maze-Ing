# Animation Buffer Quick Reference

## Question: "How did we fill the animation buffer to print them again?"

## Short Answer

The project has **two animation approaches** with different buffer mechanisms:

### 1. Frame-Capture Animation (can replay)
**Location**: `src/mazegen/internal/maze_with_animation.py`

```python
# HOW WE FILL THE BUFFER:
def _capture_frame(self, generator, description, current_pos):
    frame = AnimationFrame(...)  # Create snapshot
    self.frames.append(frame)     # Add to buffer list

# HOW WE PRINT THEM AGAIN:
def play_animation(self, fps=15):
    for i in range(len(self.frames)):  # Loop through buffer
        print(self.render_frame_simple(i))  # Print each frame
```

### 2. Real-Time Rendering (no replay)
**Location**: `src/frame_renderer.py`, `src/screen_buffer.py`

```python
# HOW WE FILL THE BUFFER:
def render_full(self, current_cell=None):
    self.buffer.clear()              # Clear 2D array
    self.buffer.set_char(x, y, char) # Write characters
    self.buffer.set_string(x, y, str)# Write strings

# HOW WE PRINT:
def display(self):
    for y in range(self.buffer.height):
        for x in range(self.buffer.width):
            char = self.buffer.get_char(x, y)  # Read from buffer
            print(char)                         # Print to screen
```

## Key Differences

| Aspect | Frame-Capture | Real-Time |
|--------|--------------|-----------|
| **Buffer Type** | List of AnimationFrame objects | Single ScreenBuffer (2D array) |
| **Filling** | Append snapshots to list | Write chars to array |
| **Printing** | Loop list and render each | Read array and print once |
| **Replay** | ✓ Yes (loop through list again) | ✗ No (buffer overwritten) |
| **Memory** | High (~500 bytes/frame) | Low (~2-3 KB constant) |

## When to Use Each

**Use Frame-Capture when:**
- Need to replay animation
- Need to save/export animation
- Debugging generation process
- Creating GIFs or videos

**Use Real-Time when:**
- Live animation only
- Memory constrained
- Performance critical
- Current display state sufficient

## Code Locations

### Frame-Capture
- `src/mazegen/internal/maze_with_animation.py`
  - `self.frames` = buffer (list)
  - `_capture_frame()` = fill buffer
  - `play_animation()` = print buffer

### Real-Time
- `src/screen_buffer.py`
  - `self.buffer` = 2D array
  - `set_char()`, `set_string()` = fill buffer
  - `get_char()` = read buffer
- `src/frame_renderer.py`
  - `render_full()` = fill buffer
  - `display()` = print buffer
- `src/maze_animator.py`
  - Animation loop using renderer

## Example Usage

### Frame-Capture
```python
from src.mazegen.internal.maze_with_animation import MazeGeneratorWithAnimation

gen = MazeGeneratorWithAnimation(width=10, height=8)
maze = gen.generate(algorithm="prim")  # Fills buffer

print(f"Captured {gen.get_frame_count()} frames")
gen.play_animation(fps=15)  # Print buffer (replay)
```

### Real-Time
```python
from src.animatable_maze_adapter import AnimatableMazeGenerator
from src.maze_animator_prim import PrimMazeAnimator

gen = AnimatableMazeGenerator('prim', width=10, height=8)
animator = PrimMazeAnimator(gen)

# Fills and prints buffer in real-time (no replay)
animator.animate_generation(delay=0.05)
```

## See Also

- **Full Documentation**: `ANIMATION_BUFFER_GUIDE.md`
- **Demo Script**: `examples/animation_buffer_demo.py`
- **Code Comments**: Enhanced in all animation-related files
