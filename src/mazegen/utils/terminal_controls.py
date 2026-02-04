import sys

"""Low-level terminal cursor control."""


def write_ansi(code):
    sys.stdout.write(code)
    sys.stdout.flush()

def move_cursor(x, y):
    write_ansi(f"\x1b[{y};{x}H")


def clear_screen():
    write_ansi("\x1b[2J\x1b[H")


def hide_cursor():
    write_ansi("\x1b[?25l")


def show_cursor():
    write_ansi("\x1b[?25h")


def save_cursor():
    write_ansi("\x1b[s")


def restore_cursor():
    write_ansi("\x1b[u")

def set_fg(r, g, b):
    write_ansi(f"\x1b[38;2;{r};{g};{b}m")


def set_bg(r, g, b):
    write_ansi(f"\x1b[48;2;{r};{g};{b}m")


def reset_color():
    write_ansi("\x1b[0m")


