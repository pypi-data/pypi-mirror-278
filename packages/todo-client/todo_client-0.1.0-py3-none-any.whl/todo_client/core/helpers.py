#!/usr/bin/env python3

import logging

import yaml

logger = logging.getLogger(__name__)


def format_todo(todo, index, padding=1):
    """
    Format a to-do item for display.

    :param todo: The to-do item.
    :type todo: dict
    :param index: The index of the to-do item.
    :type index: int
    :param padding: The padding for the index.
    :type padding: int
    :returns: The formatted to-do item.
    :rtype: str
    """
    status = "x" if todo["done"] else " "
    return f"{index:>{padding}}: [{status}] {todo['task']}"


def index_in_range(index, todos):
    """
    Check if an index is in the range of the to-do list.

    :param index: The index to check.
    :type index: int
    :param todos: The to-do list.
    :type todos: list
    :returns: True if the index is in range, False otherwise.
    :rtype: bool
    """
    if index < 0 or index >= len(todos):
        print(f"Task index {index} is out of range.")
        return False
    return True


def load_todos(file):
    """
    Load the to-do list from a file.

    :param file: The file to load from.
    :type file: str
    :returns: The loaded to-do list.
    :rtype: list
    """
    try:
        with open(file, "r") as f:
            return yaml.safe_load(f) or []
    except FileNotFoundError:
        logger.info(f"The file {file} was not found. Starting with an empty list.")
        return []
    except Exception as e:
        logger.error(f"Failed to load file {file}: {e}")
        return []


def save_todos(todos, file):
    """
    Save the to-do list to a file.

    :param todos: The to-do list to save.
    :type todos: list
    :param file: The file to save to.
    :type file: str
    """
    try:
        with open(file, "w") as f:
            yaml.safe_dump(todos, f)
    except Exception as e:
        logger.error(f"Failed to save file {file}: {e}")
