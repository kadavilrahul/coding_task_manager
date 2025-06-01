#!/bin/bash

set -e  # Exit on any error

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS] <file_path>"
    echo "Extract function definitions from code files"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -l, --lang     Specify language (auto-detect if not provided)"
    echo "  -o, --output   Output directory (default: extracted_functions)"
    echo "  -f, --format   Output format: separate|single (default: separate)"
    echo ""
    echo "Supported languages: python, javascript, bash, java, c, cpp"
    echo ""
    echo "Examples:"
    echo "  $0 main.py"
    echo "  $0 -l python -o functions src/utils.py"
    echo "  $0 -f single script.js"
}

# Function to detect language from file extension
detect_language() {
    local file="$1"
    local ext="${file##*.}"
    
    case "$ext" in
        py) echo "python" ;;
        js) echo "javascript" ;;
        sh) echo "bash" ;;
        java) echo "java" ;;
        c) echo "c" ;;
        cpp|cc|cxx) echo "cpp" ;;
        *) echo "unknown" ;;
    esac
}

# Function to extract Python functions
extract_python_functions() {
    local file="$1"
    local output_dir="$2"
    local format="$3"
    
    if [[ "$format" == "single" ]]; then
        {
            echo "# Extracted functions from $file"
            echo "# Generated on $(date)"
            echo ""
        } > "$output_dir/all_functions.py"
    fi
    
    # Use awk to extract function definitions
    awk '
    /^def / {
        func_name = $2
        gsub(/\(.*/, "", func_name)
        in_function = 1
        indent_level = 0
        if (format == "single") {
            print $0 >> output_dir "/all_functions.py"
        } else {
            print $0 > output_dir "/" func_name ".py"
        }
        next
    }
    in_function && /^[[:space:]]*$/ {
        if (format == "single") {
            print $0 >> output_dir "/all_functions.py"
        } else {
            print $0 >> output_dir "/" func_name ".py"
        }
        next
    }
    in_function && /^[[:space:]]/ {
        if (format == "single") {
            print $0 >> output_dir "/all_functions.py"
        } else {
            print $0 >> output_dir "/" func_name ".py"
        }
        next
    }
    in_function && /^[^[:space:]]/ {
        in_function = 0
        if (format == "single") {
            print "" >> output_dir "/all_functions.py"
        }
    }
    ' format="$format" output_dir="$output_dir" "$file"
}

# Function to extract JavaScript functions
extract_javascript_functions() {
    local file="$1"
    local output_dir="$2"
    local format="$3"
    
    if [[ "$format" == "single" ]]; then
        {
            echo "// Extracted functions from $file"
            echo "// Generated on $(date)"
            echo ""
        } > "$output_dir/all_functions.js"
    fi
    
    # Extract function declarations and expressions
    grep -n -A 20 -E "(^function |const .* = function|const .* = \(|function .* \()" "$file" | \
    while IFS=: read -r line_num content; do
        if [[ "$content" =~ ^[0-9]+--.* ]]; then
            continue
        fi
        
        if [[ "$content" =~ function.*\( ]]; then
            func_name=$(echo "$content" | sed -E 's/.*function ([a-zA-Z_][a-zA-Z0-9_]*).*/\1/')
            if [[ "$format" == "single" ]]; then
                echo "$content" >> "$output_dir/all_functions.js"
            else
                echo "$content" > "$output_dir/${func_name}.js"
            fi
        fi
    done
}

# Function to extract Bash functions
extract_bash_functions() {
    local file="$1"
    local output_dir="$2"
    local format="$3"
    
    if [[ "$format" == "single" ]]; then
        {
            echo "#!/bin/bash"
            echo "# Extracted functions from $file"
            echo "# Generated on $(date)"
            echo ""
        } > "$output_dir/all_functions.sh"
    fi
    
    # Extract bash function definitions
    awk '
    /^[a-zA-Z_][a-zA-Z0-9_]*\(\)/ {
        func_name = $1
        gsub(/\(\).*/, "", func_name)
        in_function = 1
        brace_count = 0
        if (format == "single") {
            print $0 >> output_dir "/all_functions.sh"
        } else {
            print "#!/bin/bash" > output_dir "/" func_name ".sh"
            print $0 >> output_dir "/" func_name ".sh"
        }
        next
    }
    in_function {
        if (format == "single") {
            print $0 >> output_dir "/all_functions.sh"
        } else {
            print $0 >> output_dir "/" func_name ".sh"
        }
        
        # Count braces to determine function end
        gsub(/\{/, "", $0); open_braces = gsub(/\{/, "", $0)
        gsub(/\}/, "", $0); close_braces = gsub(/\}/, "", $0)
        brace_count += open_braces - close_braces
        
        if (brace_count <= 0 && /\}/) {
            in_function = 0
            if (format == "single") {
                print "" >> output_dir "/all_functions.sh"
            }
        }
    }
    ' format="$format" output_dir="$output_dir" "$file"
}

# Initialize variables
file_path=""
language=""
output_dir="extracted_functions"
format="separate"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -l|--lang)
            language="$2"
            shift 2
            ;;
        -o|--output)
            output_dir="$2"
            shift 2
            ;;
        -f|--format)
            format="$2"
            if [[ "$format" != "separate" && "$format" != "single" ]]; then
                echo "Error: Format must be 'separate' or 'single'"
                exit 1
            fi
            shift 2
            ;;
        -*)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            file_path="$1"
            shift
            ;;
    esac
done

# Validate input
if [[ -z "$file_path" ]]; then
    echo "Error: No file path provided"
    usage
    exit 1
fi

if [[ ! -f "$file_path" ]]; then
    echo "Error: File '$file_path' does not exist"
    exit 1
fi

# Auto-detect language if not specified
if [[ -z "$language" ]]; then
    language=$(detect_language "$file_path")
    if [[ "$language" == "unknown" ]]; then
        echo "Error: Could not detect language for '$file_path'"
        echo "Please specify language with -l option"
        exit 1
    fi
    echo "Detected language: $language"
fi

# Create output directory
mkdir -p "$output_dir"

echo "Extracting functions from '$file_path'..."
echo "Language: $language"
echo "Output directory: $output_dir"
echo "Format: $format"

# Extract functions based on language
case "$language" in
    python)
        extract_python_functions "$file_path" "$output_dir" "$format"
        ;;
    javascript)
        extract_javascript_functions "$file_path" "$output_dir" "$format"
        ;;
    bash)
        extract_bash_functions "$file_path" "$output_dir" "$format"
        ;;
    *)
        echo "Error: Language '$language' is not yet supported"
        echo "Supported languages: python, javascript, bash"
        exit 1
        ;;
esac

echo "Function extraction completed!"
echo "Check the '$output_dir' directory for extracted functions."