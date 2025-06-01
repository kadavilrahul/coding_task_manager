#!/bin/bash

set -e  # Exit on any error

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS] <file_path> [function_name]"
    echo "Modify code using the Gemini API"
    echo ""
    echo "Options:"
    echo "  -h, --help        Show this help message"
    echo "  -p, --prompt      Custom modification prompt"
    echo "  -b, --backup      Create backup before modification"
    echo "  -d, --dry-run     Show proposed changes without applying"
    echo "  -o, --output      Output file (default: overwrite original)"
    echo ""
    echo "Examples:"
    echo "  $0 main.py calculate_sum"
    echo "  $0 -p 'Add error handling' utils.py"
    echo "  $0 -b -d script.py process_data"
}

# Function to escape JSON strings
escape_json() {
    echo "$1" | sed 's/\\/\\\\/g; s/"/\\"/g; s/$/\\n/g' | tr -d '\n'
}

# Function to call Gemini API safely
call_gemini_api() {
    local prompt="$1"
    
    # Prepare JSON payload using jq
    local json_payload
    json_payload=$(jq -n --arg text "$prompt" '{
        contents: [{
            parts: [{
                text: $text
            }]
        }],
        generationConfig: {
            temperature: 0.1,
            maxOutputTokens: 2048
        }
    }')
    
    # Make API call
    curl -s -X POST \
        -H "Content-Type: application/json" \
        -H "User-Agent: AgnoCodeTools/1.0" \
        -d "$json_payload" \
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=$GEMINI_API_KEY"
}

# Function to extract function from file
extract_function() {
    local file="$1"
    local func_name="$2"
    local lang="$3"
    
    case "$lang" in
        python)
            # Extract Python function with proper indentation
            awk -v func="$func_name" '
            /^def / && $2 ~ "^" func "\\(" {
                in_function = 1
                print $0
                next
            }
            in_function && /^[[:space:]]*$/ {
                print $0
                next
            }
            in_function && /^[[:space:]]/ {
                print $0
                next
            }
            in_function && /^[^[:space:]]/ {
                exit
            }
            ' "$file"
            ;;
        javascript)
            # Extract JavaScript function
            grep -A 50 -E "(^function $func_name|const $func_name.*=)" "$file" | \
            awk '/^function|^const.*=/ {in_func=1} in_func {print} /^}$/ && in_func {exit}'
            ;;
        bash)
            # Extract Bash function
            awk -v func="$func_name" '
            $0 ~ "^" func "\\(\\)" {
                in_function = 1
                brace_count = 0
                print $0
                next
            }
            in_function {
                print $0
                gsub(/\{/, ""); open_braces = gsub(/\{/, "")
                gsub(/\}/, ""); close_braces = gsub(/\}/, "")
                brace_count += open_braces - close_braces
                if (brace_count <= 0 && /\}/) {
                    exit
                }
            }
            ' "$file"
            ;;
        *)
            echo "Language detection failed. Extracting first 20 lines around pattern..."
            grep -A 20 -B 5 "$func_name" "$file" || echo "Pattern not found"
            ;;
    esac
}

# Function to detect language
detect_language() {
    local file="$1"
    local ext="${file##*.}"
    
    case "$ext" in
        py) echo "python" ;;
        js) echo "javascript" ;;
        sh) echo "bash" ;;
        *) echo "unknown" ;;
    esac
}

# Function to create backup
create_backup() {
    local file="$1"
    local backup_file="${file}.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$file" "$backup_file"
    echo "Backup created: $backup_file"
}

# Function to apply modifications
apply_modifications() {
    local original_file="$1"
    local modified_content="$2"
    local output_file="$3"
    local dry_run="$4"
    
    if [[ "$dry_run" == true ]]; then
        echo "=== PROPOSED CHANGES (DRY RUN) ==="
        echo "$modified_content"
        echo "=== END OF PROPOSED CHANGES ==="
        return 0
    fi
    
    echo "$modified_content" > "$output_file"
    echo "Modifications applied to: $output_file"
}

# Initialize variables
file_path=""
function_name=""
custom_prompt=""
create_backup_flag=false
dry_run=false
output_file=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -p|--prompt)
            custom_prompt="$2"
            shift 2
            ;;
        -b|--backup)
            create_backup_flag=true
            shift
            ;;
        -d|--dry-run)
            dry_run=true
            shift
            ;;
        -o|--output)
            output_file="$2"
            shift 2
            ;;
        -*)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            if [[ -z "$file_path" ]]; then
                file_path="$1"
            elif [[ -z "$function_name" ]]; then
                function_name="$1"
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
if [[ -z "$file_path" ]]; then
    echo "Error: No file path provided"
    usage
    exit 1
fi

if [[ ! -f "$file_path" ]]; then
    echo "Error: File '$file_path' does not exist"
    exit 1
fi

# Check if Gemini API key is set
if [[ -z "$GEMINI_API_KEY" ]]; then
    echo "Error: GEMINI_API_KEY environment variable is not set."
    echo "Please set it with: export GEMINI_API_KEY='your_api_key_here'"
    exit 1
fi

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "Error: 'jq' command not found. Please install jq to parse JSON responses."
    exit 1
fi

# Set output file if not specified
if [[ -z "$output_file" ]]; then
    output_file="$file_path"
fi

# Create backup if requested
if [[ "$create_backup_flag" == true ]]; then
    create_backup "$file_path"
fi

# Detect language
language=$(detect_language "$file_path")
echo "Detected language: $language"

# Extract code to modify
if [[ -n "$function_name" ]]; then
    echo "Extracting function '$function_name' from '$file_path'..."
    code_to_modify=$(extract_function "$file_path" "$function_name" "$language")
    
    if [[ -z "$code_to_modify" ]]; then
        echo "Error: Function '$function_name' not found in '$file_path'"
        exit 1
    fi
    
    context="function '$function_name'"
else
    echo "Reading entire file '$file_path'..."
    code_to_modify=$(cat "$file_path")
    context="file '$file_path'"
fi

# Create modification prompt
if [[ -n "$custom_prompt" ]]; then
    modification_request="$custom_prompt"
else
    echo "What modifications would you like to make to the $context?"
    echo "Examples:"
    echo "- Add error handling and input validation"
    echo "- Optimize for better performance"
    echo "- Add comprehensive documentation"
    echo "- Refactor to improve readability"
    echo ""
    read -p "Enter your modification request: " modification_request
    
    if [[ -z "$modification_request" ]]; then
        echo "No modification request provided. Exiting."
        exit 1
    fi
fi

# Create comprehensive prompt for Gemini
prompt="Please modify the following $language code according to this request: $modification_request

Requirements:
1. Maintain the original functionality
2. Follow $language best practices and conventions
3. Add appropriate comments where needed
4. Ensure the code is production-ready
5. Return ONLY the modified code without explanations

Original code:
\`\`\`$language
$code_to_modify
\`\`\`

Modified code:"

echo "Sending modification request to Gemini API..."

# Call Gemini API
if response=$(call_gemini_api "$prompt"); then
    # Check for API errors
    if echo "$response" | jq -e '.error' > /dev/null 2>&1; then
        echo "API Error:"
        echo "$response" | jq -r '.error.message // .error'
        exit 1
    fi
    
    # Extract the modified code
    if modified_code=$(echo "$response" | jq -r '.candidates[0].content.parts[0].text // empty' 2>/dev/null); then
        if [[ -n "$modified_code" ]]; then
            # Clean up the response (remove markdown code blocks if present)
            cleaned_code=$(echo "$modified_code" | sed -E 's/^```[a-zA-Z]*//; s/```$//; /^$/d')
            
            # Apply modifications
            if [[ -n "$function_name" ]]; then
                # Replace specific function in the original file
                # This is a simplified approach - in production, you'd want more sophisticated replacement
                echo "Warning: Function replacement is simplified. Review changes carefully."
                apply_modifications "$file_path" "$cleaned_code" "$output_file" "$dry_run"
            else
                # Replace entire file
                apply_modifications "$file_path" "$cleaned_code" "$output_file" "$dry_run"
            fi
            
            if [[ "$dry_run" == false ]]; then
                echo "Code modification completed successfully!"
                echo "Modified $context in: $output_file"
            fi
        else
            echo "Error: Empty response from Gemini API"
            exit 1
        fi
    else
        echo "Error: Could not parse Gemini API response"
        echo "Raw response:"
        echo "$response"
        exit 1
    fi
else
    echo "Error: Failed to call Gemini API"
    exit 1
fi