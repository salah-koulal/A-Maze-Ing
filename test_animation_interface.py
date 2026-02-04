from src.mazegen.algorithms.prim import MazeGenerator as PrimGenerator
from src.mazegen.algorithms.dfs import MazeGenerator as DFSGenerator

def check_interface(gen_class, name):
    print(f"Checking {name}...")
    gen = gen_class(10, 10)
    
    if not hasattr(gen, '_get_unvisited_neighbors'):
        print(f"FAIL: {name} missing _get_unvisited_neighbors")
        return False
        
    if not hasattr(gen, '_carve_passage'):
        print(f"FAIL: {name} missing _carve_passage")
        return False
        
    cell = gen.grid[0][0]
    if not hasattr(cell, 'enabled'):
        print(f"FAIL: {name} Cell missing enabled attribute")
        return False
        
    print(f"PASS: {name} has required interface.")
    return True

if __name__ == "__main__":
    p = check_interface(PrimGenerator, "PrimGenerator")
    d = check_interface(DFSGenerator, "DFSGenerator")
    
    if p and d:
        print("All checks passed.")
        exit(0)
    else:
        exit(1)
