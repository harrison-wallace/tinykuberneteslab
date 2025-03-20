from .ui import main
import curses

if __name__ == "__main__":
    curses.wrapper(main)