"""
Test suite for the unified animation system and high-level generator.
"""

import pytest
from src.mazegen.internal.maze_with_animation import MazeGeneratorWithAnimation
from src.mazegen.generator import MazeGenerator


class TestMazeGeneratorWithAnimation:
    """Test cases for MazeGeneratorWithAnimation."""
    
    def test_basic_initialization(self):
        """Test basic initialization."""
        gen = MazeGeneratorWithAnimation(10, 8, seed=42)
        assert gen.width == 10
        assert gen.height == 8
        assert gen.seed == 42
    
    def test_prim_generation(self):
        """Test maze generation with Prim's algorithm."""
        gen = MazeGeneratorWithAnimation(10, 8, seed=42)
        maze = gen.generate('prim')
        
        assert maze is not None
        assert len(maze) == 8
        assert len(maze[0]) == 10
    
    def test_dfs_generation(self):
        """Test maze generation with DFS algorithm."""
        gen = MazeGeneratorWithAnimation(10, 8, seed=42)
        maze = gen.generate('dfs')
        
        assert maze is not None
        assert len(maze) == 8
        assert len(maze[0]) == 10
    
    def test_animation_frames_captured(self):
        """Test that animation frames are captured."""
        gen = MazeGeneratorWithAnimation(8, 6, seed=42)
        maze = gen.generate('prim')
        
        frame_count = gen.get_frame_count()
        assert frame_count > 0, "Should capture at least one frame"
    
    def test_frame_rendering(self):
        """Test that frames can be rendered."""
        gen = MazeGeneratorWithAnimation(6, 5, seed=42)
        maze = gen.generate('prim')
        
        for i in range(gen.get_frame_count()):
            output = gen.render_frame_simple(i)
            assert output is not None
            assert len(output) > 0
    
    def test_pattern_cells(self):
        """Test with pattern cells."""
        pattern_cells = {(2, 2), (3, 2), (4, 2)}
        gen = MazeGeneratorWithAnimation(8, 6, pattern_cells=pattern_cells, seed=42)
        maze = gen.generate('prim')
        
        # Pattern cells should be in the final maze
        for x, y in pattern_cells:
            assert maze[y][x].visited
    
    def test_color_schemes(self):
        """Test different color schemes."""
        gen = MazeGeneratorWithAnimation(6, 5, seed=42)
        maze = gen.generate('prim')
        
        schemes = ["default", "emerald", "ocean", "amber"]
        for scheme in schemes:
            gen.color_scheme = scheme
            output = gen.render_frame_simple(gen.get_frame_count()-1)
            assert len(output) > 0
    
    def test_pattern_colors(self):
        """Test different pattern colors."""
        pattern_cells = {(2, 2)}
        gen = MazeGeneratorWithAnimation(6, 5, pattern_cells=pattern_cells, seed=42)
        maze = gen.generate('prim')
        
        colors = ["default", "magenta", "cyan", "red", "yellow", "white"]
        for color in colors:
            gen.pattern_color_scheme = color
            output = gen.render_frame_simple(gen.get_frame_count()-1)
            assert len(output) > 0
    
    def test_path_visualization(self):
        """Test path visualization toggle."""
        gen = MazeGeneratorWithAnimation(6, 5, seed=42, entry=(0, 0), exit_coords=(5, 4))
        maze = gen.generate('prim')
        
        # Without path
        gen.show_path = False
        output1 = gen.render_frame_simple(gen.get_frame_count()-1)
        
        # With path
        gen.show_path = True
        output2 = gen.render_frame_simple(gen.get_frame_count()-1)
        
        # Outputs should be different
        assert output1 != output2
    
    def test_perfect_maze(self):
        """Test perfect maze generation."""
        gen = MazeGeneratorWithAnimation(8, 6, seed=42, perfect=True)
        maze = gen.generate('prim')
        assert maze is not None
    
    def test_imperfect_maze(self):
        """Test imperfect maze generation."""
        gen = MazeGeneratorWithAnimation(8, 6, seed=42, perfect=False)
        maze = gen.generate('prim')
        assert maze is not None
        # Should have more frames for wall removal
        assert gen.get_frame_count() > 3


class TestMazeGenerator:
    """Test cases for the high-level MazeGenerator."""
    
    def test_initialization_with_config(self):
        """Test initialization with config file."""
        gen = MazeGenerator('config/default_config.txt', size=(10, 8))
        assert gen.config['WIDTH'] == 10
        assert gen.config['HEIGHT'] == 8
    
    def test_algorithm_switching(self):
        """Test switching between algorithms."""
        gen = MazeGenerator('config/default_config.txt', size=(8, 6))
        
        # Test Prim's
        gen.current_algo_idx = 0
        maze1 = gen.generate_maze()
        assert maze1 is not None
        
        # Test DFS
        gen.current_algo_idx = 1
        gen.config['SEED'] = 100
        maze2 = gen.generate_maze()
        assert maze2 is not None
    
    def test_color_scheme_cycling(self):
        """Test cycling through color schemes."""
        gen = MazeGenerator('config/default_config.txt', size=(6, 5))
        gen.generate_maze()
        
        for i, scheme in enumerate(gen.color_schemes):
            gen.generator.color_scheme = scheme
            output = gen.generator.render_frame_simple(gen.generator.get_frame_count()-1)
            assert len(output) > 0
    
    def test_pattern_color_cycling(self):
        """Test cycling through pattern colors."""
        gen = MazeGenerator('config/default_config.txt', size=(6, 5))
        gen.generate_maze()
        
        for i, color in enumerate(gen.pattern_color_schemes):
            gen.generator.pattern_color_scheme = color
            output = gen.generator.render_frame_simple(gen.generator.get_frame_count()-1)
            assert len(output) > 0
    
    def test_path_toggle(self):
        """Test path display toggle."""
        gen = MazeGenerator('config/default_config.txt', size=(6, 5))
        gen.generate_maze()
        
        # Toggle path
        gen.show_path = False
        gen.generator.show_path = False
        output1 = gen.generator.render_frame_simple(gen.generator.get_frame_count()-1)
        
        gen.show_path = True
        gen.generator.show_path = True
        output2 = gen.generator.render_frame_simple(gen.generator.get_frame_count()-1)
        
        # Both outputs should render without errors
        assert len(output1) > 0 and len(output2) > 0


def test_integration_both_algorithms():
    """Integration test for both algorithms with all features."""
    for algo in ['prim', 'dfs']:
        gen = MazeGeneratorWithAnimation(10, 8, seed=42, perfect=True)
        maze = gen.generate(algo)
        
        # Check maze is valid
        assert maze is not None
        assert len(maze) == 8
        assert len(maze[0]) == 10
        
        # Check frames captured
        assert gen.get_frame_count() > 0
        
        # Check rendering works
        output = gen.render_frame_simple(gen.get_frame_count()-1)
        assert len(output) > 0
        
        # Check color schemes work
        gen.color_scheme = "emerald"
        output = gen.render_frame_simple(gen.get_frame_count()-1)
        assert len(output) > 0


def test_reproducibility_with_seed():
    """Test that same seed produces same results."""
    # Test Prim's
    gen1 = MazeGeneratorWithAnimation(8, 6, seed=12345)
    maze1 = gen1.generate('prim')
    
    gen2 = MazeGeneratorWithAnimation(8, 6, seed=12345)
    maze2 = gen2.generate('prim')
    
    # Compare wall states
    for y in range(6):
        for x in range(8):
            assert maze1[y][x].walls == maze2[y][x].walls
    
    # Test DFS
    gen3 = MazeGeneratorWithAnimation(8, 6, seed=12345)
    maze3 = gen3.generate('dfs')
    
    gen4 = MazeGeneratorWithAnimation(8, 6, seed=12345)
    maze4 = gen4.generate('dfs')
    
    # Compare wall states
    for y in range(6):
        for x in range(8):
            assert maze3[y][x].walls == maze4[y][x].walls
