#!/bin/bash

set -e  # Exit on any error

# Function to cleanup temporary files
cleanup() {
    rm -f /tmp/gemini_payload_*.json /tmp/escaped_prompt.json
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Function to call Gemini API safely
call_gemini_api() {
    local prompt="$1"
    
    # Create a temporary file for the JSON payload
    local temp_json=$(mktemp /tmp/gemini_payload_XXXXXX.json)
    
    # Create JSON payload using a temporary file to avoid argument length limits
    if ! echo "$prompt" | jq -R -s . > /tmp/escaped_prompt.json; then
        echo "Error: Failed to escape prompt for JSON"
        rm -f "$temp_json"
        return 1
    fi
    
    cat > "$temp_json" << EOF
{
    "contents": [{
        "parts": [{
            "text": $(cat /tmp/escaped_prompt.json)
        }]
    }]
}
EOF
    
    # Clean up the escaped prompt file
    rm -f /tmp/escaped_prompt.json
    
    # Validate the JSON before sending
    if ! jq . "$temp_json" > /dev/null; then
        echo "Error: Generated invalid JSON payload"
        rm -f "$temp_json"
        return 1
    fi
    
    # Make API call using the temporary file
    local response
    response=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -H "User-Agent: AgnoCodeTools/1.0" \
        -d @"$temp_json" \
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=$GEMINI_API_KEY")
    
    # Clean up temporary file
    rm -f "$temp_json"
    
    echo "$response"
}

# Check if an argument is provided
if [ -z "$1" ]; then
    directory="."
else
    directory="$1"
fi

# Check if project_info.txt exists
if [[ ! -f "$directory/project_info.txt" ]]; then
    echo "Error: project_info.txt not found in $directory. Please run project_info.sh in that directory first."
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

echo "Reading project information..."
project_info=$(cat "$directory/project_info.txt")

# Check the size of the project info
project_info_size=${#project_info}
if [ $project_info_size -gt 100000 ]; then
    echo "Warning: Project information is quite large ($project_info_size characters)."
    echo "This may take longer to process and could hit API limits."
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Operation cancelled."
        exit 0
    fi
fi

# Create comprehensive prompt
prompt="Please analyze the following project information and generate a Product Requirements Document (PRD) with the following sections:

1. Project Overview
2. Current Architecture Analysis
3. Identified Issues and Areas for Improvement
4. Recommended Features and Enhancements
5. Technical Implementation Suggestions
6. Security Considerations
7. Performance Optimization Opportunities

Project Information:
$project_info"

echo "Calling Gemini API..."

# Call Gemini API with error handling
if response=$(call_gemini_api "$prompt"); then
    # Check if response contains an error
    if echo "$response" | jq -e '.error' > /dev/null 2>&1; then
        echo "API Error:"
        echo "$response" | jq -r '.error.message // .error'
        exit 1
    fi
    
    # Save raw response
    echo "$response" > gemini_response_raw.json
    
    # Extract and format the text response
    if text_response=$(echo "$response" | jq -r '.candidates[0].content.parts[0].text // empty' 2>/dev/null); then
        if [[ -n "$text_response" ]]; then
            {
                echo "=== GEMINI GENERATED PRD ==="
                echo "Generated on: $(date)"
                echo ""
                echo "$text_response"
            } > gemini_prd.txt
            
            echo "PRD generated successfully!"
            echo "- Raw API response saved to: gemini_response_raw.json"
            echo "- Formatted PRD saved to: gemini_prd.txt"
        else
            echo "Error: Empty response from Gemini API"
            echo "Raw response saved to gemini_response_raw.json for debugging"
            exit 1
        fi
    else
        echo "Error: Could not parse Gemini API response"
        echo "Raw response saved to gemini_response_raw.json for debugging"
        exit 1
    fi
else
    echo "Error: Failed to call Gemini API"
    exit 1
fi