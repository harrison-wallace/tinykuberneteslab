# Changelog

## Types of Changes
- [CHANGE]: A modification to an existing feature, behavior, or functionality.
- [BUGFIX]: A correction to resolve an error or unexpected behavior in the code.
- [FEATURE]: A new feature or capability added to the project.
- [DEPRECATED]: A feature or functionality marked for removal in future versions.
- [REMOVED]: A feature or functionality that has been fully removed.
- [SECURITY]: A change addressing a security vulnerability or improving security.
- [PERFORMANCE]: An optimization or improvement to enhance speed or efficiency.
- [DOCS]: Updates or additions to documentation, without code changes.

---
## Backlog

---

## [Unreleased]

---

## [0.1.0] - 2025-03-20
- [FEATURE]: `TK-001` Added real-time progress feedback in the TUI using `rich.Progress` with a spinner and live script output streaming for long-running operations like Minikube startup. (`lab_manager.py`, `ui.py`)
- [FEATURE]: `TK-001` Added an interactive menu in the TUI when the lab is already running, with options to "Destroy", "Continue", or "Show Status". (`ui.py`)
- [FEATURE]: `TK-001` Added display of the service URL in the TUI after starting the lab and in the "Show Status" table. (`ui.py`)
- [DOCS]: `TK-001` Created a cheatsheet for interacting with the lab, covering cluster management (`kubectl` commands) and pod access (`kubectl exec`, `kubectl cp`).
- [CHANGE]: `TK-001` Improved the "already running" feedback in the TUI to display `Lab q1 is already running.` in bold yellow, making it clearer to the user. (`ui.py`)
- [CHANGE]: `TK-001`Updated the "Show Status" table to render without ANSI escape codes in the `curses` TUI using `Console(force_terminal=False, record=True)`. (`ui.py`)
- [BUGFIX]: `TK-001` Fixed `FileNotFoundError: [Errno 2] No such file or directory: '../scripts'` by using absolute paths in `lab_manager.py` and calculating `BASE_DIR` with `os.getcwd()`. (`lab_manager.py`)
