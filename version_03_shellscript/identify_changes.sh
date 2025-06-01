#!/bin/bash

set -e  # Exit on any error

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS] <original_file> <modified_file>"
    echo "Identify and analyze changes between two files"
    echo ""
    echo "Options:"
    echo "  -h, --help        Show this help message"
    echo "  -u, --unified     Show unified diff format (default)"
    echo "  -s, --side-by-side Show side-by-side comparison"
    echo "  -c, --context     Number of context lines (default: 3)"
    echo "  -i, --ignore-case Ignore case differences"
    echo "  -w, --ignore-whitespace Ignore whitespace differences"
    echo "  -o, --output      Save diff to file"
    echo "  -f, --format      Output format: diff|html|json (default: diff)"
    echo "  --stats           Show change statistics"
    echo ""
    echo "Examples:"
    echo "  $0 old_file.py new_file.py"
    echo "  $0 -s -c 5 original.js modified.js"
    echo "  $0 --stats -o changes.diff file1.txt file2.txt"
}

# Function to generate HTML diff
generate_html_diff() {
    local original="$1"
    local modified="$2"
    local output="$3"
    
    cat > "$output" << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>File Comparison</title>
    <style>
        body { font-family: monospace; margin: 20px; }
        .diff-container { display: flex; }
        .diff-column { flex: 1; margin: 0 10px; }
        .diff-header { background: #f0f0f0; padding: 10px; font-weight: bold; }
        .line { padding: 2px 5px; white-space: pre; }
        .added { background-color: #d4edda; }
        .removed { background-color: #f8d7da; }
        .unchanged { background-color: #f8f9fa; }
        .line-number { color: #666; margin-right: 10px; }
    </style>
</head>
<body>
    <h1>File Comparison</h1>
    <div class="diff-container">
        <div class="diff-column">
            <div class="diff-header">Original: $(basename "$original")</div>
EOF
    
    # Add original file content with line numbers
    nl -ba "$original" | while IFS=$'\t' read -r num line; do
        echo "            <div class=\"line unchanged\"><span class=\"line-number\">$num</span>$line</div>" >> "$output"
    done
    
    cat >> "$output" << EOF
        </div>
        <div class="diff-column">
            <div class="diff-header">Modified: $(basename "$modified")</div>
EOF
    
    # Add modified file content with line numbers
    nl -ba "$modified" | while IFS=$'\t' read -r num line; do
        echo "            <div class=\"line unchanged\"><span class=\"line-number\">$num</span>$line</div>" >> "$output"
    done
    
    cat >> "$output" << 'EOF'
        </div>
    </div>
</body>
</html>
EOF
}

# Function to generate JSON diff
generate_json_diff() {
    local original="$1"
    local modified="$2"
    local output="$3"
    
    # Create a simple JSON structure with file info and diff
    {
        echo "{"
        echo "  \"comparison\": {"
        echo "    \"original_file\": \"$original\","
        echo "    \"modified_file\": \"$modified\","
        echo "    \"timestamp\": \"$(date -Iseconds)\","
        echo "    \"diff_command\": \"diff -u '$original' '$modified'\""
        echo "  },"
        echo "  \"changes\": ["
        
        # Process diff output into JSON format
        diff -u "$original" "$modified" | while IFS= read -r line; do
            case "${line:0:1}" in
                "+")
                    echo "    {\"type\": \"added\", \"content\": $(echo "${line:1}" | jq -R .)},"
                    ;;
                "-")
                    echo "    {\"type\": \"removed\", \"content\": $(echo "${line:1}" | jq -R .)},"
                    ;;
                " ")
                    echo "    {\"type\": \"unchanged\", \"content\": $(echo "${line:1}" | jq -R .)},"
                    ;;
                "@")
                    echo "    {\"type\": \"context\", \"content\": $(echo "$line" | jq -R .)},"
                    ;;
            esac
        done | sed '$ s/,$//'  # Remove trailing comma
        
        echo "  ]"
        echo "}"
    } > "$output"
}

# Function to show change statistics
show_statistics() {
    local original="$1"
    local modified="$2"
    
    echo "=== CHANGE STATISTICS ==="
    echo "Original file: $original"
    echo "Modified file: $modified"
    echo ""
    
    # File sizes
    if [[ -f "$original" ]]; then
        echo "Original size: $(wc -c < "$original") bytes, $(wc -l < "$original") lines"
    fi
    if [[ -f "$modified" ]]; then
        echo "Modified size: $(wc -c < "$modified") bytes, $(wc -l < "$modified") lines"
    fi
    echo ""
    
    # Diff statistics
    local diff_output
    diff_output=$(diff -u "$original" "$modified" 2>/dev/null || true)
    
    local added_lines removed_lines
    added_lines=$(echo "$diff_output" | grep -c "^+" || echo "0")
    removed_lines=$(echo "$diff_output" | grep -c "^-" || echo "0")
    
    # Subtract the +++ and --- lines
    if [[ $added_lines -gt 0 ]]; then
        ((added_lines--))
    fi
    if [[ $removed_lines -gt 0 ]]; then
        ((removed_lines--))
    fi
    
    echo "Lines added: $added_lines"
    echo "Lines removed: $removed_lines"
    echo "Net change: $((added_lines - removed_lines)) lines"
    echo ""
}

# Initialize variables
original_file=""
modified_file=""
diff_format="unified"
context_lines=3
ignore_case=false
ignore_whitespace=false
output_file=""
output_format="diff"
show_stats=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -u|--unified)
            diff_format="unified"
            shift
            ;;
        -s|--side-by-side)
            diff_format="side-by-side"
            shift
            ;;
        -c|--context)
            context_lines="$2"
            if ! [[ "$context_lines" =~ ^[0-9]+$ ]]; then
                echo "Error: Context lines must be a number"
                exit 1
            fi
            shift 2
            ;;
        -i|--ignore-case)
            ignore_case=true
            shift
            ;;
        -w|--ignore-whitespace)
            ignore_whitespace=true
            shift
            ;;
        -o|--output)
            output_file="$2"
            shift 2
            ;;
        -f|--format)
            output_format="$2"
            if [[ "$output_format" != "diff" && "$output_format" != "html" && "$output_format" != "json" ]]; then
                echo "Error: Format must be 'diff', 'html', or 'json'"
                exit 1
            fi
            shift 2
            ;;
        --stats)
            show_stats=true
            shift
            ;;
        -*)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            if [[ -z "$original_file" ]]; then
                original_file="$1"
            elif [[ -z "$modified_file" ]]; then
                modified_file="$1"
            else
                echo "Too many arguments"
                usage
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate inputs
if [[ -z "$original_file" || -z "$modified_file" ]]; then
    echo "Error: Both original and modified file paths are required"
    usage
    exit 1
fi

if [[ ! -f "$original_file" ]]; then
    echo "Error: Original file '$original_file' does not exist"
    exit 1
fi

if [[ ! -f "$modified_file" ]]; then
    echo "Error: Modified file '$modified_file' does not exist"
    exit 1
fi

# Show statistics if requested
if [[ "$show_stats" == true ]]; then
    show_statistics "$original_file" "$modified_file"
fi

# Build diff command
diff_cmd="diff"

# Add options based on flags
if [[ "$ignore_case" == true ]]; then
    diff_cmd="$diff_cmd -i"
fi

if [[ "$ignore_whitespace" == true ]]; then
    diff_cmd="$diff_cmd -w"
fi

if [[ "$diff_format" == "unified" ]]; then
    diff_cmd="$diff_cmd -u -C $context_lines"
elif [[ "$diff_format" == "side-by-side" ]]; then
    diff_cmd="$diff_cmd -y --width=160"
fi

# Execute diff and handle output
echo "Comparing files..."
echo "Original: $original_file"
echo "Modified: $modified_file"
echo ""

case "$output_format" in
    diff)
        if [[ -n "$output_file" ]]; then
            $diff_cmd "$original_file" "$modified_file" > "$output_file" 2>/dev/null || true
            echo "Diff saved to: $output_file"
        else
            $diff_cmd "$original_file" "$modified_file" || true
        fi
        ;;
    html)
        if [[ -z "$output_file" ]]; then
            output_file="comparison_$(date +%Y%m%d_%H%M%S).html"
        fi
        generate_html_diff "$original_file" "$modified_file" "$output_file"
        echo "HTML comparison saved to: $output_file"
        ;;
    json)
        if [[ -z "$output_file" ]]; then
            output_file="comparison_$(date +%Y%m%d_%H%M%S).json"
        fi
        
        # Check if jq is available for JSON generation
        if ! command -v jq &> /dev/null; then
            echo "Error: 'jq' command not found. Please install jq for JSON output."
            exit 1
        fi
        
        generate_json_diff "$original_file" "$modified_file" "$output_file"
        echo "JSON comparison saved to: $output_file"
        ;;
esac

# Check if files are identical
if diff -q "$original_file" "$modified_file" > /dev/null 2>&1; then
    echo ""
    echo "Files are identical - no changes detected."
else
    echo ""
    echo "Changes detected between the files."
fi