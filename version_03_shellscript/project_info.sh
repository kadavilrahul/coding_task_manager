#!/bin/bash

set -e  # Exit on any error

# Function to cleanup temporary files
cleanup() {
    rm -f project_structure.txt sensitive_info.txt line_counts.txt
}

# Set trap to cleanup on exit
trap cleanup EXIT

echo "Gathering project information..."

# Check if an argument is provided
if [ -z "$1" ]; then
    directory="."
else
    directory="$1"
fi

# Search for sensitive information
echo "Scanning for sensitive information..."
{
    echo "=== Sensitive Information Scan ==="
    grep -i -r --exclude="sensitive_info.txt" --exclude="project_info.txt" \
         -E "(API_KEY|SECRET|PASSWORD|TOKEN|DATABASE_URL)" "$directory" 2>/dev/null || echo "No sensitive patterns found"
} > sensitive_info.txt

# Count lines of code for various file types
echo "Counting lines of code..."
{
    echo "=== Line Counts ==="
    find "$directory" -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.java" \
                     -o -name "*.c" -o -name "*.cpp" -o -name "*.sh" -o -name "*.go" \
                     -o -name "*.rb" -o -name "*.php" \) -exec wc -l {} + 2>/dev/null || echo "No code files found"
} > line_counts.txt

# Prompt for project description with validation
while true; do
    read -p "Enter a brief description of the project: " project_description
    if [[ -n "$project_description" ]]; then
        break
    else
        echo "Please enter a non-empty description."
    fi
done

# Store project information
echo "Creating project_info.txt..."
{
    echo "=== PROJECT INFORMATION ==="
    echo "Generated on: $(date)"
    echo "Project Description: $project_description"
    echo ""
    cat sensitive_info.txt
    echo ""
    cat line_counts.txt
} > project_info.txt

echo "Project information saved to project_info.txt"