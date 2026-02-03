"""
Main maze generator module.
This is the high-level interface for generating and displaying mazes.

For details on the algorithms, see internal/README.md
"""

import random
import time
from typing import List, Tuple, Any
from .internal.config_parser import load_config
from .internal.leet_animation import leet_animation
from .internal.pattern_embedder import get_pattern_cells
from .internal.maze_with_animation import MazeGeneratorWithAnimation
from .internal.path_finder import find_path


class MazeGenerator:
    """
    High-level API for maze generation and visualization.
    
    This class manages:
    - Configuration loading
    - Algorithm selection (Prim's or DFS)
    - Color schemes for walls and patterns
    - Interactive menu system
    - Animation playback
    
    Usage:
        gen = MazeGenerator('config/default_config.txt')
        gen.run()  # Start interactive mode
    """
    
    def __init__(self, config_path: str, seed: str = None, size: Tuple[int, int] = None):
        """
        Initialize the maze generator.
        
        Args:
            config_path: Path to configuration file
            seed: Optional random seed (overrides config)
            size: Optional (width, height) tuple (overrides config)
        """
        # Load configuration from file
        self.config = load_config(config_path)
        
        # Override with provided parameters
        if seed is not None:
            self.config['SEED'] = int(seed)
        if size is not None:
            self.config['WIDTH'], self.config['HEIGHT'] = size
        
        # Algorithm settings: ["prim", "dfs"]
        # Start with Prim's algorithm (index 0)
        self.current_algo_idx = 0
        self.algorithms = ["prim", "dfs"]
        
        # Color scheme settings for maze walls
        self.color_schemes = ["default", "emerald", "ocean", "amber"]
        self.current_color_idx = 0
        
        # Pattern color settings (for "42" pattern)
        self.pattern_color_schemes = ["default", "magenta", "cyan", "red", "yellow", "white"]
        self.current_pattern_color_idx = 0
        
        # Display settings
        self.show_path = False  # Whether to show solution path
        
        # The actual generator instance (created when generating)
        self.generator = None
        self.last_maze = None

    def generate_maze(self) -> List[List[Any]]:
        """
        Generate a new maze based on the current configuration.
        
        This method:
        1. Gets entry/exit points from config
        2. Generates "42" pattern coordinates
        3. Creates a MazeGeneratorWithAnimation instance
        4. Generates the maze using current algorithm (Prim or DFS)
        5. Captures animation frames during generation
        
        Returns:
            The generated maze grid (list of list of Cell objects)
        """
        # Get entry and exit points from configuration
        entry = self.config.get('ENTRY', (0, 0))
        exit_coords = self.config.get('EXIT', (self.config['WIDTH']-1, self.config['HEIGHT']-1))
        
        # Generate the "42" pattern cells to protect during maze generation
        pattern_cells = get_pattern_cells(
            self.config['WIDTH'], 
            self.config['HEIGHT'], 
            entry=entry, 
            exit_coords=exit_coords
        )
        
        # Create the maze generator with animation support
        self.generator = MazeGeneratorWithAnimation(
            width=self.config['WIDTH'],
            height=self.config['HEIGHT'],
            pattern_cells=pattern_cells,
            seed=self.config.get('SEED'),
            entry=entry,
            exit_coords=exit_coords,
            perfect=self.config.get('PERFECT', True)
        )
        
        # Apply current display settings
        self.generator.show_path = self.show_path
        self.generator.color_scheme = self.color_schemes[self.current_color_idx]
        self.generator.pattern_color_scheme = self.pattern_color_schemes[self.current_pattern_color_idx]
        
        # Generate the maze using current algorithm ("prim" or "dfs")
        algo = self.algorithms[self.current_algo_idx]
        self.last_maze = self.generator.generate(algorithm=algo)
        return self.last_maze

    def draw_maze(self, maze: List[List[Any]] = None):
        """
        Display the current state of the maze in the terminal.
        """
        if self.generator and self.generator.frames:
            # Render the last frame (fully generated maze)
            print(self.generator.render_frame_simple(self.generator.get_frame_count() - 1))
        else:
            print("No maze generated yet. Call generate_maze() first.")

    def get_solution(self, maze: List[List[Any]] = None) -> str:
        """
        Solve the maze and return the path as a string of directions (N, E, S, W).
        """
        target_maze = maze or self.last_maze
        if not target_maze:
            return ""
            
        grid_state = [[cell.walls for cell in row] for row in target_maze]
        entry = self.config.get('ENTRY', (0, 0))
        exit_coords = self.config.get('EXIT', (self.config['WIDTH']-1, self.config['HEIGHT']-1))
        return find_path(grid_state, entry, exit_coords)

    def run(self):
        """
        Run the interactive maze generator loop with animation and menu.
        """
        leet_animation()
        time.sleep(2)
        
        while True:
            algo_name = "Prim's" if self.algorithms[self.current_algo_idx] == "prim" else "DFS"
            print(f"Generating {self.config['WIDTH']}x{self.config['HEIGHT']} maze using {algo_name} algorithm...")
            
            self.generate_maze()
            
            # Write output file (mandatory part of subject)
            output_file = self.config.get('OUTPUT_FILE', 'maze_output.txt')
            entry = self.config.get('ENTRY', (0, 0))
            exit_coords = self.config.get('EXIT', (self.config['WIDTH']-1, self.config['HEIGHT']-1))
            self.generator.write_to_hex_file(output_file, entry, exit_coords)
            
            # Play animation
            self.generator.play_animation(fps=20.0)
            
            # Menu Loop
            while True:
                next_algo = "DFS" if self.algorithms[(self.current_algo_idx + 1) % len(self.algorithms)] == "prim" else "Prim's (Default)"
                print("\nchoices :")
                print(f"\n1 regenerate new maze (Next: {next_algo})")
                print("2 show/hide the path from entry to exit")
                print("3 change maze colors")
                print("4 change '42' pattern colors")
                print("5 quit")
                
                choice = input("\n> enter a choice (1-5): ")
                
                if choice == '1':
                    # Cycle algorithm
                    self.current_algo_idx = (self.current_algo_idx + 1) % len(self.algorithms)
                    
                    # Update seed for new maze
                    if self.config.get('SEED'):
                        self.config['SEED'] += 1
                    else:
                        self.config['SEED'] = random.randint(1, 1000)
                    break # Break inner loop to regenerate
                elif choice == '2':
                    self.show_path = not self.show_path
                    self.generator.show_path = self.show_path
                    # Re-render final frame with path toggled
                    print("\033[2J\033[H", end="")
                    print(self.generator.render_frame_simple(self.generator.get_frame_count()-1))
                elif choice == '3':
                    self.current_color_idx = (self.current_color_idx + 1) % len(self.color_schemes)
                    self.generator.color_scheme = self.color_schemes[self.current_color_idx]
                    # Re-render final frame with color changed
                    print("\033[2J\033[H", end="")
                    print(self.generator.render_frame_simple(self.generator.get_frame_count()-1))
                elif choice == '4':
                    self.current_pattern_color_idx = (self.current_pattern_color_idx + 1) % len(self.pattern_color_schemes)
                    self.generator.pattern_color_scheme = self.pattern_color_schemes[self.current_pattern_color_idx]
                    print(f"Pattern color changed to: {self.pattern_color_schemes[self.current_pattern_color_idx]}")
                    # Re-render final frame with pattern color changed
                    print("\033[2J\033[H", end="")
                    print(self.generator.render_frame_simple(self.generator.get_frame_count()-1))
                elif choice == '5':
                    print("\nSEE YOU SOON! ")
                    print("\033[2J\033[H", end="") 
                    print("A-MAZE-ING | 42 School\n")
                    return
                else:
                    print("Invalid choice, try again.")
