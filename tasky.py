"""Simple CLI task tracker."""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List


DATA_FILE = Path("tasks.json")


@dataclass
class Task:
    """Represents a task entry."""

    id: int
    description: str
    completed: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(id=data["id"], description=data["description"], completed=data.get("completed", False))


def load_tasks(path: Path = DATA_FILE) -> List[Task]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        raw_tasks = json.load(f)
    return [Task.from_dict(item) for item in raw_tasks]


def save_tasks(tasks: List[Task], path: Path = DATA_FILE) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump([asdict(task) for task in tasks], f, indent=2)


def add_task(description: str) -> Task:
    tasks = load_tasks()
    next_id = max((task.id for task in tasks), default=0) + 1
    task = Task(id=next_id, description=description)
    tasks.append(task)
    save_tasks(tasks)
    return task


def list_tasks(show_all: bool = False) -> List[Task]:
    tasks = load_tasks()
    if show_all:
        return tasks
    return [task for task in tasks if not task.completed]


def complete_task(task_id: int) -> Task:
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.completed = True
            save_tasks(tasks)
            return task
    raise ValueError(f"Task with id {task_id} not found")


def delete_task(task_id: int) -> Task:
    tasks = load_tasks()
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            removed = tasks.pop(idx)
            save_tasks(tasks)
            return removed
    raise ValueError(f"Task with id {task_id} not found")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Tasky - simple CLI task tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Description of the task")

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--all", action="store_true", dest="show_all", help="Include completed tasks")

    done_parser = subparsers.add_parser("done", help="Mark a task as complete")
    done_parser.add_argument("id", type=int, help="ID of the task to mark as complete")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="ID of the task to delete")

    return parser


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "add":
        task = add_task(args.description)
        print(f"Added task {task.id}: {task.description}")
    elif args.command == "list":
        tasks = list_tasks(show_all=args.show_all)
        if not tasks:
            print("No tasks found." if args.show_all else "No pending tasks!")
            return
        for task in tasks:
            status = "✓" if task.completed else " "
            print(f"[{status}] {task.id}: {task.description}")
    elif args.command == "done":
        try:
            task = complete_task(args.id)
        except ValueError as exc:
            parser.error(str(exc))
        else:
            print(f"Marked task {task.id} as complete")
    elif args.command == "delete":
        try:
            task = delete_task(args.id)
        except ValueError as exc:
            parser.error(str(exc))
        else:
            print(f"Deleted task {task.id}: {task.description}")


if __name__ == "__main__":
    main()
