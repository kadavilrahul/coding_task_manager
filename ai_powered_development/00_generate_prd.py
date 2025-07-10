from agno.agent import Agent
from agno.models.google.gemini import Gemini
from agno.models.anthropic.claude import Claude # Import Claude
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Get API key from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    # Check for Claude API key if Gemini is not set
    CLAUDE_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    if not CLAUDE_API_KEY:
        raise ValueError("Missing GEMINI_API_KEY or ANTHROPIC_API_KEY environment variable")
    # If Claude key exists, we'll handle model initialization based on choice
    GEMINI_API_KEY = None # Ensure Gemini key is None if not found

class PRDGenerator:
    def __init__(self, llm_choice):
        """Initialize the PRD Generator with the chosen LLM model"""
        self.model = None
        if llm_choice == '1':
            if not GEMINI_API_KEY:
                 raise ValueError("GEMINI_API_KEY is required for Gemini models")
            self.model = Gemini(id="gemini-2.0-flash-exp", api_key=GEMINI_API_KEY)
        elif llm_choice == '2':
            if not GEMINI_API_KEY:
                 raise ValueError("GEMINI_API_KEY is required for Gemini models")
            self.model = Gemini(id="gemini-2.5-flash-preview-05-20", api_key=GEMINI_API_KEY)
        elif llm_choice == '3':
            if not GEMINI_API_KEY:
                 raise ValueError("GEMINI_API_KEY is required for Gemini models")
            self.model = Gemini(id="gemini-2.5-pro-preview-06-05", api_key=GEMINI_API_KEY)
        elif llm_choice == '4':
            CLAUDE_API_KEY = os.getenv('ANTHROPIC_API_KEY')
            if not CLAUDE_API_KEY:
                 raise ValueError("ANTHROPIC_API_KEY is required for Claude models")
            self.model = Claude(id="claude-sonnet-4-20250514", api_key=CLAUDE_API_KEY)
        else:
            raise ValueError("Invalid LLM choice")

        if not self.model:
             raise ValueError("Failed to initialize LLM model")

        self.prd_agent = Agent(
            name="PRD Generator",
            role="Product Requirements Document Generator",
            model=self.model,
            instructions="""
            You are an expert Product Manager and Technical Architect who creates comprehensive Product Requirements Documents (PRDs).
            
            Generate detailed PRDs with these sections:
            1. Executive Summary
            2. Problem Statement & Market Opportunity
            3. Goals and Success Metrics
            4. Functional Requirements
            5. Non-Functional Requirements
            6. Technical Architecture Overview
            7. Risk Assessment & Mitigation
            8. Dependencies & Assumptions
            9. Development Specifications (for coding projects)
            10. File Structure 

            For coding projects, include specific technical details like:
            - Programming languages and frameworks
            - File organization and naming conventions
            - Function specifications and APIs
            - Database schemas if applicable
            - Integration requirements
            - Performance benchmarks
            - Dont give code examples
            
            Format with clear headings, bullet points, and actionable details.
            Include realistic timelines, specific metrics, and technical considerations.
            """
        )
        self.existing_files = []
        self.project_analysis = {}

    def scan_existing_files(self, directory="."):
        """Scan all files in the current directory and subdirectories"""
        all_files = []
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if not any(
                d in pattern for pattern in ['__pycache__', 'node_modules', 'venv', 'env', '.venv',
                                            'dist', 'build', 'target', '.git', '.pytest_cache', '.mypy_cache']
            )]
            for file in files:
                file_path = os.path.join(root, file)
                if not any(file.endswith(ext) for ext in ['.pyc', '.pyo', '.class', '.log', '.tmp']) and \
                   not file.startswith('.') and file not in ['.DS_Store', 'Thumbs.db']:
                    all_files.append(file_path)
        self.existing_files = sorted(all_files)
        print(f"✅ Scanned {len(self.existing_files)} files in the project")

    def analyze_project_structure(self):
        """Analyze the existing project structure and technologies"""
        analysis = {
            'languages': set(),
            'frameworks': set(),
            'total_files': len(self.existing_files),
        }
        
        for file_path in self.existing_files:
            file_name = os.path.basename(file_path)
            file_ext = os.path.splitext(file_name)[1].lower()
            
            language_map = {
                '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', '.java': 'Java',
                '.c': 'C', '.cpp': 'C++', '.cs': 'C#', '.go': 'Go', '.rb': 'Ruby',
                '.php': 'PHP', '.rs': 'Rust', '.kt': 'Kotlin', '.swift': 'Swift',
                '.sh': 'Shell Script', '.ps1': 'PowerShell'
            }
            if file_ext in language_map:
                analysis['languages'].add(language_map[file_ext])
            
            # Basic framework detection (can be expanded)
            if file_ext in ['.py', '.js', '.ts']:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(500) # Read first 500 chars for quick check
                        if 'django' in content.lower(): analysis['frameworks'].add('Django')
                        if 'flask' in content.lower(): analysis['frameworks'].add('Flask')
                        if 'react' in content.lower(): analysis['frameworks'].add('React')
                        if 'vue' in content.lower(): analysis['frameworks'].add('Vue.js')
                except:
                    pass
        
        self.project_analysis = analysis
        print(f"🔬 Analyzed project: Languages={', '.join(analysis['languages'])}, Frameworks={', '.join(analysis['frameworks'])}")
        return analysis

    def generate_prd(self, product_idea: str, is_new_project: bool, project_analysis: dict = None) -> str:
        """Generate a concise PRD based on a product idea, project type, and optional analysis"""
        project_type_context = "This is a new project." if is_new_project else "This is an existing project that needs modifications or enhancements."
        
        analysis_context = ""
        if project_analysis and not is_new_project:
            analysis_context = f"""
**EXISTING PROJECT ANALYSIS:**
- Total Files: {project_analysis.get('total_files', 0)}
- Detected Languages: {', '.join(project_analysis.get('languages', [])) if project_analysis.get('languages') else 'None'}
- Detected Frameworks: {', '.join(project_analysis.get('frameworks', [])) if project_analysis.get('frameworks') else 'None'}
"""
        
        prompt = f"""
**PROJECT CONTEXT:**
{project_type_context}
{analysis_context}
**Product Idea:** {product_idea}

Create a comprehensive PRD based on the above context.
"""
        try:
            response = self.prd_agent.run(prompt)
            return response.content
        except Exception as e:
            return f"Error generating PRD: {str(e)}"

    def save_prd(self, prd_content: str, filename: str = None) -> str:
        """Save the generated PRD to a file"""
        if not filename:
            timestamp = datetime.now().strftime("%d-%m-%Y_%H%M%S")
            filename = f"PRD_{timestamp}.md"
        
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(prd_content)
            return f"PRD saved successfully to {filename}"
        except Exception as e:
            return f"Error saving PRD: {str(e)}"

def main():
    """Main function for the simplified PRD generator"""
    print("="*60)
    print("🚀 PRD GENERATOR")
    print("="*60)

    print("\nChoose project type:")
    print("1. New Project")
    print("2. Existing Project to be modified")
    project_status_choice = input("Enter your choice (1/2): ").strip()
    is_new_project = (project_status_choice == '1')

    print("\nChoose LLM model:")
    print("1. Gemini (gemini-2.0-flash-exp)")
    print("2. Gemini (gemini-2.5-flash-preview-05-20)")
    print("3. Gemini (gemini-2.5-pro-preview-06-05)")
    print("4. Claude (claude-sonnet-4-20250514)")
    llm_choice = input("Enter your choice (1/2/3/4): ").strip()

    # Initialize generator with chosen LLM
    generator = PRDGenerator(llm_choice=llm_choice)

    project_analysis = None
    if not is_new_project:
        print("\n🔍 Scanning existing project files...")
        generator.scan_existing_files()
        project_analysis = generator.analyze_project_structure()
        
    product_idea = input("📝 Enter your product idea (e.g., 'I want to simplify the project and use Gulp to generate html pages from csv files'): ").strip()
    
    if not product_idea:
        print("Product idea cannot be empty. Exiting.")
        return

    print("\n🤖 Generating PRD...")
    prd = generator.generate_prd(product_idea, is_new_project, project_analysis)
    
    
    # Auto-save PRD
    project_name_safe = product_idea.split(' ')[0].replace('/', '_') if product_idea else 'product'
    timestamp = datetime.now().strftime('%d-%m-%Y_%H%M%S')
    filename = f"PRD_{project_name_safe}_{timestamp}.md"
    result = generator.save_prd(prd, filename)
    print(f"\n✅ {result}")

if __name__ == "__main__":
    main()
