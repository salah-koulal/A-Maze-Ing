from ..utils.terminal_controls import hide_cursor,clear_screen
import time
import os


def read_text_file(filename: str) -> str:
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "File not found!"


def slide_in(text: str) -> None:
    lines = text.split('\n')
    max_len = max(len(line) for line in lines) if lines else 0

    for i in range(max_len + 1):
        clear_screen()
        for line in lines:
            spaces = " " * (max_len - i)
            print(spaces + line[:i])
        time.sleep(0.05)


def leet_animation() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "1337.txt")
    text = read_text_file(file_path)
    clear_screen()
    hide_cursor()
    slide_in(text)
