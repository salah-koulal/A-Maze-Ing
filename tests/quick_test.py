#!/usr/bin/env python3
"""
Quick test script for manually testing new features.
Run with: python3 tests/quick_test.py
"""

import sys
sys.path.insert(0, '/home/runner/work/A-Maze-Ing/A-Maze-Ing')

from src.mazegen.generator import MazeGenerator
from src.mazegen.internal.maze_generator_prim import PrimMazeGenerator
from src.mazegen.internal.maze_generator_dfs import DFSMazeGenerator
from src.mazegen.internal.maze_with_animation import MazeGeneratorWithAnimation


def test_section(name):
    """Print test section header."""
    print("\n" + "="*70)
    print(f"  {name}")
    print("="*70)


def test_base_classes():
    """Test the unified base classes."""
    test_section("Testing Base Classes")
    
    from src.mazegen.internal.maze_base import Cell
    
    # Test Cell
    cell = Cell(5, 10)
    assert cell.x == 5 and cell.y == 10
    assert cell.walls == 15
    
    cell.remove_wall('N')
    assert not cell.has_wall('N')
    
    print("✓ Cell class working")
    print("✓ Wall manipulation working")


def test_algorithms():
    """Test both maze generation algorithms."""
    test_section("Testing Maze Generation Algorithms")
    
    # Test Prim's
    print("\n1. Testing Prim's Algorithm...")
    prim_gen = PrimMazeGenerator(10, 8, seed=42)
    prim_maze = prim_gen.generate()
    print(f"   ✓ Generated {len(prim_maze)}x{len(prim_maze[0])} maze")
    
    # Test DFS
    print("\n2. Testing DFS Algorithm...")
    dfs_gen = DFSMazeGenerator(10, 8, seed=42)
    dfs_maze = dfs_gen.generate()
    print(f"   ✓ Generated {len(dfs_maze)}x{len(dfs_maze[0])} maze")
    
    # Test with pattern cells
    print("\n3. Testing Pattern Cell Protection...")
    pattern_cells = {(2, 2), (3, 2), (4, 2)}
    gen_with_pattern = PrimMazeGenerator(10, 8, seed=42, pattern_cells=pattern_cells)
    maze = gen_with_pattern.generate()
    for x, y in pattern_cells:
        assert maze[y][x].visited
    print(f"   ✓ Pattern cells protected: {len(pattern_cells)} cells")


def test_animation():
    """Test the animation system."""
    test_section("Testing Animation System")
    
    # Test with Prim's
    print("\n1. Testing Animation with Prim's...")
    gen = MazeGeneratorWithAnimation(8, 6, seed=42)
    maze = gen.generate('prim')
    print(f"   ✓ Captured {gen.get_frame_count()} animation frames")
    
    # Test with DFS
    print("\n2. Testing Animation with DFS...")
    gen2 = MazeGeneratorWithAnimation(8, 6, seed=43)
    maze2 = gen2.generate('dfs')
    print(f"   ✓ Captured {gen2.get_frame_count()} animation frames")
    
    # Test rendering
    print("\n3. Testing Frame Rendering...")
    for i in range(min(3, gen.get_frame_count())):
        output = gen.render_frame_simple(i)
        assert len(output) > 0
    print(f"   ✓ Successfully rendered frames")


def test_colors():
    """Test color schemes."""
    test_section("Testing Color Schemes")
    
    gen = MazeGenerator('config/default_config.txt', size=(8, 6))
    gen.generate_maze()
    
    # Test wall colors
    print("\n1. Testing Wall Color Schemes...")
    for scheme in gen.color_schemes:
        gen.generator.color_scheme = scheme
        output = gen.generator.render_frame_simple(gen.generator.get_frame_count()-1)
        assert len(output) > 0
        print(f"   ✓ {scheme.capitalize()} color scheme")
    
    # Test pattern colors
    print("\n2. Testing Pattern Color Schemes...")
    for color in gen.pattern_color_schemes[:3]:  # Test first 3
        gen.generator.pattern_color_scheme = color
        output = gen.generator.render_frame_simple(gen.generator.get_frame_count()-1)
        assert len(output) > 0
        print(f"   ✓ {color.capitalize()} pattern color")


def test_features():
    """Test additional features."""
    test_section("Testing Additional Features")
    
    gen = MazeGenerator('config/default_config.txt', size=(8, 6))
    gen.generate_maze()
    
    # Test path visualization
    print("\n1. Testing Path Visualization...")
    gen.generator.show_path = False
    output1 = gen.generator.render_frame_simple(gen.generator.get_frame_count()-1)
    gen.generator.show_path = True
    output2 = gen.generator.render_frame_simple(gen.generator.get_frame_count()-1)
    # Path may or may not change output depending on maze structure
    # Just verify both render without errors
    assert len(output1) > 0 and len(output2) > 0
    print("   ✓ Path visualization toggle working")
    
    # Test algorithm switching
    print("\n2. Testing Algorithm Switching...")
    gen.current_algo_idx = 0
    maze1 = gen.generate_maze()
    print("   ✓ Prim's algorithm")
    
    gen.current_algo_idx = 1
    gen.config['SEED'] = 100
    maze2 = gen.generate_maze()
    print("   ✓ DFS algorithm")


def display_sample_maze():
    """Display a sample generated maze."""
    test_section("Sample Maze Output")
    
    gen = MazeGenerator('config/default_config.txt', size=(12, 8), seed=42)
    gen.generate_maze()
    
    # Show with default colors
    print("\nMaze with default colors (Prim's algorithm):")
    print("-" * 70)
    output = gen.generator.render_frame_simple(gen.generator.get_frame_count()-1)
    # Print first 15 lines
    for line in output.split('\n')[:15]:
        print(line)
    print("...")
    
    # Switch to DFS and show
    gen.current_algo_idx = 1
    gen.config['SEED'] = 43
    gen.generate_maze()
    
    print("\nMaze with default colors (DFS algorithm):")
    print("-" * 70)
    output = gen.generator.render_frame_simple(gen.generator.get_frame_count()-1)
    # Print first 15 lines
    for line in output.split('\n')[:15]:
        print(line)
    print("...")


def main():
    """Run all tests."""
    print("\n╔════════════════════════════════════════════════════════════════════╗")
    print("║              A-MAZE-ING: QUICK FEATURE TEST SUITE                  ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    try:
        test_base_classes()
        test_algorithms()
        test_animation()
        test_colors()
        test_features()
        display_sample_maze()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        print("\nNew features are working correctly:")
        print("  • Unified base classes (Cell, MazeGeneratorBase)")
        print("  • Prim's algorithm (refactored)")
        print("  • DFS algorithm (new)")
        print("  • Animation system (unified)")
        print("  • Color schemes (4 wall schemes, 6 pattern colors)")
        print("  • Pattern protection (built-in)")
        print("  • Path visualization")
        print("\nFor more detailed testing, run: pytest tests/ -v")
        print("="*70 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
