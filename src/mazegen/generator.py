import random
import time
from typing import List, Tuple, Any
from .internal.config_parser import load_config
from .internal.leet_animation import leet_animation
from .internal.pattern_embedder import get_pattern_cells
from .internal.animated_maze_with_pattern import AnimatedMazeGeneratorWithPattern
from .internal.path_finder import find_path

class MazeGenerator:
    """
    High-level API for maze generation and visualization.
    Integrates multiple algorithms, animation, and pattern protection.
    """
    def __init__(self, config_path: str, seed: str = None, size: Tuple[int, int] = None):
        self.config = load_config(config_path)
        if seed is not None:
            self.config['SEED'] = int(seed)
        if size is not None:
            self.config['WIDTH'], self.config['HEIGHT'] = size
            
        self.current_algo_idx = 0
        self.algorithms = ["prim", "dfs"]
        self.color_schemes = ["default", "emerald", "ocean", "amber"]
        self.current_color_idx = 0
        self.show_path = False
        
        self.generator = None
        self.last_maze = None

    def generate_maze(self) -> List[List[Any]]:
        """
        Generate a new maze based on the current configuration.
        Returns the maze grid (list of list of Cell objects).
        """
        entry = self.config.get('ENTRY', (0, 0))
        exit_coords = self.config.get('EXIT', (self.config['WIDTH']-1, self.config['HEIGHT']-1))
        
        pattern_cells = get_pattern_cells(
            self.config['WIDTH'], 
            self.config['HEIGHT'], 
            entry=entry, 
            exit_coords=exit_coords
        )
        
        self.generator = AnimatedMazeGeneratorWithPattern(
            width=self.config['WIDTH'],
            height=self.config['HEIGHT'],
            pattern_cells=pattern_cells,
            seed=self.config.get('SEED'),
            entry=entry,
            exit_coords=exit_coords,
            perfect=self.config.get('PERFECT', True)
        )
        self.generator.show_path = self.show_path
        self.generator.color_scheme = self.color_schemes[self.current_color_idx]
        
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
                print("4 quit")
                
                choice = input("\n> enter a choice (1-4 ): ")
                
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
                    print("\nSEE YOU SOON! ")
                    print("\033[2J\033[H", end="") 
                    print("A-MAZE-ING | 42 School\n")
                    return
                else:
                    print("Invalid choice, try again.")
