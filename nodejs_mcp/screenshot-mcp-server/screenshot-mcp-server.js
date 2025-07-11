#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

class ScreenshotMCPServer {
    constructor() {
        this.tools = [{
            name: "screenshot",
            description: "Take a screenshot of a webpage from a URL",
            inputSchema: {
                type: "object",
                properties: {
                    url: {
                        type: "string",
                        description: "The URL of the webpage to screenshot"
                    },
                    width: {
                        type: "integer",
                        description: "Viewport width in pixels (default: 1920)",
                        default: 1920
                    },
                    height: {
                        type: "integer",
                        description: "Viewport height in pixels (default: 1080)",
                        default: 1080
                    },
                    output_path: {
                        type: "string",
                        description: "Path to save the screenshot (optional)"
                    },
                    browser: {
                        type: "string",
                        description: "Browser to use: 'chrome', 'chromium', or 'auto' (default: auto)",
                        enum: ["chrome", "chromium", "auto"],
                        default: "auto"
                    }
                },
                required: ["url"]
            }
        }];
    }

    takeScreenshot(url, width = 1920, height = 1080, outputPath = null, browserChoice = 'auto') {
        try {
            // Validate and fix URL
            if (!url.startsWith('http://') && !url.startsWith('https://')) {
                url = `https://${url}`;
            }
            
            // Validate URL format
            new URL(url);
            
            // Generate output path if not provided
            if (!outputPath) {
                const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
                const domain = new URL(url).hostname.replace(/\./g, '_');
                outputPath = `screenshot_${domain}_${timestamp}.png`;
            }

            // Ensure output directory exists
            const outputDir = path.dirname(outputPath);
            if (outputDir !== '.' && !fs.existsSync(outputDir)) {
                fs.mkdirSync(outputDir, { recursive: true });
            }

            // Determine browser to use
            let browser;
            if (browserChoice === 'chrome') {
                try {
                    execSync('which google-chrome', { stdio: 'pipe' });
                    browser = 'google-chrome';
                } catch (e) {
                    throw new Error('Google Chrome not found. Please install Chrome or use "chromium" option.');
                }
            } else if (browserChoice === 'chromium') {
                try {
                    execSync('which chromium-browser', { stdio: 'pipe' });
                    browser = 'chromium-browser';
                } catch (e) {
                    throw new Error('Chromium browser not found. Please install Chromium or use "chrome" option.');
                }
            } else {
                // Auto-detect (prefer Chrome over Chromium)
                try {
                    execSync('which google-chrome', { stdio: 'pipe' });
                    browser = 'google-chrome';
                } catch (e) {
                    try {
                        execSync('which chromium-browser', { stdio: 'pipe' });
                        browser = 'chromium-browser';
                    } catch (e2) {
                        throw new Error('Neither Google Chrome nor Chromium browser found. Please install one of them.');
                    }
                }
            }

            // Take screenshot using headless browser
            const command = `${browser} --headless --disable-gpu --disable-software-rasterizer --no-sandbox --screenshot="${outputPath}" --window-size=${width},${height} --virtual-time-budget=10000 "${url}"`;
            
            execSync(command, { 
                stdio: 'pipe',
                timeout: 30000 // 30 second timeout
            });

            // Check if file was created and get its size
            if (!fs.existsSync(outputPath)) {
                throw new Error('Screenshot file was not created');
            }

            const stats = fs.statSync(outputPath);
            const absolutePath = path.resolve(outputPath);

            return {
                success: true,
                screenshot_path: absolutePath,
                url: url,
                dimensions: `${width}x${height}`,
                file_size_bytes: stats.size,
                browser_used: browser,
                message: `Screenshot saved to ${outputPath} using ${browser}`
            };

        } catch (error) {
            return {
                success: false,
                error: error.message,
                url: url
            };
        }
    }

    handleRequest(request) {
        const { method, params } = request;

        switch (method) {
            case 'initialize':
                return {
                    protocolVersion: "2024-11-05",
                    capabilities: {
                        tools: {}
                    },
                    serverInfo: {
                        name: "screenshot-mcp-server",
                        version: "1.0.0"
                    }
                };
            
            case 'initialized':
                return {};
            
            case 'tools/list':
                return { tools: this.tools };
            
            case 'tools/call':
                const { name, arguments: args } = params;
                
                if (name === 'screenshot') {
                    const result = this.takeScreenshot(
                        args.url,
                        args.width,
                        args.height,
                        args.output_path,
                        args.browser
                    );
                    
                    return {
                        content: [{
                            type: "text",
                            text: JSON.stringify(result, null, 2)
                        }]
                    };
                }
                
                return { error: `Unknown tool: ${name}` };
            
            default:
                return { error: `Unknown method: ${method}` };
        }
    }

    run() {
        const readline = require('readline');
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout,
            terminal: false
        });

        rl.on('line', (line) => {
            try {
                const request = JSON.parse(line);
                const result = this.handleRequest(request);
                
                // Don't send response for notifications (requests without id)
                if (request.id === undefined) {
                    return;
                }
                
                const response = {
                    jsonrpc: "2.0",
                    id: request.id
                };
                
                if (result.error) {
                    response.error = result.error;
                } else {
                    response.result = result;
                }
                
                console.log(JSON.stringify(response));
            } catch (error) {
                const errorResponse = {
                    jsonrpc: "2.0",
                    id: request && request.id !== undefined ? request.id : null,
                    error: { code: -32603, message: error.message }
                };
                console.log(JSON.stringify(errorResponse));
            }
        });

        rl.on('close', () => {
            process.exit(0);
        });
    }
}

if (require.main === module) {
    const server = new ScreenshotMCPServer();
    server.run();
}