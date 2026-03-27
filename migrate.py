#!/usr/bin/env python3
"""Migrate between todo.txt and todo.txt.d formats."""

import argparse
import os
import sys


def read_tasks(filepath):
    """Read non-empty lines from a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return [line for line in f.read().splitlines() if line.strip()]


def to_d(todo_path, done_path, output_dir):
    """Convert todo.txt (and optionally done.txt) to todo.txt.d/ directory."""
    if os.path.exists(output_dir):
        print(f"Error: '{output_dir}' already exists.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir)
    count = 0

    if todo_path:
        tasks = read_tasks(todo_path)
        for i, task in enumerate(tasks, 1):
            filename = f"task-{i:04d}.txt"
            with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
                f.write(task + "\n")
            count += 1

    if done_path:
        done_dir = os.path.join(output_dir, "done.txt.d")
        os.makedirs(done_dir)
        done_tasks = read_tasks(done_path)
        for i, task in enumerate(done_tasks, 1):
            filename = f"done-{i:04d}.txt"
            with open(os.path.join(done_dir, filename), "w", encoding="utf-8") as f:
                f.write(task + "\n")
            count += 1

    print(f"Migrated {count} tasks to '{output_dir}'.")


def from_d(input_dir, todo_path, done_path):
    """Convert todo.txt.d/ directory to todo.txt (and optionally done.txt)."""
    if not os.path.isdir(input_dir):
        print(f"Error: '{input_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    if os.path.exists(todo_path):
        print(f"Error: '{todo_path}' already exists.", file=sys.stderr)
        sys.exit(1)

    done_dir = os.path.join(input_dir, "done.txt.d")
    has_done = os.path.isdir(done_dir)
    if has_done and os.path.exists(done_path):
        print(f"Error: '{done_path}' already exists.", file=sys.stderr)
        sys.exit(1)

    # Collect tasks from .txt files (excluding done.txt.d/)
    tasks = []
    for name in sorted(os.listdir(input_dir)):
        filepath = os.path.join(input_dir, name)
        if os.path.isfile(filepath) and name.endswith(".txt"):
            tasks.extend(read_tasks(filepath))

    with open(todo_path, "w", encoding="utf-8") as f:
        for task in tasks:
            f.write(task + "\n")

    count = len(tasks)

    # Collect done tasks
    if has_done:
        done_tasks = []
        for name in sorted(os.listdir(done_dir)):
            filepath = os.path.join(done_dir, name)
            if os.path.isfile(filepath) and name.endswith(".txt"):
                done_tasks.extend(read_tasks(filepath))

        with open(done_path, "w", encoding="utf-8") as f:
            for task in done_tasks:
                f.write(task + "\n")
        count += len(done_tasks)

    print(f"Migrated {count} tasks to '{todo_path}'" + (f" and '{done_path}'" if has_done else "") + ".")


def main():
    parser = argparse.ArgumentParser(description="Migrate between todo.txt and todo.txt.d formats.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # todo.txt -> todo.txt.d
    to_d_parser = subparsers.add_parser("to-d", help="Convert todo.txt to todo.txt.d/ directory.")
    to_d_parser.add_argument("todo", help="Path to todo.txt file.")
    to_d_parser.add_argument("-d", "--done", help="Path to done.txt file (optional).")
    to_d_parser.add_argument("-o", "--output", default="todo.txt.d", help="Output directory (default: todo.txt.d).")

    # todo.txt.d -> todo.txt
    from_d_parser = subparsers.add_parser("from-d", help="Convert todo.txt.d/ directory to todo.txt.")
    from_d_parser.add_argument("directory", help="Path to todo.txt.d/ directory.")
    from_d_parser.add_argument("-o", "--output", default="todo.txt", help="Output file (default: todo.txt).")
    from_d_parser.add_argument("-d", "--done", default="done.txt", help="Output done file (default: done.txt).")

    args = parser.parse_args()

    if args.command == "to-d":
        to_d(args.todo, args.done, args.output)
    elif args.command == "from-d":
        from_d(args.directory, args.output, args.done)


if __name__ == "__main__":
    main()
