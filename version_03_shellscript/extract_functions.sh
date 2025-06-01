#!/bin/bash

# Example for Python (adjust for other languages)
tree-sitter parse python_file.py -q '(function_definition name: (identifier) @name) @function' |
  while read -r line; do
    function_name=$(echo "$line" | awk '{print $2}')
    # Extract function code (requires more sophisticated parsing)
    # For simplicity, let's just create an empty file with the function name
    touch "$function_name.txt"
    echo "Function $function_name extracted to $function_name.txt"
  done