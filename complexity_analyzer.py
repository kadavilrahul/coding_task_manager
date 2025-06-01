import os

def analyze_complexity(task_name):
    """Analyzes the complexity of a task based on its description."""
    try:
        with open("tasks.txt", "r") as f:
            tasks = f.readlines()
    except FileNotFoundError:
        print("Error: tasks.txt file not found.")
        return

    task_description = None
    for task in tasks:
        task_parts = task.split("|")
        if len(task_parts) > 1:
            task_name_in_file = task_parts[1].strip()
            if task_name_in_file == task_name:
                task_description = task_name_in_file
                break
    else:
        print(f"Error: Task with name '{task_name}' not found.")
        return

    # Basic complexity analysis (can be improved with more sophisticated methods)
    word_count = len(task_description.split())
    if word_count < 5:
        complexity = "Simple"
    elif word_count < 10:
        complexity = "Medium"
    else:
        complexity = "Complex"

    print(f"Task '{task_description}' has a complexity of: {complexity}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Task complexity analyzer")
    parser.add_argument("task_name", help="Name of the task to analyze")
    args = parser.parse_args()

    analyze_complexity(args.task_name)