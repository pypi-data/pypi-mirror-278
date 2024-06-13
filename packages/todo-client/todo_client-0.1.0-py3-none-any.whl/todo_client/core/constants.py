#!/usr/bin/env python3

"""
This module contains constants used throughout the todos application.
"""

# Default file name for the to-do list
DEFAULT_TODO_FILE = "todo.yaml"

# The banner displayed when entering REPL mode.
REPL_BANNER = """
 _____ ___________ _____   ______ ___________ _
|_   _|  _  |  _  \\  _  |  | ___ \\  ___| ___ \\ |
  | | | | | | | | | | | |  | |_/ / |__ | |_/ / |
  | | | | | | | | | | | |  |    /|  __||  __/| |
  | | \\ \\_/ / |/ /\\ \\_/ /  | |\\ \\| |___| |   | |____
  \\_/  \\___/|___/  \\___/   \\_| \\_\\____/\\_|   \\_____/
"""

# REPL commands
TASK_ADD = "add"
TASK_CLEAR = "clear"
TASK_DONE = "done"
TASK_EXIT = "exit"
TASK_HELP = "help"
TASK_LIST = "list"
TASK_REMOVE = "remove"

# The list of commands available in REPL mode.
REPL_COMMANDS = f"""
Commands:
- {TASK_ADD} <task>
- {TASK_REMOVE} <index>
- {TASK_DONE} <index>
- {TASK_LIST}
- {TASK_CLEAR}
- {TASK_EXIT}
- {TASK_HELP}
"""
