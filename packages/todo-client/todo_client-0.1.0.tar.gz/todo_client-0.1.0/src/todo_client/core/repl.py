#!/usr/bin/env python3

import logging
import readline

from .constants import (
    REPL_BANNER,
    REPL_COMMANDS,
    TASK_ADD,
    TASK_CLEAR,
    TASK_DONE,
    TASK_EXIT,
    TASK_HELP,
    TASK_LIST,
    TASK_REMOVE,
)
from .tasks import add_task, clear_tasks, list_tasks, mark_done, remove_task

logger = logging.getLogger(__name__)


def repl(file):
    """
    Enter REPL mode for the to-do list application.

    :param file: The file where the to-do list is stored.
    :type file: str
    """
    print(REPL_BANNER)
    print("Entering REPL mode. Type 'help' for a list of commands.")

    while True:
        try:
            # Get user input and split it into a command and arguments
            line = input("> ").strip()
            readline.add_history(line)  # Add the line to the history
            command = line.split()

            # Skip empty commands
            if not command:
                continue

            # Extract the command and arguments
            cmd, *args = command

            # Add a task
            if cmd == TASK_ADD:
                if args:
                    add_task(" ".join(args), file)
                else:
                    print("Usage: add <task>")

            # Clear all tasks
            elif cmd == TASK_CLEAR:
                clear_tasks(file)

            # List all tasks
            elif cmd == TASK_DONE:
                if args and args[0].isdigit():
                    mark_done(int(args[0]), file)
                else:
                    print("Usage: done <index>")

            # Mark a task as done
            elif cmd == TASK_LIST:
                list_tasks(file)

            # Remove a task
            elif cmd == TASK_REMOVE:
                if args and args[0].isdigit():
                    remove_task(int(args[0]), file)
                else:
                    print("Usage: remove <index>")

            # Display help
            elif cmd == TASK_HELP:
                print(REPL_COMMANDS)

            # Exit REPL mode
            elif cmd == TASK_EXIT:
                break

            # Unknown command
            else:
                print(f"Unknown command: {cmd}")
        except (EOFError, KeyboardInterrupt):
            break

    print("Exiting REPL mode. Goodbye.")
