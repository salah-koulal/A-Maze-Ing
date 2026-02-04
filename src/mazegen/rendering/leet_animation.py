import time
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def read_text_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "File not found!"


def slide_in(text):
    lines = text.split('\n')
    max_len = max(len(line) for line in lines) if lines else 0

    for i in range(max_len + 1):
        clear_screen()
        for line in lines:
            spaces = " " * (max_len - i)
            print(spaces + line[:i])
        time.sleep(0.05)


def leet_animation():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "1337.txt")
    text = read_text_file(file_path)
    clear_screen()
    slide_in(text)
