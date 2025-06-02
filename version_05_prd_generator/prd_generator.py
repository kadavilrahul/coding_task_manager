from agno.agent import Agent
from agno.models.google.gemini import Gemini
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Get API key from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY environment variable")

class PRDGenerator:
    def __init__(self):
        """Initialize the PRD Generator with Gemini model"""
        self.model = Gemini(
            id="gemini-2.0-flash-exp",
            api_key=GEMINI_API_KEY
        )
        
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
            4. Target Users & User Stories
            5. Functional Requirements
            6. Non-Functional Requirements
            7. Technical Architecture Overview
            8. Implementation Timeline
            9. Risk Assessment & Mitigation
            10. Dependencies & Assumptions
            11. Development Specifications (for coding projects)
            12. File Structure & Organization
            13. Testing Strategy
            
            For coding projects, include specific technical details like:
            - Programming languages and frameworks
            - File organization and naming conventions
            - Function specifications and APIs
            - Database schemas if applicable
            - Integration requirements
            - Performance benchmarks
            
            Format with clear headings, bullet points, and actionable details.
            Include realistic timelines, specific metrics, and technical considerations.
            """
        )
        
        self.project_info = None
        self.existing_files = []
        self.project_analysis = {}

    def read_project_info(self):
        """Read and parse project_info.txt if it exists"""
        try:
            if os.path.exists('project_info.txt'):
                with open('project_info.txt', 'r', encoding='utf-8') as f:
                    self.project_info = f.read()
                print("✅ Project info loaded from project_info.txt")
                return True
            else:
                print("ℹ️  No project_info.txt found")
                return False
        except Exception as e:
            print(f"⚠️  Error reading project_info.txt: {e}")
            return False

    def scan_existing_files(self, directory="."):
        """Scan all files in the current directory and subdirectories"""
        try:
            all_files = []
            for root, dirs, files in os.walk(directory):
                # Skip excluded directories
                dirs[:] = [d for d in dirs if not any(
                    d in pattern for pattern in ['__pycache__', 'node_modules', 'venv', 'env', '.venv', 
                                                'dist', 'build', 'target', '.git', '.pytest_cache', '.mypy_cache']
                )]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    # Skip excluded files
                    if not any(file.endswith(ext) for ext in ['.pyc', '.pyo', '.class', '.log', '.tmp']) and \
                       not file.startswith('.') and file not in ['.DS_Store', 'Thumbs.db']:
                        all_files.append(file_path)
            
            self.existing_files = sorted(all_files)
            print(f"✅ Scanned {len(self.existing_files)} files in the project")
            return True
        except Exception as e:
            print(f"⚠️  Error scanning files: {e}")
            return False

    def analyze_project_structure(self):
        """Analyze the existing project structure and technologies"""
        analysis = {
            'languages': set(),
            'frameworks': set(),
            'file_types': {},
            'total_files': len(self.existing_files),
            'config_files': [],
            'documentation': [],
            'scripts': [],
            'source_code': []
        }
        
        for file_path in self.existing_files:
            file_name = os.path.basename(file_path)
            file_ext = os.path.splitext(file_name)[1].lower()
            
            # Count file types
            analysis['file_types'][file_ext] = analysis['file_types'].get(file_ext, 0) + 1
            
            # Identify languages
            language_map = {
                '.py': 'Python',
                '.js': 'JavaScript',
                '.ts': 'TypeScript',
                '.tsx': 'TypeScript/React',
                '.jsx': 'JavaScript/React',
                '.java': 'Java',
                '.c': 'C',
                '.cpp': 'C++',
                '.cs': 'C#',
                '.go': 'Go',
                '.rb': 'Ruby',
                '.php': 'PHP',
                '.rs': 'Rust',
                '.kt': 'Kotlin',
                '.swift': 'Swift',
                '.sh': 'Shell Script',
                '.ps1': 'PowerShell'
            }
            
            if file_ext in language_map:
                analysis['languages'].add(language_map[file_ext])
                analysis['source_code'].append(file_path)
            
            # Identify configuration files
            config_files = ['requirements.txt', 'package.json', 'Dockerfile', 'docker-compose.yml', 
                          'config.json', 'config.yaml', '.env', 'setup.py', 'pyproject.toml']
            if file_name in config_files or file_ext in ['.json', '.yaml', '.yml', '.toml', '.ini']:
                analysis['config_files'].append(file_path)
            
            # Identify documentation
            if file_ext in ['.md', '.txt', '.rst'] or 'readme' in file_name.lower():
                analysis['documentation'].append(file_path)
            
            # Identify scripts
            if file_ext in ['.sh', '.bat', '.ps1'] or 'script' in file_name.lower():
                analysis['scripts'].append(file_path)
        
        # Try to identify frameworks from file contents
        try:
            for file_path in analysis['source_code'][:10]:  # Check first 10 source files
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(1000)  # Read first 1000 chars
                        
                        # Python frameworks
                        if 'django' in content.lower():
                            analysis['frameworks'].add('Django')
                        if 'flask' in content.lower():
                            analysis['frameworks'].add('Flask')
                        if 'fastapi' in content.lower():
                            analysis['frameworks'].add('FastAPI')
                        
                        # JavaScript frameworks
                        if 'react' in content.lower():
                            analysis['frameworks'].add('React')
                        if 'vue' in content.lower():
                            analysis['frameworks'].add('Vue.js')
                        if 'angular' in content.lower():
                            analysis['frameworks'].add('Angular')
                        if 'express' in content.lower():
                            analysis['frameworks'].add('Express.js')
                        
                except:
                    continue
        except:
            pass
        
        self.project_analysis = analysis
        return analysis

    def ask_project_questions(self):
        """Interactive questionnaire about the project"""
        print("\n" + "="*60)
        print("PROJECT REQUIREMENTS QUESTIONNAIRE")
        print("="*60)
        
        # Determine if project is new or existing
        is_new_project = True
        if self.existing_files:
            print(f"\n📁 Found {len(self.existing_files)} existing files in the project.")
            choice = input("Is this a NEW project or EXISTING project to be modified? (new/existing): ").strip().lower()
            is_new_project = choice.startswith('n')
        
        questions = {}
        
        # Basic project information
        questions['project_name'] = input("\n📝 Project Name: ").strip()
        questions['project_description'] = input("📝 Brief Project Description: ").strip()
        questions['project_type'] = input("📝 Project Type (web app, mobile app, API, CLI tool, etc.): ").strip()
        
        # Technical specifications
        print("\n🔧 TECHNICAL SPECIFICATIONS")
        
        if is_new_project:
            questions['primary_language'] = input("💻 Primary Programming Language: ").strip()
            questions['secondary_languages'] = input("💻 Secondary Languages (comma-separated, optional): ").strip()
            questions['frameworks'] = input("🛠️  Frameworks/Libraries to use: ").strip()
            questions['database'] = input("🗄️  Database (if any): ").strip()
        else:
            print(f"📊 Detected Languages: {', '.join(self.project_analysis.get('languages', []))}")
            print(f"📊 Detected Frameworks: {', '.join(self.project_analysis.get('frameworks', []))}")
            questions['additional_languages'] = input("💻 Additional Languages needed: ").strip()
            questions['additional_frameworks'] = input("🛠️  Additional Frameworks/Libraries: ").strip()
        
        # Scale and complexity
        print("\n📏 PROJECT SCALE")
        questions['estimated_files'] = input("📄 Estimated number of files needed: ").strip()
        questions['estimated_lines'] = input("📏 Estimated lines of code: ").strip()
        questions['estimated_functions'] = input("⚙️  Estimated number of functions/methods: ").strip()
        questions['complexity'] = input("🎯 Complexity Level (simple/medium/complex): ").strip()
        
        # Features and functionality
        print("\n🎯 FEATURES & FUNCTIONALITY")
        questions['core_features'] = input("🎯 Core Features (comma-separated): ").strip()
        questions['user_interface'] = input("🖥️  User Interface Type (CLI, Web UI, Mobile, API only): ").strip()
        questions['integrations'] = input("🔗 External Integrations (APIs, services): ").strip()
        
        # Performance and requirements
        print("\n⚡ PERFORMANCE & REQUIREMENTS")
        questions['performance_requirements'] = input("⚡ Performance Requirements: ").strip()
        questions['scalability'] = input("📈 Scalability Needs: ").strip()
        questions['security_requirements'] = input("🔒 Security Requirements: ").strip()
        
        # Timeline and resources
        print("\n⏰ TIMELINE & RESOURCES")
        questions['timeline'] = input("⏰ Development Timeline: ").strip()
        questions['team_size'] = input("👥 Team Size: ").strip()
        questions['budget_constraints'] = input("💰 Budget Constraints: ").strip()
        
        # Target audience
        print("\n👥 TARGET AUDIENCE")
        questions['target_users'] = input("👥 Target Users: ").strip()
        questions['user_expertise'] = input("🎓 User Technical Expertise Level: ").strip()
        
        # Additional context
        print("\n📋 ADDITIONAL CONTEXT")
        questions['business_goals'] = input("🎯 Business Goals: ").strip()
        questions['success_metrics'] = input("📊 Success Metrics: ").strip()
        questions['constraints'] = input("⚠️  Known Constraints/Limitations: ").strip()
        questions['special_requirements'] = input("⭐ Special Requirements: ").strip()
        
        return questions, is_new_project

    def generate_comprehensive_prd(self, questions, is_new_project):
        """Generate a comprehensive PRD based on project analysis and user input"""
        
        # Prepare context for the AI
        context = f"""
**PROJECT CONTEXT:**
Project Type: {"New Project" if is_new_project else "Existing Project Enhancement"}

**EXISTING PROJECT ANALYSIS:**
"""
        
        if self.project_info:
            context += f"Project Info Summary:\n{self.project_info[:2000]}...\n\n"
        
        if self.project_analysis:
            context += f"""
Current Project Statistics:
- Total Files: {self.project_analysis.get('total_files', 0)}
- Languages: {', '.join(self.project_analysis.get('languages', []))}
- Frameworks: {', '.join(self.project_analysis.get('frameworks', []))}
- File Types: {dict(list(self.project_analysis.get('file_types', {}).items())[:10])}
- Source Code Files: {len(self.project_analysis.get('source_code', []))}
- Configuration Files: {len(self.project_analysis.get('config_files', []))}

"""
        
        context += "**USER REQUIREMENTS:**\n"
        for key, value in questions.items():
            if value.strip():
                context += f"- {key.replace('_', ' ').title()}: {value}\n"
        
        context += """

**INSTRUCTIONS:**
Create a comprehensive PRD that includes:
1. Technical specifications based on the existing codebase analysis
2. Detailed implementation plan considering current project structure
3. Specific file organization and coding standards
4. Integration requirements with existing systems
5. Migration strategy if modifying existing project
6. Detailed development timeline with milestones
7. Resource allocation and team structure recommendations
8. Risk assessment specific to the technology stack
9. Testing strategy including unit, integration, and system tests
10. Deployment and maintenance considerations

Make the PRD actionable with specific technical details, code structure recommendations, and clear acceptance criteria for each feature.
"""
        
        try:
            response = self.prd_agent.run(context)
            return response.content
        except Exception as e:
            return f"Error generating PRD: {str(e)}"

    def generate_prd(self, product_idea: str, **kwargs) -> str:
        """Generate a comprehensive PRD based on product idea and optional context"""
        
        prompt = f"**Product Idea:** {product_idea}\n"
        
        # Add optional context if provided
        if kwargs.get('target_audience'):
            prompt += f"**Target Audience:** {kwargs['target_audience']}\n"
        if kwargs.get('business_goals'):
            prompt += f"**Business Goals:** {kwargs['business_goals']}\n"
        if kwargs.get('technical_constraints'):
            prompt += f"**Technical Constraints:** {kwargs['technical_constraints']}\n"
        if kwargs.get('timeline'):
            prompt += f"**Timeline:** {kwargs['timeline']}\n"
        
        prompt += "\nCreate a comprehensive PRD with actionable insights and measurable success criteria."
        
        try:
            response = self.prd_agent.run(prompt)
            return response.content
        except Exception as e:
            return f"Error generating PRD: {str(e)}"

    def interactive_mode(self):
        """Enhanced interactive mode with project analysis"""
        print("="*80)
        print("🚀 ENHANCED PRD GENERATOR")
        print("="*80)
        
        # Step 1: Read project info
        print("\n📊 STEP 1: ANALYZING EXISTING PROJECT")
        self.read_project_info()
        
        # Step 2: Scan existing files
        print("\n🔍 STEP 2: SCANNING PROJECT FILES")
        self.scan_existing_files()
        
        # Step 3: Analyze project structure
        print("\n🔬 STEP 3: ANALYZING PROJECT STRUCTURE")
        analysis = self.analyze_project_structure()
        
        if analysis['total_files'] > 0:
            print(f"\n📈 PROJECT ANALYSIS SUMMARY:")
            print(f"   • Total Files: {analysis['total_files']}")
            print(f"   • Languages: {', '.join(analysis['languages']) if analysis['languages'] else 'None detected'}")
            print(f"   • Frameworks: {', '.join(analysis['frameworks']) if analysis['frameworks'] else 'None detected'}")
            print(f"   • Source Files: {len(analysis['source_code'])}")
            print(f"   • Config Files: {len(analysis['config_files'])}")
            print(f"   • Documentation: {len(analysis['documentation'])}")
        
        # Step 4: Interactive questionnaire
        print("\n❓ STEP 4: PROJECT REQUIREMENTS QUESTIONNAIRE")
        questions, is_new_project = self.ask_project_questions()
        
        # Step 5: Generate PRD
        print("\n🤖 STEP 5: GENERATING COMPREHENSIVE PRD")
        print("This may take a moment...")
        
        prd = self.generate_comprehensive_prd(questions, is_new_project)
        
        print("\n" + "="*80)
        print("📋 GENERATED PRD:")
        print("="*80)
        print(prd)
        
        # Step 6: Save PRD automatically
        print("\n💾 STEP 6: SAVING PRD")
        project_name = questions.get('project_name', 'project').replace(' ', '_').replace('/', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"PRD_{project_name}_{timestamp}.md"
        result = self.save_prd(prd, filename)
        print(f"✅ {result}")
        
        return prd

    def simple_mode(self):
        """Simple mode for quick PRD generation"""
        print("=== SIMPLE PRD GENERATOR ===")
        print("Enter your product details (press Enter to skip optional fields):\n")
        
        product_idea = input("Product Idea (required): ").strip()
        if not product_idea:
            print("Product idea is required!")
            return
        
        target_audience = input("Target Audience (optional): ").strip()
        business_goals = input("Business Goals (optional): ").strip()
        technical_constraints = input("Technical Constraints (optional): ").strip()
        timeline = input("Timeline/Deadline (optional): ").strip()
        
        print("\nGenerating PRD...")
        
        kwargs = {}
        if target_audience: kwargs['target_audience'] = target_audience
        if business_goals: kwargs['business_goals'] = business_goals
        if technical_constraints: kwargs['technical_constraints'] = technical_constraints
        if timeline: kwargs['timeline'] = timeline
        
        prd = self.generate_prd(product_idea, **kwargs)
        
        print("\n" + "="*80)
        print("GENERATED PRD:")
        print("="*80)
        print(prd)
        
        # Auto-save PRD
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"PRD_Simple_{timestamp}.md"
        result = self.save_prd(prd, filename)
        print(f"\n✅ {result}")

    def save_prd(self, prd_content: str, filename: str = None) -> str:
        """Save the generated PRD to a file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"PRD_{timestamp}.md"
        
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(prd_content)
            return f"PRD saved successfully to {filename}"
        except Exception as e:
            return f"Error saving PRD: {str(e)}"

def main():
    """Enhanced main function with mode selection"""
    generator = PRDGenerator()
    
    print("🚀 PRD GENERATOR")
    print("Choose your mode:")
    print("1. Enhanced Mode (Full project analysis + questionnaire)")
    print("2. Simple Mode (Quick PRD generation)")
    print("3. Demo Mode (Example PRD)")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == "1":
        generator.interactive_mode()
    elif choice == "2":
        generator.simple_mode()
    elif choice == "3":
        # Demo mode with example
        print("\n🎯 DEMO MODE: Generating example PRD...")
        product_idea = "AI-powered code review tool that integrates with GitHub and analyzes code quality, security vulnerabilities, and suggests improvements"
        
        prd = generator.generate_prd(
            product_idea,
            target_audience="Software developers, engineering teams, and DevOps professionals",
            business_goals="Improve code quality, reduce review time by 50%, and catch security issues early",
            technical_constraints="Must integrate with GitHub API, support multiple programming languages, and provide real-time feedback",
            timeline="6 months MVP, 12 months full release"
        )
        
        print("\n" + "="*80)
        print("DEMO PRD:")
        print("="*80)
        print(prd)
        print("="*80)
        
        # Auto-save demo PRD
        result = generator.save_prd(prd, "Demo_PRD_AI_Code_Review_Tool.md")
        print(f"\n✅ {result}")
    else:
        print("Invalid choice. Running enhanced mode by default...")
        generator.interactive_mode()

if __name__ == "__main__":
    main()