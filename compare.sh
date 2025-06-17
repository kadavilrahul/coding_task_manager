#!/bin/bash

# Interactive script to count and compare total lines of code in multiple codebases
# Uses: find /path/to/folder -type f -exec wc -l {} + | tail -n 1

# Output file for results
OUTPUT_FILE="codebase_line_counts.txt"

# Clear the output file and add header
echo "Codebase Line Count Comparison" > "$OUTPUT_FILE"
echo "Generated on: $(date)" >> "$OUTPUT_FILE"
echo "======================================" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "Interactive Codebase Line Counter"
echo "================================="
echo "This script will count total lines of code in multiple codebases."
echo "Results will be saved to: $OUTPUT_FILE"
echo ""

# Counter for codebase number
counter=1

while true; do
    echo "Codebase #$counter"
    echo "-------------"
    
    # Get folder path from user
    read -p "Enter the path to codebase folder (or 'quit' to finish): " folder_path
    
    # Check if user wants to quit
    if [[ "$folder_path" == "quit" || "$folder_path" == "q" ]]; then
        break
    fi
    
    # Check if folder exists
    if [[ ! -d "$folder_path" ]]; then
        echo "Error: Directory '$folder_path' does not exist!"
        echo "Please try again."
        echo ""
        continue
    fi
    
    # Use folder name as codebase name
    codebase_name=$(basename "$folder_path")
    
    # Count lines using the specified command
    line_count=$(find "$folder_path" -type f -exec wc -l {} + 2>/dev/null | tail -n 1 | awk '{print $1}')
    
    # Check if count was successful
    if [[ -z "$line_count" || "$line_count" == "0" ]]; then
        echo "Warning: No files found or unable to count lines in '$folder_path'"
        line_count="0"
    fi
    
    # Format the result
    result="$codebase_name: $line_count lines"
    
    # Display result
    echo "Result: $result"
    
    # Save to file
    echo "$result" >> "$OUTPUT_FILE"
    echo "  Path: $folder_path" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    
    echo "Result saved to $OUTPUT_FILE"
    echo ""
    
    # Increment counter
    ((counter++))
done

echo ""
echo "Summary saved to: $OUTPUT_FILE"
echo ""

# Display final summary
if [[ -f "$OUTPUT_FILE" ]]; then
    echo "Final Results:"
    echo "=============="
    cat "$OUTPUT_FILE"
fi

echo ""
echo "Script completed!"
