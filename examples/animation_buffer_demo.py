#!/usr/bin/env python3
"""
Demonstration of both animation buffer approaches.

This script shows:
1. Frame-Capture Animation (stores frames, can replay)
2. Real-Time Rendering (no storage, immediate display)
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mazegen.internal.maze_with_animation import MazeGeneratorWithAnimation
from animatable_maze_adapter import AnimatableMazeGenerator
from maze_animator_prim import PrimMazeAnimator

print("="*70)
print("ANIMATION BUFFER DEMONSTRATION")
print("="*70)

# ==============================================================================
# APPROACH 1: Frame-Capture Animation
# ==============================================================================
print("\n" + "="*70)
print("APPROACH 1: Frame-Capture Animation")
print("="*70)
print("\nThis approach CAPTURES and STORES frames during generation,")
print("then REPLAYS them later.\n")

# Create generator
print("Step 1: Creating MazeGeneratorWithAnimation...")
gen = MazeGeneratorWithAnimation(width=8, height=6, seed=42)

# Generate maze (this fills the frame buffer)
print("Step 2: Generating maze (filling frame buffer)...")
maze = gen.generate(algorithm="prim")

# Check frame buffer
frame_count = gen.get_frame_count()
print(f"\n✓ Frame buffer filled with {frame_count} frames")
print(f"  Each frame is an AnimationFrame object containing:")
print(f"    - grid_state (wall configuration)")
print(f"    - visited_cells (set of visited coordinates)")
print(f"    - pattern_cells (set of pattern coordinates)")
print(f"    - current_cell (current position)")
print(f"    - description (frame description)")

# Show some frame info
print(f"\n  Frame buffer details:")
for i in [0, frame_count//2, frame_count-1]:
    frame = gen.frames[i]
    print(f"    Frame {i}: {frame.description}")
    print(f"      - Visited cells: {len(frame.visited_cells)}")

print("\nStep 3: Playing animation from buffer...")
print("  (Would call gen.play_animation(fps=15) to replay)")
print("  This loops through self.frames and renders each one.")

# Show final frame rendering
print("\n  Rendering final frame:")
final_frame = gen.render_frame_simple(frame_count - 1)
print(final_frame)

print("\n✓ Approach 1 Complete: Frames captured and can be replayed anytime!")

# ==============================================================================
# APPROACH 2: Real-Time Rendering
# ==============================================================================
print("\n" + "="*70)
print("APPROACH 2: Real-Time Rendering")
print("="*70)
print("\nThis approach renders DIRECTLY during generation using a")
print("REUSABLE screen buffer (no frame history).\n")

# Create generator and animator
print("Step 1: Creating AnimatableMazeGenerator and PrimMazeAnimator...")
gen2 = AnimatableMazeGenerator('prim', width=8, height=6, seed=42)
animator = PrimMazeAnimator(gen2)

print(f"\n  Animator created with:")
print(f"    - FrameRenderer (has ScreenBuffer)")
print(f"    - Buffer size: {animator.renderer.buffer.width} x {animator.renderer.buffer.height}")
print(f"    - Buffer is a 2D array of characters")

print("\nStep 2: How the buffer is filled and displayed:")
print("  1. animator.renderer.render_full() - fills buffer")
print("     - Clears buffer (resets to spaces)")
print("     - Loops through maze grid")
print("     - Writes characters using buffer.set_char()")
print("  2. animator.renderer.display() - prints buffer")
print("     - Loops through buffer")
print("     - Reads characters using buffer.get_char()")
print("     - Prints to terminal")
print("  3. Repeat for each animation frame (buffer is reused)")

# Generate without animation for demo
print("\nStep 3: Generating maze without animation...")
maze2 = gen2.generate_without_animation()

# Render final state
print("\nStep 4: Rendering final state to buffer and displaying...")
animator.renderer.render_full(show_visited=False)
print("  ✓ Buffer filled with maze characters")

print("\n  Final maze (from screen buffer):")
animator.renderer.display()
print("\n")

print("✓ Approach 2 Complete: Rendered in real-time, no frame storage!")

# ==============================================================================
# COMPARISON
# ==============================================================================
print("\n" + "="*70)
print("COMPARISON")
print("="*70)

comparison = """
┌─────────────────────┬──────────────────────┬─────────────────────┐
│ Feature             │ Frame-Capture        │ Real-Time Rendering │
├─────────────────────┼──────────────────────┼─────────────────────┤
│ Memory Usage        │ High (all frames)    │ Low (single buffer) │
│ Can Replay          │ ✓ Yes                │ ✗ No                │
│ Real-Time Display   │ ✗ No (two-pass)      │ ✓ Yes               │
│ Buffer Type         │ List of AnimationFrame│ ScreenBuffer (2D)   │
│ Buffer Size         │ ~500 bytes/frame     │ ~2-3 KB constant    │
│ Primary Use         │ Analysis, replay     │ Live animation      │
│ Implementation      │ maze_with_animation  │ frame_renderer +    │
│                     │                      │ maze_animator       │
└─────────────────────┴──────────────────────┴─────────────────────┘
"""
print(comparison)

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print("""
Frame-Capture Animation:
  • Fills buffer: _capture_frame() adds AnimationFrame to self.frames list
  • Prints buffer: play_animation() loops through self.frames and renders each

Real-Time Rendering:
  • Fills buffer: render_full() writes to ScreenBuffer using set_char()
  • Prints buffer: display() reads from ScreenBuffer using get_char()
  • Buffer is REUSED each frame (cleared and refilled)

Both approaches "fill a buffer", but:
  - Frame-Capture: buffer = list that GROWS (stores history)
  - Real-Time: buffer = fixed 2D array that's REUSED (no history)
""")

print("="*70)
print("See ANIMATION_BUFFER_GUIDE.md for detailed documentation!")
print("="*70)
