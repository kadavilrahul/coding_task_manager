import os
import uuid
import re

def parse_prd(prd_file):
    """Parses a PRD file and generates tasks in the tasks.txt file."""
    try:
        with open(prd_file, "r") as f:
            prd_content = f.read()
    except FileNotFoundError:
        print(f"Error: PRD file '{prd_file}' not found.")
        return

    tasks = []
    for task_match in re.finditer(r"## (.*?)\n((?:- .*?\n)*)", prd_content):
        task_name = task_match.group(1).strip()
        subtask_lines = task_match.group(2).strip().splitlines()
        subtasks = [line.strip().lstrip("-").strip() for line in subtask_lines]
        tasks.append({"name": task_name, "subtasks": subtasks})

    with open("/root/claude-task-master/new_repo/tasks.txt", "w") as f:
        for task in tasks:
            task_id = str(uuid.uuid4())
            f.write(f"{task_id} | {task['name']}{os.linesep}")
            for subtask in task["subtasks"]:
                subtask_id = str(uuid.uuid4())
                f.write(f"  {subtask_id} | {subtask}{os.linesep}")

    print("PRD parsed successfully and tasks generated in tasks.txt.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PRD parser")
    parser.add_argument("prd_file", help="Path to the PRD file")
    args = parser.parse_args()

    parse_prd(args.prd_file)