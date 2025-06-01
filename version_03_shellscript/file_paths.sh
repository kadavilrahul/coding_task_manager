#!/bin/bash

set -e  # Exit on any error

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS] [PATTERN]"
    echo "Search for files in the current directory and subdirectories"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -t, --type     File type filter (e.g., py, js, txt)"
    echo "  -i, --ignore   Ignore case in pattern matching"
    echo "  -e, --exact    Exact filename match"
    echo ""
    echo "Examples:"
    echo "  $0 main.py              # Find files containing 'main.py'"
    echo "  $0 -t py main           # Find Python files containing 'main'"
    echo "  $0 -i README            # Case-insensitive search for 'README'"
    echo "  $0 -e config.json       # Exact match for 'config.json'"
}

# Initialize variables
file_pattern=""
file_type=""
ignore_case=false
exact_match=false
interactive=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -t|--type)
            file_type="$2"
            shift 2
            ;;
        -i|--ignore)
            ignore_case=true
            shift
            ;;
        -e|--exact)
            exact_match=true
            shift
            ;;
        -*)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            file_pattern="$1"
            shift
            ;;
    esac
done

# If no pattern provided, enter interactive mode
if [[ -z "$file_pattern" ]]; then
    interactive=true
    echo "=== File Path Search Tool ==="
    echo "Enter a file name or pattern to search for:"
    read -p "> " file_pattern
    
    if [[ -z "$file_pattern" ]]; then
        echo "No pattern provided. Listing all files..."
        file_pattern="."
    fi
fi

# Create temporary file for results
temp_file=$(mktemp)
trap "rm -f $temp_file" EXIT

echo "Searching for files..."

# Build find command based on options
find_cmd="find . -type f"

# Add file type filter if specified
if [[ -n "$file_type" ]]; then
    find_cmd="$find_cmd -name \"*.$file_type\""
fi

# Execute find and store results
eval "$find_cmd" > "$temp_file"

# Apply pattern filtering
if [[ "$exact_match" == true ]]; then
    # Exact filename match
    if [[ "$ignore_case" == true ]]; then
        grep -i "/$file_pattern$" "$temp_file" || echo "No exact matches found for '$file_pattern'"
    else
        grep "/$file_pattern$" "$temp_file" || echo "No exact matches found for '$file_pattern'"
    fi
elif [[ "$ignore_case" == true ]]; then
    # Case-insensitive pattern match
    grep -i "$file_pattern" "$temp_file" || echo "No matches found for '$file_pattern' (case-insensitive)"
else
    # Regular pattern match
    grep "$file_pattern" "$temp_file" || echo "No matches found for '$file_pattern'"
fi

# If interactive mode, offer additional options
if [[ "$interactive" == true ]]; then
    echo ""
    echo "Would you like to:"
    echo "1. Search again with a different pattern"
    echo "2. Show file details (size, date)"
    echo "3. Exit"
    read -p "Choose an option (1-3): " choice
    
    case $choice in
        1)
            exec "$0"  # Restart the script
            ;;
        2)
            echo "File details:"
            if [[ "$ignore_case" == true ]]; then
                grep -i "$file_pattern" "$temp_file" | head -20 | xargs ls -la 2>/dev/null || echo "Could not get file details"
            else
                grep "$file_pattern" "$temp_file" | head -20 | xargs ls -la 2>/dev/null || echo "Could not get file details"
            fi
            ;;
        3)
            echo "Goodbye!"
            ;;
        *)
            echo "Invalid option"
            ;;
    esac
fi