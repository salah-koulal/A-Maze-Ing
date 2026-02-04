from src.mazegen.rendering.animated_maze_with_pattern import AnimatedMazeGeneratorWithPattern

def test_colors():
    gen = AnimatedMazeGeneratorWithPattern(5, 5, [], entry=(0,0), exit_coords=(4,4), seed=42)
    gen.generate()
    
    # 1. Default (Subject)
    gen.color_scheme = "subject"
    frame_subject = gen.render_frame_simple(0)
    
    # 2. Vivid
    gen.color_scheme = "vivid"
    frame_vivid = gen.render_frame_simple(0)
    
    # Check for ANSI codes (escapes)
    has_esc_subject = "\033[" in frame_subject
    has_esc_vivid = "\033[" in frame_vivid
    
    print(f"Subject has ANSI: {has_esc_subject}")
    print(f"Vivid has ANSI: {has_esc_vivid}")
    
    if frame_subject == frame_vivid:
        print("FAILURE: Frames are identical despite different color schemes!")
    else:
        print("SUCCESS: Frames differ with different color schemes.")

if __name__ == "__main__":
    test_colors()
