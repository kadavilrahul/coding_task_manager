import os

def add_task(task_name, parent_task=None):
    """Adds a new task to the tasks.txt file."""
    task_id = generate_task_id()
    task_string = f"{task_id} | {task_name}"
    if parent_task:
        task_string = f"  {task_string}"
    with open("tasks.txt", "a") as f:
        f.write(task_string + os.linesep)
    print(f"Task '{task_name}' added successfully.")

def add_subtask(task_name, parent_task_id):
    """Adds a new subtask to the tasks.txt file under the specified parent task."""
    with open("tasks.txt", "r") as f:
        tasks = f.readlines()
    for i, task in enumerate(tasks):
        task_id = task.split("|")[0].strip()
        if task_id == parent_task_id:
            subtask_id = generate_task_id()
            subtask_string = f"  {subtask_id} | {task_name}"
            tasks.insert(i + 1, subtask_string + os.linesep)
            break
    else:
        print(f"Task with ID '{parent_task_id}' not found.")
        return
    with open("tasks.txt", "w") as f:
        f.writelines(tasks)
    print(f"Subtask '{task_name}' added successfully to task '{parent_task_id}'.")

def list_tasks():
    """Lists all tasks and subtasks from the tasks.txt file."""
    with open("tasks.txt", "r") as f:
        tasks = f.readlines()
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        if task.startswith("  "):
            print("  " + task.strip())
        else:
            print(task.strip())

def update_task(task_id, new_task_name):
    """Updates the name of an existing task in the tasks.txt file."""
    with open("tasks.txt", "r") as f:
        tasks = f.readlines()
    for i, task in enumerate(tasks):
        task_id_in_file = task.split("|")[0].strip()
        if task_id_in_file == task_id:
            tasks[i] = task.replace(task.split("|")[1].strip(), new_task_name)
            break
    else:
        print(f"Task with ID '{task_id}' not found.")
        return
    with open("tasks.txt", "w") as f:
        f.writelines(tasks)
    print(f"Task '{task_id}' updated successfully.")

def update_subtask(task_id, new_task_name):
    """Updates the name of an existing subtask in the tasks.txt file."""
    with open("tasks.txt", "r") as f:
        tasks = f.readlines()
    for i, task in enumerate(tasks):
        task_id_in_file = task.split("|")[0].strip()
        if task_id_in_file == task_id:
            tasks[i] = task.replace(task.split("|")[1].strip(), new_task_name)
            break
    else:
        print(f"Task with ID '{task_id}' not found.")
        return
    with open("tasks.txt", "w") as f:
        f.writelines(tasks)
    print(f"Task '{task_id}' updated successfully.")

def remove_subtask(task_id):
    """Removes a subtask from the tasks.txt file."""
    with open("tasks.txt", "r") as f:
        tasks = f.readlines()
    for i, task in enumerate(tasks):
        task_id_in_file = task.split("|")[0].strip()
        if task_id_in_file == task_id:
            del tasks[i]
            break
    else:
        print(f"Task with ID '{task_id}' not found.")
        return
    with open("tasks.txt", "w") as f:
        f.writelines(tasks)
    print(f"Task '{task_id}' removed successfully.")

def remove_task(task_id):
    """Removes a task from the tasks.txt file."""
    with open("tasks.txt", "r") as f:
        tasks = f.readlines()
    for i, task in enumerate(tasks):
        if task.startswith(task_id):
            del tasks[i]
            break
    else:
        print(f"Task with ID '{task_id}' not found.")
        return
    with open("tasks.txt", "w") as f:
        f.writelines(tasks)
    print(f"Task '{task_id}' removed successfully.")

def generate_task_id():
    """Generates a unique task ID."""
    import uuid
    return str(uuid.uuid4())

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Task management tool")
    parser.add_argument("command", help="Command to execute (add, list, update, remove)")
    parser.add_argument("--task_name", help="Task name")
    parser.add_argument("--parent_task", help="Parent task ID")
    parser.add_argument("--task_id", help="Task ID")
    parser.add_argument("--new_task_name", help="New task name")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.task_name, args.parent_task)
    elif args.command == "list":
        list_tasks()
    elif args.command == "update":
        update_task(args.task_id, args.new_task_name)
    elif args.command == "remove":
        remove_task(args.task_id)
    elif args.command == "add_subtask":
        add_subtask(args.task_name, args.parent_task)
    elif args.command == "update_subtask":
        update_subtask(args.task_id, args.new_task_name)
    elif args.command == "remove_subtask":
        remove_subtask(args.task_id)
    else:
        print("Invalid command.")