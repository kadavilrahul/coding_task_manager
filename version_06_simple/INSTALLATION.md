
### 1. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
 -  Edit .env file and add your Gemini API key
 -  Replace 'your_gemini_api_key_here' with your actual API key

### 4. Install gemini library for agno
```
pip install google-genai
```

### 5. Run the PRD Generator
```bash
python prd_generator.py
```
