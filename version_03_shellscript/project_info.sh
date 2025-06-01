#!/bin/bash

# List files and directories
tree . > project_structure.txt

# Search for sensitive information
grep -i -r "API_KEY" . > sensitive_info.txt
grep -i -r "database_url" . >> sensitive_info.txt

# Count lines of code
find . -name "*.py" -o -name "*.js" | xargs wc -l > line_counts.txt

# Prompt for project description
read -p "Enter a brief description of the project: " project_description

# Store project information
echo "Project Description: $project_description" > project_info.txt
cat project_structure.txt >> project_info.txt
cat sensitive_info.txt >> project_info.txt
cat line_counts.txt >> project_info.txt

echo "Project information saved to project_info.txt"