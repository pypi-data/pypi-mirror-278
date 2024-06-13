#!/usr/bin/env python3

import logging

from .helpers import format_todo, index_in_range, load_todos, save_todos

logger = logging.getLogger(__name__)


def add_task(task, file):
    """
    Add a task to the to-do list.

    :param task: The task to add.
    :type task: str
    :param file: The file where the to-do list is stored.
    :type file: str
    """
    todos = load_todos(file)
    todos.append({"task": task, "done": False})
    save_todos(todos, file)
    print(f"Added task: {task}")


def clear_tasks(file):
    """
    Clear all tasks from the to-do list.

    :param file: The file where the to-do list is stored.
    :type file: str
    """
    # Ask for confirmation before clearing all tasks
    confirm = input("Are you sure you want to clear all tasks? (yes/no) ")
    if confirm.lower() != "yes":
        print("Clearing all tasks aborted.")
        return

    save_todos([], file)
    print("Cleared all tasks.")


def list_tasks(file):
    """
    List all tasks in the to-do list.

    :param file: The file where the to-do list is stored.
    :type file: str
    """
    todos = load_todos(file)

    if not todos:
        print("No tasks in the list.")
        return

    padding = len(str(len(todos)))

    for i, todo in enumerate(todos):
        print(format_todo(todo, i, padding))


def mark_done(index, file):
    """
    Mark a task as done.

    :param index: The index of the task to mark as done.
    :type index: int
    :param file: The file where the to-do list is stored.
    :type file: str
    """
    todos = load_todos(file)

    if not index_in_range(index, todos):
        return

    todos[index]["done"] = True
    save_todos(todos, file)
    print(f"Marked task as done: {todos[index]['task']}")


def remove_task(index, file):
    """
    Remove a task from the to-do list.

    :param index: The index of the task to remove.
    :type index: int
    :param file: The file where the to-do list is stored.
    :type file: str
    """
    todos = load_todos(file)

    if not index_in_range(index, todos):
        return

    removed_task = todos.pop(index)
    save_todos(todos, file)
    print(f"Removed task: {removed_task['task']}")
