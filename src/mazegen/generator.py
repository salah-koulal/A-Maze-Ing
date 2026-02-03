"""
Main maze generator module.
This is the high-level interface for generating and displaying mazes.

For details on the algorithms, see internal/README.md
"""

import random
import time
import sys
import os
from typing import List, Tuple, Any

# Add src directory to path for imports
src_path = os.path.join(os.path.dirname(__file__), '..')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from .internal.config_parser import load_config
from .internal.leet_animation import leet_animation
from .internal.pattern_embedder import get_pattern_cells
from .internal.path_finder import find_path

# Import the animators from src directory
from animatable_maze_adapter import AnimatableMazeGenerator
from maze_animator import MazeAnimator
from maze_animator_prim import PrimMazeAnimator


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
        
        # Color scheme settings
        self.color_schemes = ["default", "blue", "green", "red", "yellow", "magenta", "cyan"]
        self.current_color_idx = 0
        
        # Display settings
        self.show_path = False  # Whether to show solution path
        
        # The actual generator and animator instances
        self.generator = None
        self.animator = None
        self.last_maze = None
        self.last_path = ""  # Store the solution path

    def generate_maze(self) -> List[List[Any]]:
        """
        Generate a new maze based on the current configuration.
        Uses real-time animation with FrameRenderer.
        
        This method:
        1. Gets entry/exit points from config
        2. Generates "42" pattern coordinates
        3. Creates an AnimatableMazeGenerator instance
        4. Uses appropriate animator (DFS or Prim)
        5. Animates the generation in real-time
        
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
        
        # Create the animatable maze generator
        algo = self.algorithms[self.current_algo_idx]
        self.generator = AnimatableMazeGenerator(
            algorithm=algo,
            width=self.config['WIDTH'],
            height=self.config['HEIGHT'],
            seed=self.config.get('SEED'),
            pattern_cells=pattern_cells
        )
        
        # Create appropriate animator
        if algo == 'prim':
            self.animator = PrimMazeAnimator(self.generator)
        else:  # dfs
            self.animator = MazeAnimator(self.generator)
        
        # Set color scheme on renderer
        self.animator.renderer.color_scheme = self.color_schemes[self.current_color_idx]
        
        # Animate the generation process
        self.animator.animate_generation(delay=0.05)
        
        # Store the generated maze
        self.last_maze = self.generator.grid
        
        # Compute and store the solution path
        entry = self.config.get('ENTRY', (0, 0))
        exit_coords = self.config.get('EXIT', (self.config['WIDTH']-1, self.config['HEIGHT']-1))
        grid_state = [[cell.walls for cell in row] for row in self.last_maze]
        self.last_path = find_path(grid_state, entry, exit_coords)
        
        # Set path info on renderer
        self.animator.renderer.set_path_info(self.last_path, entry, exit_coords)
        self.animator.renderer.show_path = self.show_path
        
        return self.last_maze

    def draw_maze(self, maze: List[List[Any]] = None):
        """
        Display the current state of the maze in the terminal.
        Uses the frame renderer for consistent display.
        """
        if self.generator and self.animator:
            # Update renderer settings
            self.animator.renderer.color_scheme = self.color_schemes[self.current_color_idx]
            self.animator.renderer.show_path = self.show_path
            
            # Re-render the final maze
            from terminal_controls import clear_screen
            clear_screen()
            self.animator.renderer.render_full(show_visited=True)
            self.animator.renderer.display()
            print("\n")
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

    def write_to_file(self, filename: str, entry: Tuple[int, int], exit_coords: Tuple[int, int], path: str):
        """
        Write maze to file in hexadecimal format.
        
        Args:
            filename: Output filename
            entry: Entry coordinates
            exit_coords: Exit coordinates  
            path: Solution path string
        """
        with open(filename, 'w') as f:
            for row in self.last_maze:
                line = ''.join(format(cell.walls, 'X') for cell in row)
                f.write(line + '\n')
            
            f.write('\n')
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_coords[0]},{exit_coords[1]}\n")
            f.write(f"{path}\n")
    
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
            
            # Get solution path
            grid_state = [[cell.walls for cell in row] for row in self.last_maze]
            path_str = find_path(grid_state, entry, exit_coords)
            
            # Write to file
            self.write_to_file(output_file, entry, exit_coords, path_str)
            
            # Menu Loop
            while True:
                next_algo = "DFS" if self.algorithms[(self.current_algo_idx + 1) % len(self.algorithms)] == "dfs" else "Prim's"
                print("\nchoices :")
                print(f"\n1 regenerate new maze (Next: {next_algo})")
                print("2 show current maze")
                print("3 change maze wall colors")
                print("4 show/hide path from entry to exit")
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
                    break  # Break inner loop to regenerate
                elif choice == '2':
                    # Show the maze again
                    self.draw_maze()
                elif choice == '3':
                    # Cycle through color schemes
                    self.current_color_idx = (self.current_color_idx + 1) % len(self.color_schemes)
                    current_color = self.color_schemes[self.current_color_idx]
                    print(f"\nMaze color changed to: {current_color}")
                    self.draw_maze()
                elif choice == '4':
                    # Toggle path visibility
                    self.show_path = not self.show_path
                    status = "visible" if self.show_path else "hidden"
                    print(f"\nPath is now: {status}")
                    self.draw_maze()
                elif choice == '5':
                    print("\nSEE YOU SOON! ")
                    print("\033[2J\033[H", end="") 
                    print("A-MAZE-ING | 42 School\n")
                    return
                else:
                    print("Invalid choice, try again.")
