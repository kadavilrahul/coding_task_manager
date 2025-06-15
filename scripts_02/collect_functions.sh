#!/bin/bash

# Ask the user to choose a method
echo "Choose a method to collect function names:"
echo "1. grep"
echo "2. ctags"
echo "3. ast (Python)"
read -p "Enter your choice (1-3): " choice

# Function to use grep
grep_functions() {
  grep -r "^def " . > ./functions.txt
  echo "Function names collected using grep and saved to functions.txt"
}

# Function to use ctags
ctags_functions() {
  # Install ctags if it's not already installed
  if ! command -v ctags &> /dev/null
  then
    echo "Installing ctags..."
    sudo apt-get update
    sudo apt-get install exuberant-ctags -y
  else
    echo "ctags is already installed."
  fi
  ctags -R .
  grep "^[a-zA-Z0-9_]*$" tags | awk '{print $5, $1}' > ./functions.txt
  echo "Function names collected using ctags and saved to functions.txt"
}

# Process the user's choice
case $choice in
  1)
    grep_functions
    ;;
  2)
    ctags_functions
    ;;
  3)
    python extract_functions.py
    echo "Function names collected using ast (Python) and saved to functions.txt"
    ;;
  *)
    echo "Invalid choice. Please enter a number between 1 and 3."
    exit 1
    ;;
esac

exit 0