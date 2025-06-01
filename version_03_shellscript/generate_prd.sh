#!/bin/bash

# Read project information
project_info=$(cat project_info.txt)

# Create prompt
prompt="Analyze the following project and suggest improvements:\n$project_info"

# Call Gemini API (replace with your actual API endpoint and key)
GEMINI_API_KEY=$(echo $GEMINI_API_KEY)
url="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=$GEMINI_API_KEY"
data='{"contents":[{"parts":[{"text":"'$prompt'"}]}]}'

response=$(curl -X POST \
  -H "Content-Type: application/json" \
  -d "$data" \
  "$url")

# Save Gemini response
echo "$response" > gemini_response.txt

echo "Gemini response saved to gemini_response.txt"