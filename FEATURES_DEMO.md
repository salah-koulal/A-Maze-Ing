# Color Schemes and Path Visualization Features

## Overview

This implementation adds two key interactive features to the maze generator:
1. **Color Scheme Selection**: Cycle through 7 different wall colors
2. **Path Visualization**: Toggle the display of the solution path from entry to exit

## Visual Demonstrations

### Example 1: Default Color, No Path
```
╔═══╦═══════════════════╗
║ S ║███ ███ ███ ███ ███║
║   ║   ════════════╦═══╣
║███ ███ ███ ███ ███║███║
╠════════   ════╦═══╣   ║
║███ ███ ███ ███║███║███║
║   ╔════   ════╝   ║   ║
║███║███ ███ ███ ███ ███║
╠═══╝   ════╗   ║   ════╣
║███ ███ ███║███║███  E ║
╚═══════════╩═══╩═══════╝
```

### Example 2: Colored Walls with Path Visible
```
╔═══╦═══════════════════╗    (walls in blue/green/red/etc.)
║ S ║███ ███ ███ ███ ███║
║   ║   ════════════╦═══╣
║ ◦   ◦   ◦  ███ ███║███║    ◦ = Path cells
╠════════   ════╦═══╣   ║
║███ ███  ◦  ███║███║███║
║   ╔════   ════╝   ║   ║
║███║███  ◦   ◦   ◦  ███║
╠═══╝   ════╗   ║   ════╣
║███ ███ ███║███║ ◦   E ║    E = Exit
╚═══════════╩═══╩═══════╝
```

## Features

### 1. Color Schemes
Seven color options for maze walls:
- **default**: White (255, 255, 255)
- **blue**: Light blue (100, 150, 255)
- **green**: Light green (100, 255, 150)
- **red**: Light red (255, 100, 100)
- **yellow**: Yellow (255, 255, 100)
- **magenta**: Magenta (255, 100, 255)
- **cyan**: Cyan (100, 255, 255)

Colors are applied using ANSI RGB terminal control codes for true color support.

### 2. Path Visualization
When enabled, the path from entry to exit is displayed with:
- **S**: Start/Entry marker
- **E**: End/Exit marker
- **◦**: Path cell marker

The path is computed using BFS (Breadth-First Search) to find the shortest route.

### 3. Pattern Cells
The "42" pattern remains visible as solid blocks (███) and is protected from both the maze generation algorithm and path visualization.

## Interactive Menu

The enhanced menu provides:
```
choices :

1 regenerate new maze (Next: Prim's/DFS)
2 show current maze
3 change maze wall colors
4 show/hide path from entry to exit
5 quit
```

### Usage Examples

**Changing colors:**
- Select option 3
- Cycles through: default → blue → green → red → yellow → magenta → cyan → default
- Maze re-renders immediately with new color

**Toggling path:**
- Select option 4
- Toggles between visible and hidden
- Maze re-renders immediately with/without path

## Technical Implementation

### FrameRenderer Enhancements
```python
# Color scheme system
self.color_schemes = {
    "default": (255, 255, 255),
    "blue": (100, 150, 255),
    # ... more colors
}

# Path visualization
def set_path_info(self, path_str: str, entry: tuple, exit: tuple):
    """Set path information for visualization."""
    # Computes all cells on the path from entry to exit
    
def display(self):
    """Display with colors using RGB terminal codes."""
    # Applies colors using set_fg(r, g, b)
```

### MazeGenerator Integration
```python
# Color management
self.color_schemes = ["default", "blue", "green", ...]
self.current_color_idx = 0

# Path management
self.show_path = False
self.last_path = ""

# Applied to renderer after generation
animator.renderer.color_scheme = self.color_schemes[self.current_color_idx]
animator.renderer.show_path = self.show_path
```

## Benefits

1. **Enhanced Visual Experience**: Multiple color options make the maze more visually appealing
2. **Educational Value**: Seeing the solution path helps understand maze structure
3. **Interactive Control**: Users can customize the display to their preference
4. **Preserved Animation**: All features work seamlessly with the real-time maze generation animation

## Compatibility

- Works with both Prim's and DFS algorithms
- Compatible with pattern embedding ("42")
- Maintains all existing features (regeneration, file output, etc.)
- Uses standard ANSI terminal codes for wide compatibility
