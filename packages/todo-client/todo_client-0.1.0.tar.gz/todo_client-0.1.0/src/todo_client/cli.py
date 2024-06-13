#!/usr/bin/env python3

"""
This is the CLI module for the todo_client package.
"""

import logging
from argparse import ArgumentParser

from .core.constants import (
    DEFAULT_TODO_FILE,
    TASK_ADD,
    TASK_CLEAR,
    TASK_DONE,
    TASK_LIST,
    TASK_REMOVE,
)
from .core.logging_config import setup_logging
from .core.repl import repl
from .core.tasks import add_task, clear_tasks, list_tasks, mark_done, remove_task

logger = logging.getLogger(__name__)


def parse_args():
    """
    Parse command line arguments.

    :returns: A tuple containing the parser and the parsed arguments.
    :rtype: tuple
    """
    parser = ArgumentParser(description="Simple To-Do List Manager")
    parser.add_argument(
        "--file", type=str, default=DEFAULT_TODO_FILE, help="The to-do list file"
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

    add_parser = subparsers.add_parser(TASK_ADD, help="Add a new task")
    add_parser.add_argument("task", type=str, help="The task to add")

    remove_parser = subparsers.add_parser(TASK_REMOVE, help="Remove a task by index")
    remove_parser.add_argument(
        "index", type=int, help="The index of the task to remove"
    )

    done_parser = subparsers.add_parser(TASK_DONE, help="Mark a task as done by index")
    done_parser.add_argument(
        "index", type=int, help="The index of the task to mark as done"
    )

    subparsers.add_parser(TASK_LIST, help="List all tasks")

    subparsers.add_parser(TASK_CLEAR, help="Clear all tasks")

    parser.add_argument("--repl", action="store_true", help="Enter REPL mode")

    return parser, parser.parse_args()


def run():
    """
    Main function to run the cli application.

    :returns: None
    """
    setup_logging(default_level=logging.DEBUG)
    parser, args = parse_args()

    if args.repl:
        repl(args.file)
    elif args.command == TASK_ADD:
        add_task(args.task, args.file)
    elif args.command == TASK_REMOVE:
        remove_task(args.index, args.file)
    elif args.command == TASK_DONE:
        mark_done(args.index, args.file)
    elif args.command == TASK_LIST:
        list_tasks(args.file)
    elif args.command == TASK_CLEAR:
        clear_tasks(args.clear)
    else:
        parser.print_help()


if __name__ == "__main__":
    run()
