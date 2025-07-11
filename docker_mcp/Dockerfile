# MCP Puppeteer Server Dockerfile
FROM node:18-alpine

# Install Puppeteer and Chrome dependencies
RUN apk add --no-cache \
    chromium \
    nss \
    freetype \
    freetype-dev \
    harfbuzz \
    ca-certificates \
    ttf-freefont

# Set Puppeteer to use installed Chromium
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Create app directory
WORKDIR /app

# Install MCP Puppeteer server
RUN npm install -g @modelcontextprotocol/server-puppeteer

# Set environment variables
ENV DOCKER_CONTAINER=true

# Expose port (if needed)
EXPOSE 3000

# Run the MCP server
CMD ["npx", "@modelcontextprotocol/server-puppeteer"]