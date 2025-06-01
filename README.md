# Task Management Tool

This is a simple task management tool implemented in Python. It allows you to add, list, update, and remove tasks, as well as parse Product Requirements Documents (PRDs) to automatically generate tasks.

This tool is designed to be used within a coding project. The `new_repo` folder, which contains all the files for this tool, should be placed in the root directory of your coding project.

## Installation

## What is a PRD File?

A PRD (Product Requirements Document) file is a document that describes the purpose, features, functionality, and behavior of a software product. It is used to communicate the requirements of the product to the development team.

## Creating a PRD File

A PRD (Product Requirements Document) file is a text-based document that you create to describe the features and functionality of your software. You can use any text editor to create a PRD file. The PRD file can be a plain text file (`.txt`), a Markdown file (`.md`), or a similar text-based format. The PRD file should follow the format described below.
It can be located in any directory. However, you will need to provide the correct path to the prd_parser.py script when you run it.

## Sample PRD File Format

```
## Task 1: Implement user authentication
- Create login page
- Create registration page
- Implement password reset functionality

## Task 2: Implement task management features
- Add task
- List tasks
- Update task
- Remove task
```

## Usage

1.  **Parse a PRD file:**

    `python3 prd_parser.py <prd_file>`

    This will parse the PRD file and generate tasks in the `tasks.txt` file.
2.  **Manage tasks:**

    `python3 task_manager.py <command> [options]`

    Available commands:

    *   `add`: Add a new task.
        *   `--task_name <task_name>`: The name of the task.
    *   `add_subtask`: Add a new subtask to a parent task.
        *   `--task_name <task_name>`: The name of the subtask.
        *   `--parent_task <parent_task_id>`: The ID of the parent task.
    *   `list`: List all tasks.
    *   `update`: Update an existing task.
        *   `--task_id <task_id>`: The ID of the task to update.
        *   `--new_task_name <new_task_name>`: The new name of the task.
    *   `remove`: Remove a task.
        *   `--task_id <task_id>`: The ID of the task to remove.
    *   `update_subtask`: Update an existing subtask.
        *   `--task_id <task_id>`: The ID of the subtask to update.
        *   `--new_task_name <new_task_name>`: The new name of the subtask.
    *   `remove_subtask`: Remove a subtask.
        *   `--task_id <task_id>`: The ID of the subtask to remove.
3.  **Analyze task complexity:**

    `python3 complexity_analyzer.py <task_name>`

    This will analyze the complexity of the task and print the result.
4.  **Expand a task:**

    `python3 task_expander.py <task_id> "<subtask1>" "<subtask2>" ...`

    This will expand the task with the specified ID into the given subtasks.
5.  **Generate a task file:**

    `python3 task_generator.py <task_id>`

    This will generate a task file with the task description.
6.  **Import tasks from an existing task file:**

    `python3 importer.py <task_file>`

    This will import tasks from the specified task file.

## Task File Format

The `tasks.txt` file is a plain text file where each line represents a task or subtask. The format of each line is:

`<task_id> | <task_name>`

Subtasks are indented with two spaces.

