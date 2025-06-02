# PRD Generator Installation Guide

## Prerequisites
- Python 3.8 or higher
- Gemini API key from Google AI Studio

## Installation Steps

### 1. Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd prd-generator

# Or download and extract the files to a folder
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
 -  Edit .env file and add your Gemini API key
 -  Replace 'your_gemini_api_key_here' with your actual API key

### 5. Install gemini library
```
pip install google-genai
```

**Get your Gemini API key:**
1. Go to [Google AI Studio]
2. Create a new API key
3. Copy the key and paste it in your `.env` file

### 5. Run the PRD Generator
```bash
python prd_generator.py
```

## Usage Examples

### Basic Usage
The script will run with a default example. Modify the `product_idea` in the `main()` function for your own product.

### Interactive Mode
Uncomment the interactive mode line in `main()` function:
```python
# Uncomment this line for interactive input:
generator.interactive_mode()
```

## Troubleshooting

### Common Issues

**1. ModuleNotFoundError: No module named 'google.genai':**
```bash
pip install google-genai google-generativeai
```

**2. Import Error for agno:**
```bash
pip install --upgrade agno
```

**3. Gemini API Error:**
- Verify your API key is correct
- Check if you have API quota remaining
- Ensure the API key has proper permissions

**4. Virtual Environment Issues:**
```bash
# Deactivate and recreate if needed
deactivate
rm -rf venv  # On Windows: rmdir /s venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## File Structure
```
prd-generator/
├── prd_generator.py    # Main application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (add your API key here)
├── INSTALLATION.md    # This file
└── generated_prds/    # Output folder (created automatically)
```

## Next Steps
- Modify the product idea in `prd_generator.py`
- Customize the PRD template in the agent instructions
- Add additional context fields as needed
- Save generated PRDs to review and iterate

## Support
If you encounter issues:
1. Check that all dependencies are installed correctly
2. Verify your Gemini API key is valid
3. Ensure you're using Python 3.8+
4. Check the agno library documentation for updates