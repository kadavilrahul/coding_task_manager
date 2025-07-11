#!/bin/bash

# MCP Puppeteer Server Setup Script

echo "Setting up MCP Puppeteer Server..."

# Create screenshots directory
mkdir -p screenshots

# Pull the official MCP Puppeteer image (alternative to building)
echo "Pulling official MCP Puppeteer image..."
docker pull mcp/puppeteer:latest

# Build custom image (optional)
echo "Building custom MCP Puppeteer image..."
docker build -t mcp-puppeteer-custom .

# Run with docker-compose
echo "Starting MCP Puppeteer server with docker-compose..."
docker-compose up -d

echo "MCP Puppeteer server is now running!"
echo "You can use the official image with: docker run -i --rm --init -e DOCKER_CONTAINER=true mcp/puppeteer"
echo "Or use the custom built image with docker-compose"

# Display running containers
docker ps | grep puppeteer