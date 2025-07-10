#!/bin/bash

# Install cloc if it's not already installed
if ! command -v cloc &> /dev/null
then
    echo "Installing cloc..."
    sudo apt-get update
    sudo apt-get install cloc -y
else
    echo "cloc is already installed."
fi

# Run cloc on the current directory
echo "Running cloc on the current directory..."
cloc . --out=cloc_report.txt