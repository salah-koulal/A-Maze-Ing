import sys

"""Low-level terminal cursor control."""


def write_ansi(code: str) -> None:
    sys.stdout.write(code)
    sys.stdout.flush()


def move_cursor(x: int, y: int) -> None:
    write_ansi(f"\x1b[{y};{x}H")


def clear_screen() -> None:
    write_ansi("\x1b[2J\x1b[H")


def hide_cursor() -> None:
    write_ansi("\x1b[?25l")


def show_cursor() -> None:
    write_ansi("\x1b[?25h")


def save_cursor() -> None:
    write_ansi("\x1b[s")


def restore_cursor() -> None:
    write_ansi("\x1b[u")


def set_fg(r: int, g: int, b: int) -> None:
    write_ansi(f"\x1b[38;2;{r};{g};{b}m")


def set_bg(r: int, g: int, b: int) -> None:
    write_ansi(f"\x1b[48;2;{r};{g};{b}m")


def reset_color() -> None:
    write_ansi("\x1b[0m")
