from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
import curses
from .lab_manager import start_lab, destroy_lab, get_status
import time

console = Console()

def draw_menu(stdscr, selected_idx, options):
    stdscr.clear()
    for idx, option in enumerate(options):
        x = 2
        y = idx + 2
        if idx == selected_idx:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y, x, option)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, option)
    stdscr.refresh()

def display_message(stdscr, message, color_pair=None):
    stdscr.clear()
    lines = message.split("\n")
    for i, line in enumerate(lines[:10]):  # Limit to 10 lines to avoid overflow
        stdscr.addstr(i + 2, 2, line[:80])  # Limit line length to 80 chars
    stdscr.addstr(12, 2, "Press any key to continue...")
    stdscr.refresh()
    stdscr.getch()

def show_already_running_menu(stdscr, lab):
    selected_idx = 0
    options = ["Destroy", "Continue", "Show Status"]
    while True:
        draw_menu(stdscr, selected_idx, options)
        key = stdscr.getch()

        if key == curses.KEY_UP and selected_idx > 0:
            selected_idx -= 1
        elif key == curses.KEY_DOWN and selected_idx < len(options) - 1:
            selected_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            choice = options[selected_idx].lower()
            if choice == "destroy":
                curses.endwin()
                run_with_progress("destroy", lab)
                stdscr = curses.initscr()
                curses.curs_set(0)
                curses.start_color()
                curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
                curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
                return True  # Indicate the lab was destroyed
            elif choice == "continue":
                return False  # Return to main menu
            elif choice == "show status":
                status = get_status(lab)
                table = Table(title="Lab Q1 Status")
                table.add_column("Field", style="cyan")
                table.add_column("Value", style="green")
                table.add_row("Running", str(status["running"]))
                table.add_row("Logs", status["logs"] or "N/A")
                # Render table without ANSI codes for curses
                console_for_render = Console(force_terminal=False, record=True)
                console_for_render.print(table)
                table_str = console_for_render.export_text()
                display_message(stdscr, table_str)

def run_with_progress(action, lab):
    output_lines = []
    def output_callback(line):
        output_lines.append(line)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        task = progress.add_task(f"Running {action} for {lab}...", total=None)
        result = globals()[f"{action}_lab"](lab, output_callback=output_callback)
    
    color = "green" if action == "start" else "red"
    console.print(f"[bold {color}]{action.capitalize()}ing Lab {lab}[/bold {color}]")
    for line in output_lines:
        console.print(line)
    console.print("\nPress Enter to continue...")
    input()
    return result

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    selected_idx = 0
    actions = ["start", "destroy", "status", "exit"]
    
    # Initialize color pairs for better visibility
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    
    while True:
        draw_menu(stdscr, selected_idx, ["Start Lab Q1", "Destroy Lab Q1", "Show Status", "Exit"])
        key = stdscr.getch()

        if key == curses.KEY_UP and selected_idx > 0:
            selected_idx -= 1
        elif key == curses.KEY_DOWN and selected_idx < len(actions) - 1:
            selected_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            action = actions[selected_idx]
            if action == "exit":
                break
            elif action in ["start", "destroy"]:
                # Exit curses temporarily to show progress
                curses.endwin()
                result = run_with_progress(action, "q1")
                # Reinitialize curses
                stdscr = curses.initscr()
                curses.curs_set(0)
                curses.start_color()
                curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
                curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
                # If the lab is already running and action is start, show the menu
                if action == "start" and "already running" in result.lower():
                    destroyed = show_already_running_menu(stdscr, "q1")
                    # If the user destroyed the lab, try starting it again
                    if destroyed:
                        curses.endwin()
                        run_with_progress(action, "q1")
                        stdscr = curses.initscr()
                        curses.curs_set(0)
                        curses.start_color()
                        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
                        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            elif action == "status":
                status = get_status("q1")
                table = Table(title="Lab Q1 Status")
                table.add_column("Field", style="cyan")
                table.add_column("Value", style="green")
                table.add_row("Running", str(status["running"]))
                table.add_row("Logs", status["logs"] or "N/A")
                # Render table without ANSI codes for curses
                console_for_render = Console(force_terminal=False, record=True)
                console_for_render.print(table)
                table_str = console_for_render.export_text()
                display_message(stdscr, table_str)