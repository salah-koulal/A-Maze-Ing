"""
Test suite for maze generation algorithms (Prim's and DFS).
"""

import pytest
from src.mazegen.internal.maze_generator_prim import PrimMazeGenerator
from src.mazegen.internal.maze_generator_dfs import DFSMazeGenerator


class TestPrimMazeGenerator:
    """Test cases for Prim's algorithm."""
    
    def test_basic_generation(self):
        """Test basic maze generation with Prim's."""
        gen = PrimMazeGenerator(5, 5, seed=42)
        maze = gen.generate()
        
        assert maze is not None
        assert len(maze) == 5
        assert len(maze[0]) == 5
    
    def test_all_cells_visited(self):
        """Test that all cells are visited after generation."""
        gen = PrimMazeGenerator(8, 6, seed=42)
        maze = gen.generate()
        
        for row in maze:
            for cell in row:
                assert cell.visited, f"Cell ({cell.x}, {cell.y}) not visited"
    
    def test_walls_removed(self):
        """Test that walls are removed during generation."""
        gen = PrimMazeGenerator(5, 5, seed=42)
        maze = gen.generate()
        
        # Count cells with all walls (should be very few or none)
        all_walls_count = sum(1 for row in maze for cell in row if cell.walls == 15)
        assert all_walls_count == 0, "All cells should have some walls removed"
    
    def test_reproducibility(self):
        """Test that same seed produces same maze."""
        gen1 = PrimMazeGenerator(5, 5, seed=100)
        maze1 = gen1.generate()
        
        gen2 = PrimMazeGenerator(5, 5, seed=100)
        maze2 = gen2.generate()
        
        # Compare wall states
        for y in range(5):
            for x in range(5):
                assert maze1[y][x].walls == maze2[y][x].walls, \
                    f"Cell ({x}, {y}) walls differ"
    
    def test_with_pattern_cells(self):
        """Test generation with pattern cells."""
        pattern_cells = {(2, 2), (2, 3), (3, 2)}
        gen = PrimMazeGenerator(6, 6, seed=42, pattern_cells=pattern_cells)
        maze = gen.generate()
        
        # Pattern cells should remain visited
        for x, y in pattern_cells:
            assert maze[y][x].visited
        
        # All other cells should also be visited
        for y in range(6):
            for x in range(6):
                assert maze[y][x].visited
    
    def test_different_sizes(self):
        """Test generation with different maze sizes."""
        sizes = [(3, 3), (10, 5), (5, 10), (15, 15)]
        
        for width, height in sizes:
            gen = PrimMazeGenerator(width, height, seed=42)
            maze = gen.generate()
            assert len(maze) == height
            assert len(maze[0]) == width


class TestDFSMazeGenerator:
    """Test cases for DFS algorithm."""
    
    def test_basic_generation(self):
        """Test basic maze generation with DFS."""
        gen = DFSMazeGenerator(5, 5, seed=42)
        maze = gen.generate()
        
        assert maze is not None
        assert len(maze) == 5
        assert len(maze[0]) == 5
    
    def test_all_cells_visited(self):
        """Test that all cells are visited after generation."""
        gen = DFSMazeGenerator(8, 6, seed=42)
        maze = gen.generate()
        
        for row in maze:
            for cell in row:
                assert cell.visited, f"Cell ({cell.x}, {cell.y}) not visited"
    
    def test_walls_removed(self):
        """Test that walls are removed during generation."""
        gen = DFSMazeGenerator(5, 5, seed=42)
        maze = gen.generate()
        
        # Count cells with all walls (should be none)
        all_walls_count = sum(1 for row in maze for cell in row if cell.walls == 15)
        assert all_walls_count == 0, "All cells should have some walls removed"
    
    def test_reproducibility(self):
        """Test that same seed produces same maze."""
        gen1 = DFSMazeGenerator(5, 5, seed=100)
        maze1 = gen1.generate()
        
        gen2 = DFSMazeGenerator(5, 5, seed=100)
        maze2 = gen2.generate()
        
        # Compare wall states
        for y in range(5):
            for x in range(5):
                assert maze1[y][x].walls == maze2[y][x].walls, \
                    f"Cell ({x}, {y}) walls differ"
    
    def test_with_pattern_cells(self):
        """Test generation with pattern cells."""
        pattern_cells = {(2, 2), (2, 3), (3, 2)}
        gen = DFSMazeGenerator(6, 6, seed=42, pattern_cells=pattern_cells)
        maze = gen.generate()
        
        # Pattern cells should remain visited
        for x, y in pattern_cells:
            assert maze[y][x].visited
        
        # All other cells should also be visited
        for y in range(6):
            for x in range(6):
                assert maze[y][x].visited
    
    def test_different_sizes(self):
        """Test generation with different maze sizes."""
        sizes = [(3, 3), (10, 5), (5, 10), (15, 15)]
        
        for width, height in sizes:
            gen = DFSMazeGenerator(width, height, seed=42)
            maze = gen.generate()
            assert len(maze) == height
            assert len(maze[0]) == width
    
    def test_start_position_override(self):
        """Test that custom start position works."""
        gen = DFSMazeGenerator(5, 5, seed=42)
        maze = gen.generate(start_x=2, start_y=2)
        
        # All cells should still be visited
        for row in maze:
            for cell in row:
                assert cell.visited


class TestAlgorithmComparison:
    """Compare Prim's and DFS algorithms."""
    
    def test_both_generate_valid_mazes(self):
        """Test that both algorithms generate valid mazes."""
        prim_gen = PrimMazeGenerator(10, 10, seed=42)
        dfs_gen = DFSMazeGenerator(10, 10, seed=42)
        
        prim_maze = prim_gen.generate()
        dfs_maze = dfs_gen.generate()
        
        # Both should visit all cells
        for maze in [prim_maze, dfs_maze]:
            for row in maze:
                for cell in row:
                    assert cell.visited
    
    def test_different_maze_structures(self):
        """Test that algorithms produce different structures."""
        prim_gen = PrimMazeGenerator(10, 10, seed=42)
        dfs_gen = DFSMazeGenerator(10, 10, seed=42)
        
        prim_maze = prim_gen.generate()
        dfs_maze = dfs_gen.generate()
        
        # Mazes should be different (count wall differences)
        differences = 0
        for y in range(10):
            for x in range(10):
                if prim_maze[y][x].walls != dfs_maze[y][x].walls:
                    differences += 1
        
        # There should be significant differences
        assert differences > 0, "Algorithms should produce different mazes"
    
    def test_both_respect_pattern_cells(self):
        """Test that both algorithms respect pattern cells."""
        pattern_cells = {(3, 3), (3, 4), (4, 3), (4, 4)}
        
        prim_gen = PrimMazeGenerator(8, 8, seed=42, pattern_cells=pattern_cells)
        dfs_gen = DFSMazeGenerator(8, 8, seed=42, pattern_cells=pattern_cells)
        
        prim_maze = prim_gen.generate()
        dfs_maze = dfs_gen.generate()
        
        # Both should protect pattern cells
        for x, y in pattern_cells:
            assert prim_maze[y][x].visited
            assert dfs_maze[y][x].visited


def test_large_maze_performance():
    """Test that algorithms can handle larger mazes."""
    # This is a simple performance test
    for width, height in [(50, 50), (100, 50)]:
        prim_gen = PrimMazeGenerator(width, height, seed=42)
        prim_maze = prim_gen.generate()
        assert len(prim_maze) == height
        
        dfs_gen = DFSMazeGenerator(width, height, seed=42)
        dfs_maze = dfs_gen.generate()
        assert len(dfs_maze) == height
