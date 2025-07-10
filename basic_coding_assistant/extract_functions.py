import ast
import os

def get_functions(filename):
    with open(filename, "r") as f:
        tree = ast.parse(f.read())
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(f"{node.name} (line {node.lineno})")
    return functions

def process_directory(directory):
    all_functions = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                all_functions.extend(get_functions(filepath))
    return all_functions

if __name__ == "__main__":
    functions = process_directory(".")
    with open(os.path.join(os.path.dirname(__file__), "functions.txt"), "w") as f:
        for func in functions:
            f.write(func + "\n")