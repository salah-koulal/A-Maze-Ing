import random
import time
from typing import List, Tuple, Any, Optional
from .utils.config_parser import load_config
from .rendering.leet_animation import leet_animation
from .utils.pattern_embedder import get_pattern_cells
from .rendering.animated_maze_with_pattern import (
    AnimatedMazeGeneratorWithPattern
)
from .algorithms.path_finder import find_path


class MazeGenerator:
    """
    High-level API for maze generation and visualization.
    Integrates multiple algorithms, animation, and pattern protection.
    """
    def __init__(self, config_path: Optional[str] = None,
                 seed: Optional[str] = None,
                 size: Optional[Tuple[int, int]] = None) -> None:
        self.config = load_config(config_path)
        if seed is not None:
            self.config['SEED'] = int(seed)
        if size is not None:
            self.config['WIDTH'], self.config['HEIGHT'] = size
            self.config['EXIT'] = (size[0] - 1, size[1] - 1)

        self.current_algo_idx = 0
        self.algorithms = ["prim", "dfs"]
        self.color_schemes = ["default", "vivid", "emerald", "ocean", "amber"]
        self.current_color_idx = 0
        self.show_path = False

        self.generator: Optional[AnimatedMazeGeneratorWithPattern] = None
        self.last_maze: Optional[List[List[Any]]] = None

    def generate_maze(self) -> List[List[Any]]:
        """
        Generate a new maze based on the current configuration.
        Returns the maze grid (list of list of Cell objects).
        """
        entry = self.config.get('ENTRY', (0, 0))
        exit_coords = self.config.get('EXIT', (
            self.config['WIDTH'] - 1, self.config['HEIGHT'] - 1
        ))

        pattern_cells = get_pattern_cells(
            self.config['WIDTH'],
            self.config['HEIGHT'],
            entry=entry,
            exit_coords=exit_coords
        )

        self.generator = AnimatedMazeGeneratorWithPattern(
            width=self.config['WIDTH'],
            height=self.config['HEIGHT'],
            pattern_cells=list(pattern_cells),
            seed=str(self.config.get('SEED')),
            entry=entry,
            exit_coords=exit_coords,
            perfect=self.config.get('PERFECT', True)
        )
        self.generator.show_path = self.show_path
        self.generator.color_scheme = self.color_schemes[
            self.current_color_idx
        ]

        algo = self.algorithms[self.current_algo_idx]
        self.last_maze = self.generator.generate(algorithm=algo)
        return self.last_maze

    def draw_maze(self, maze: Optional[List[List[Any]]] = None) -> None:
        """
        Display the current state of the maze in the terminal.
        """
        if self.generator and self.generator.get_frame_count() > 0:
            # Render the last frame (fully generated maze)
            print(self.generator.render_frame_simple(
                self.generator.get_frame_count() - 1
            ))
        else:
            print("No maze generated yet. Call generate_maze() first.")

    def get_solution(self, maze: Optional[List[List[Any]]] = None) -> str:
        """
        Solve the maze and return the path as a string of directions.
        """
        target_maze = maze or self.last_maze
        if not target_maze:
            return ""

        grid_state = [[cell.walls for cell in row] for row in target_maze]
        entry = self.config.get('ENTRY', (0, 0))
        exit_coords = self.config.get('EXIT', (
            self.config['WIDTH'] - 1, self.config['HEIGHT'] - 1
        ))
        return find_path(grid_state, entry, exit_coords)

    def run(self) -> None:
        """
        Run the interactive maze generator loop with animation and menu.
        """
        # leet_animation()
        time.sleep(2)

        while True:
            self.generate_maze()

            # Write output file (mandatory part of subject)
            output_file = self.config.get('OUTPUT_FILE', 'maze_output.txt')
            entry = self.config.get('ENTRY', (0, 0))
            exit_coords = self.config.get('EXIT', (
                self.config['WIDTH'] - 1, self.config['HEIGHT'] - 1
            ))

            solution_path = self.get_solution()
            if self.generator:
                self.generator.write_to_hex_file(
                    output_file, entry, exit_coords, path=solution_path
                )

            if self.generator:
                self.generator.play_animation(fps=7000000000000.0)

            while True:
                # next_algo = (
                #     "DFS" if self.algorithms[
                #         (self.current_algo_idx + 1) % len(self.algorithms)
                #     ] == "prim" else "Prim's"
                # )
                print("\nchoices :")
                print(f"\n1 regenerate new maze :")
                print("2 show/hide the path from entry to exit")
                print("3 change maze colors")
                print("4 quit")

                choice = input("\n> enter a choice (1-4 ): ")

                if choice == '1':
                    self.current_algo_idx = (
                        self.current_algo_idx + 1
                    ) % len(self.algorithms)

                    if self.config.get('SEED'):
                        self.config['SEED'] += 0
                    else:
                        self.config['SEED'] = random.randint(1, 1000)
                    break
                elif choice == '2':
                    self.show_path = not self.show_path
                    if self.generator:
                        self.generator.show_path = self.show_path
                        print("\033[2J\033[H", end="")
                        if self.show_path:
                            # Animate path smoothly when showing
                            self.generator.animate_path(delay=0.03)
                        else:
                            # Just render without path
                            print(self.generator.render_frame_simple(
                                self.generator.get_frame_count() - 1
                            ))
                elif choice == '3':
                    self.current_color_idx = (
                        self.current_color_idx + 1
                    ) % len(self.color_schemes)
                    if self.generator:
                        self.generator.color_scheme = self.color_schemes[
                            self.current_color_idx
                        ]
                        print("\033[2J\033[H", end="")
                        print(self.generator.render_frame_simple(
                            self.generator.get_frame_count() - 1
                        ))
                elif choice == '4':
                    print("\nSEE YOU SOON! ")
                    print("\033[2J\033[H", end="")
                    print("A-MAZE-ING | By Skoulal & wabbad\n")
                    return
                else:
                    print("Invalid choice, try again.")
