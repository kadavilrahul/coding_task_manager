import os
import uuid

def expand_task(task_id, subtasks):
    """Expands a task into smaller, more manageable subtasks."""
    try:
        with open("tasks.txt", "r") as f:
            tasks = f.readlines()
    except FileNotFoundError:
        print("Error: tasks.txt file not found.")
        return

    for i, task in enumerate(tasks):
        if task.startswith(task_id):
            task_name = task.split("|")[1].strip()
            print(f"Expanding task '{task_name}' into subtasks:")
            for subtask in subtasks:
                print(f"- {subtask}")

            with open("tasks.txt", "r") as f:
                tasks = f.readlines()

            for i, task in enumerate(tasks):
                task_id_in_file = task.split("|")[0].strip()
                if task_id_in_file == task_id:
                    for subtask in subtasks:
                        subtask_id = str(uuid.uuid4())
                        tasks.insert(i + 1, f"  {subtask_id} | {subtask}{os.linesep}")
                    break
            else:
                print(f"Error: Task with ID '{task_id}' not found.")
                return

            with open("tasks.txt", "w") as f:
                f.writelines(tasks)
            break
    else:
        print(f"Error: Task with ID '{task_id}' not found.")
        return

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Task expander")
    parser.add_argument("task_id", help="ID of the task to expand")
    parser.add_argument("subtasks", nargs="+", help="Subtasks to add to the task")
    args = parser.parse_args()

    expand_task(args.task_id, args.subtasks)