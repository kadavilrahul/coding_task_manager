import os

def generate_task_file(task_id):
    """Generates a task file or template based on the task ID."""
    try:
        with open("tasks.txt", "r") as f:
            tasks = f.readlines()
    except FileNotFoundError:
        print("Error: tasks.txt file not found.")
        return

    task_description = None
    for task in tasks:
        if task.startswith(task_id):
            task_description = task.split("|")[1].strip()
            break
    else:
        print(f"Error: Task with ID '{task_id}' not found.")
        return

    file_name = f"{task_id}.txt"
    file_content = f"Task: {task_description}\\n\\n# Implementation details\\n"

    try:
        with open(file_name, "w") as f:
            f.write(file_content)
        print(f"Task file '{file_name}' generated successfully.")
    except Exception as e:
        print(f"Error: Could not generate task file: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Task file generator")
    parser.add_argument("task_id", help="ID of the task to generate a file for")
    args = parser.parse_args()

    generate_task_file(args.task_id)