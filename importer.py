import os

def import_tasks(task_file):
    """Imports tasks from an existing task file."""
    try:
        with open(task_file, "r") as f:
            tasks = f.readlines()
    except FileNotFoundError:
        print(f"Error: Task file '{task_file}' not found.")
        return

    with open("tasks.txt", "a") as f:
        for task in tasks:
            f.write(task)

    print(f"Tasks imported successfully from '{task_file}'.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Task importer")
    parser.add_argument("task_file", help="Path to the task file to import")
    args = parser.parse_args()

    import_tasks(args.task_file)