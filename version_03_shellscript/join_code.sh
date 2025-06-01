#!/bin/bash

set -e  # Exit on any error

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS] <output_file> <input_files...>"
    echo "Join multiple code files into a single file"
    echo ""
    echo "Options:"
    echo "  -h, --help        Show this help message"
    echo "  -s, --separator   Custom separator between files (default: newlines)"
    echo "  -c, --comments    Add file name comments as separators"
    echo "  -n, --numbers     Add line numbers to output"
    echo "  -f, --format      Auto-format the output (requires language-specific tools)"
    echo "  -l, --lang        Specify language for formatting (auto-detect if not provided)"
    echo "  -d, --directory   Join all files from a directory"
    echo "  -p, --pattern     File pattern to match (e.g., '*.py', '*.js')"
    echo "  --exclude         Exclude files matching pattern"
    echo ""
    echo "Examples:"
    echo "  $0 combined.py file1.py file2.py file3.py"
    echo "  $0 -c -n all_scripts.js src/*.js"
    echo "  $0 -d -p '*.py' combined.py src/"
    echo "  $0 --exclude '*test*' combined.py *.py"
}

# Function to detect language from file extension
detect_language() {
    local file="$1"
    local ext="${file##*.}"
    
    case "$ext" in
        py) echo "python" ;;
        js) echo "javascript" ;;
        ts) echo "typescript" ;;
        java) echo "java" ;;
        c) echo "c" ;;
        cpp|cc|cxx) echo "cpp" ;;
        sh) echo "bash" ;;
        rb) echo "ruby" ;;
        php) echo "php" ;;
        go) echo "go" ;;
        rs) echo "rust" ;;
        *) echo "unknown" ;;
    esac
}

# Function to add file separator comment
add_file_comment() {
    local file="$1"
    local lang="$2"
    local output="$3"
    
    case "$lang" in
        python|bash|ruby)
            echo "# =============================================" >> "$output"
            echo "# File: $file" >> "$output"
            echo "# =============================================" >> "$output"
            ;;
        javascript|typescript|java|c|cpp|go|rust|php)
            echo "// =============================================" >> "$output"
            echo "// File: $file" >> "$output"
            echo "// =============================================" >> "$output"
            ;;
        *)
            echo "/* =============================================" >> "$output"
            echo " * File: $file" >> "$output"
            echo " * ============================================= */" >> "$output"
            ;;
    esac
}

# Function to format code based on language
format_code() {
    local file="$1"
    local lang="$2"
    
    case "$lang" in
        python)
            if command -v black &> /dev/null; then
                black --quiet "$file" 2>/dev/null || true
            elif command -v autopep8 &> /dev/null; then
                autopep8 --in-place "$file" 2>/dev/null || true
            fi
            ;;
        javascript|typescript)
            if command -v prettier &> /dev/null; then
                prettier --write "$file" 2>/dev/null || true
            fi
            ;;
        java)
            if command -v google-java-format &> /dev/null; then
                google-java-format --replace "$file" 2>/dev/null || true
            fi
            ;;
        go)
            if command -v gofmt &> /dev/null; then
                gofmt -w "$file" 2>/dev/null || true
            fi
            ;;
        rust)
            if command -v rustfmt &> /dev/null; then
                rustfmt "$file" 2>/dev/null || true
            fi
            ;;
    esac
}

# Function to collect files from directory
collect_files_from_directory() {
    local dir="$1"
    local pattern="$2"
    local exclude_pattern="$3"
    
    local find_cmd="find '$dir' -type f"
    
    if [[ -n "$pattern" ]]; then
        find_cmd="$find_cmd -name '$pattern'"
    fi
    
    local files
    files=$(eval "$find_cmd" | sort)
    
    if [[ -n "$exclude_pattern" ]]; then
        files=$(echo "$files" | grep -v "$exclude_pattern" || true)
    fi
    
    echo "$files"
}

# Initialize variables
output_file=""
input_files=()
custom_separator=""
add_comments=false
add_line_numbers=false
auto_format=false
language=""
from_directory=""
file_pattern=""
exclude_pattern=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -s|--separator)
            custom_separator="$2"
            shift 2
            ;;
        -c|--comments)
            add_comments=true
            shift
            ;;
        -n|--numbers)
            add_line_numbers=true
            shift
            ;;
        -f|--format)
            auto_format=true
            shift
            ;;
        -l|--lang)
            language="$2"
            shift 2
            ;;
        -d|--directory)
            from_directory="$2"
            shift 2
            ;;
        -p|--pattern)
            file_pattern="$2"
            shift 2
            ;;
        --exclude)
            exclude_pattern="$2"
            shift 2
            ;;
        -*)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            if [[ -z "$output_file" ]]; then
                output_file="$1"
            else
                input_files+=("$1")
            fi
            shift
            ;;
    esac
done

# Validate inputs
if [[ -z "$output_file" ]]; then
    echo "Error: Output file not specified"
    usage
    exit 1
fi

# Collect input files
if [[ -n "$from_directory" ]]; then
    if [[ ! -d "$from_directory" ]]; then
        echo "Error: Directory '$from_directory' does not exist"
        exit 1
    fi
    
    echo "Collecting files from directory: $from_directory"
    if [[ -n "$file_pattern" ]]; then
        echo "Pattern: $file_pattern"
    fi
    if [[ -n "$exclude_pattern" ]]; then
        echo "Excluding: $exclude_pattern"
    fi
    
    mapfile -t input_files < <(collect_files_from_directory "$from_directory" "$file_pattern" "$exclude_pattern")
else
    # Filter existing input files and apply exclude pattern
    filtered_files=()
    for file in "${input_files[@]}"; do
        if [[ -f "$file" ]]; then
            if [[ -z "$exclude_pattern" ]] || [[ ! "$file" =~ $exclude_pattern ]]; then
                filtered_files+=("$file")
            fi
        else
            echo "Warning: File '$file' does not exist, skipping..."
        fi
    done
    input_files=("${filtered_files[@]}")
fi

if [[ ${#input_files[@]} -eq 0 ]]; then
    echo "Error: No input files specified or found"
    exit 1
fi

# Auto-detect language if not specified
if [[ -z "$language" && ${#input_files[@]} -gt 0 ]]; then
    language=$(detect_language "${input_files[0]}")
    if [[ "$language" != "unknown" ]]; then
        echo "Detected language: $language"
    fi
fi

# Check if output file already exists
if [[ -f "$output_file" ]]; then
    read -p "Output file '$output_file' already exists. Overwrite? (y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "Operation cancelled."
        exit 0
    fi
fi

echo "Joining ${#input_files[@]} files into '$output_file'..."

# Create output file header
{
    echo "/*"
    echo " * Combined file: $output_file"
    echo " * Generated on: $(date)"
    echo " * Source files: ${#input_files[@]} files"
    echo " * Language: $language"
    echo " */"
    echo ""
} > "$output_file"

# Process each input file
file_count=0
for file in "${input_files[@]}"; do
    ((file_count++))
    echo "Processing file $file_count/${#input_files[@]}: $file"
    
    # Add file separator comment if requested
    if [[ "$add_comments" == true ]]; then
        add_file_comment "$file" "$language" "$output_file"
        echo "" >> "$output_file"
    fi
    
    # Add custom separator if specified
    if [[ -n "$custom_separator" ]]; then
        echo "$custom_separator" >> "$output_file"
    fi
    
    # Add file content
    if [[ "$add_line_numbers" == true ]]; then
        # Add line numbers with file prefix
        nl -ba "$file" | sed "s/^/[$file] /" >> "$output_file"
    else
        cat "$file" >> "$output_file"
    fi
    
    # Add spacing between files
    echo "" >> "$output_file"
    echo "" >> "$output_file"
done

echo "Successfully joined ${#input_files[@]} files into '$output_file'"

# Auto-format if requested
if [[ "$auto_format" == true ]]; then
    echo "Formatting output file..."
    format_code "$output_file" "$language"
    echo "Formatting completed."
fi

# Show file statistics
echo ""
echo "=== OUTPUT FILE STATISTICS ==="
echo "File: $output_file"
echo "Size: $(wc -c < "$output_file") bytes"
echo "Lines: $(wc -l < "$output_file") lines"
echo "Words: $(wc -w < "$output_file") words"

# Show input file summary
echo ""
echo "=== INPUT FILES SUMMARY ==="
for file in "${input_files[@]}"; do
    printf "%-40s %8s bytes %6s lines\n" \
        "$file" \
        "$(wc -c < "$file")" \
        "$(wc -l < "$file")"
done