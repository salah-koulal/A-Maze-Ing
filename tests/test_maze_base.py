"""
Test suite for the unified base classes (Cell and MazeGeneratorBase).
"""

import pytest
from src.mazegen.internal.maze_base import Cell, MazeGeneratorBase


class TestCell:
    """Test cases for the Cell class."""
    
    def test_cell_initialization(self):
        """Test that cells are initialized correctly."""
        cell = Cell(5, 10)
        assert cell.x == 5
        assert cell.y == 10
        assert cell.walls == 15  # All walls present (0b1111)
        assert cell.visited is False
    
    def test_has_wall_all_directions(self):
        """Test has_wall for all directions when all walls present."""
        cell = Cell(0, 0)
        assert cell.has_wall('N')
        assert cell.has_wall('E')
        assert cell.has_wall('S')
        assert cell.has_wall('W')
    
    def test_remove_wall_north(self):
        """Test removing north wall."""
        cell = Cell(0, 0)
        cell.remove_wall('N')
        assert not cell.has_wall('N')
        assert cell.has_wall('E')
        assert cell.has_wall('S')
        assert cell.has_wall('W')
        assert cell.walls == 14  # 0b1110
    
    def test_remove_wall_east(self):
        """Test removing east wall."""
        cell = Cell(0, 0)
        cell.remove_wall('E')
        assert cell.has_wall('N')
        assert not cell.has_wall('E')
        assert cell.has_wall('S')
        assert cell.has_wall('W')
        assert cell.walls == 13  # 0b1101
    
    def test_remove_wall_south(self):
        """Test removing south wall."""
        cell = Cell(0, 0)
        cell.remove_wall('S')
        assert cell.has_wall('N')
        assert cell.has_wall('E')
        assert not cell.has_wall('S')
        assert cell.has_wall('W')
        assert cell.walls == 11  # 0b1011
    
    def test_remove_wall_west(self):
        """Test removing west wall."""
        cell = Cell(0, 0)
        cell.remove_wall('W')
        assert cell.has_wall('N')
        assert cell.has_wall('E')
        assert cell.has_wall('S')
        assert not cell.has_wall('W')
        assert cell.walls == 7  # 0b0111
    
    def test_remove_multiple_walls(self):
        """Test removing multiple walls."""
        cell = Cell(0, 0)
        cell.remove_wall('N')
        cell.remove_wall('E')
        assert not cell.has_wall('N')
        assert not cell.has_wall('E')
        assert cell.has_wall('S')
        assert cell.has_wall('W')
        assert cell.walls == 12  # 0b1100
    
    def test_remove_all_walls(self):
        """Test removing all walls."""
        cell = Cell(0, 0)
        cell.remove_wall('N')
        cell.remove_wall('E')
        cell.remove_wall('S')
        cell.remove_wall('W')
        assert not cell.has_wall('N')
        assert not cell.has_wall('E')
        assert not cell.has_wall('S')
        assert not cell.has_wall('W')
        assert cell.walls == 0


class TestMazeGeneratorBase:
    """Test cases for MazeGeneratorBase class."""
    
    def test_initialization_basic(self):
        """Test basic initialization without pattern cells."""
        class TestGenerator(MazeGeneratorBase):
            def generate(self):
                return self.grid
        
        gen = TestGenerator(5, 4, seed=42)
        assert gen.width == 5
        assert gen.height == 4
        assert len(gen.grid) == 4
        assert len(gen.grid[0]) == 5
    
    def test_initialization_with_pattern(self):
        """Test initialization with pattern cells."""
        class TestGenerator(MazeGeneratorBase):
            def generate(self):
                return self.grid
        
        pattern_cells = {(1, 1), (2, 2), (3, 1)}
        gen = TestGenerator(5, 4, seed=42, pattern_cells=pattern_cells)
        
        # Check pattern cells are marked as visited
        for x, y in pattern_cells:
            assert gen.grid[y][x].visited, f"Pattern cell ({x}, {y}) should be visited"
        
        # Check non-pattern cells are not visited
        assert not gen.grid[0][0].visited
        assert not gen.grid[3][4].visited
    
    def test_get_cell_valid(self):
        """Test get_cell with valid coordinates."""
        class TestGenerator(MazeGeneratorBase):
            def generate(self):
                return self.grid
        
        gen = TestGenerator(5, 4)
        cell = gen.get_cell(2, 1)
        assert cell is not None
        assert cell.x == 2
        assert cell.y == 1
    
    def test_get_cell_invalid(self):
        """Test get_cell with invalid coordinates."""
        class TestGenerator(MazeGeneratorBase):
            def generate(self):
                return self.grid
        
        gen = TestGenerator(5, 4)
        assert gen.get_cell(-1, 0) is None
        assert gen.get_cell(5, 0) is None
        assert gen.get_cell(0, -1) is None
        assert gen.get_cell(0, 4) is None
    
    def test_get_neighbors_corner(self):
        """Test get_neighbors for corner cell."""
        class TestGenerator(MazeGeneratorBase):
            def generate(self):
                return self.grid
        
        gen = TestGenerator(5, 4)
        cell = gen.grid[0][0]
        neighbors = gen.get_neighbors(cell)
        
        # Corner cell should have 2 neighbors
        assert len(neighbors) == 2
        
        # Check neighbors are correct
        neighbor_positions = [(n.x, n.y) for n, _ in neighbors]
        assert (1, 0) in neighbor_positions  # East
        assert (0, 1) in neighbor_positions  # South
    
    def test_get_neighbors_edge(self):
        """Test get_neighbors for edge cell."""
        class TestGenerator(MazeGeneratorBase):
            def generate(self):
                return self.grid
        
        gen = TestGenerator(5, 4)
        cell = gen.grid[0][2]  # Top edge
        neighbors = gen.get_neighbors(cell)
        
        # Edge cell should have 3 neighbors
        assert len(neighbors) == 3
    
    def test_get_neighbors_middle(self):
        """Test get_neighbors for middle cell."""
        class TestGenerator(MazeGeneratorBase):
            def generate(self):
                return self.grid
        
        gen = TestGenerator(5, 4)
        cell = gen.grid[2][2]  # Middle
        neighbors = gen.get_neighbors(cell)
        
        # Middle cell should have 4 neighbors
        assert len(neighbors) == 4
    
    def test_get_unvisited_neighbors(self):
        """Test get_unvisited_neighbors filtering."""
        class TestGenerator(MazeGeneratorBase):
            def generate(self):
                return self.grid
        
        gen = TestGenerator(5, 4)
        cell = gen.grid[2][2]
        
        # Mark some neighbors as visited
        gen.grid[1][2].visited = True  # North
        gen.grid[2][3].visited = True  # East
        
        unvisited = gen.get_unvisited_neighbors(cell)
        
        # Should only have 2 unvisited neighbors (South and West)
        assert len(unvisited) == 2
        unvisited_positions = [(n.x, n.y) for n, _ in unvisited]
        assert (2, 1) not in unvisited_positions  # North is visited (row 1, col 2)
        assert (3, 2) not in unvisited_positions  # East is visited (row 2, col 3)
    
    def test_remove_wall_between(self):
        """Test removing wall between two cells."""
        class TestGenerator(MazeGeneratorBase):
            def generate(self):
                return self.grid
        
        gen = TestGenerator(5, 4)
        cell1 = gen.grid[1][1]
        cell2 = gen.grid[0][1]  # North of cell1
        
        # Both should have walls initially
        assert cell1.has_wall('N')
        assert cell2.has_wall('S')
        
        # Remove wall between them
        gen.remove_wall_between(cell1, cell2, 'N')
        
        # Both walls should be removed
        assert not cell1.has_wall('N')
        assert not cell2.has_wall('S')
    
    def test_grid_cell_positions(self):
        """Test that all grid cells have correct positions."""
        class TestGenerator(MazeGeneratorBase):
            def generate(self):
                return self.grid
        
        gen = TestGenerator(5, 4)
        
        for y in range(4):
            for x in range(5):
                cell = gen.grid[y][x]
                assert cell.x == x
                assert cell.y == y


def test_pattern_protection_integration():
    """Integration test for pattern protection."""
    class TestGenerator(MazeGeneratorBase):
        def generate(self):
            # Simple generation that visits all non-pattern cells
            for row in self.grid:
                for cell in row:
                    if not cell.visited:
                        cell.visited = True
            return self.grid
    
    pattern_cells = {(1, 1), (2, 2)}
    gen = TestGenerator(4, 4, pattern_cells=pattern_cells)
    
    # Pattern cells should already be visited
    for x, y in pattern_cells:
        assert gen.grid[y][x].visited
    
    # Generate maze
    maze = gen.generate()
    
    # All cells should be visited after generation
    for row in maze:
        for cell in row:
            assert cell.visited
