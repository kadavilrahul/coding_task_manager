"""
Interactive PRD (Product Requirements Document) generation.
Creates comprehensive PRDs based on project analysis and user input.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from .path_manager import PathManager
from .config_manager import ConfigManager


class PRDGenerator:
    """Generates Product Requirements Documents interactively."""
    
    def __init__(self, path_manager: PathManager, config_manager: ConfigManager):
        """Initialize PRD generator."""
        self.path_manager = path_manager
        self.config_manager = config_manager
        self.template_manager = TemplateManager(path_manager)
    
    def generate_interactive_prd(self, template: Optional[str] = None, 
                               questions_file: Optional[str] = None) -> str:
        """Generate PRD through interactive questioning."""
        print("\n🎯 Interactive PRD Generation")
        print("=" * 40)
        
        # Load base template if specified
        if template:
            base_content = self.template_manager.load_prd_template(template)
        else:
            base_content = self.template_manager.get_default_prd_template()
        
        # Load custom questions if provided
        if questions_file:
            questions = self._load_custom_questions(questions_file)
        else:
            questions = self._get_default_questions()
        
        # Collect answers
        answers = self._collect_answers(questions)
        
        # Generate PRD content
        prd_content = self._generate_prd_content(base_content, answers)
        
        return prd_content
    
    def generate_from_template(self, template: str) -> str:
        """Generate PRD from a template with minimal input."""
        config = self.config_manager.get_config()
        
        template_content = self.template_manager.load_prd_template(template)
        
        # Replace template variables with config values
        replacements = {
            '{{PROJECT_NAME}}': config.project_name,
            '{{PROJECT_TYPE}}': config.project_type,
            '{{DESCRIPTION}}': config.description,
            '{{TECH_STACK}}': ', '.join(config.tech_stack),
            '{{DATE}}': datetime.now().strftime('%Y-%m-%d'),
            '{{VERSION}}': config.version
        }
        
        prd_content = template_content
        for placeholder, value in replacements.items():
            prd_content = prd_content.replace(placeholder, value)
        
        return prd_content
    
    def generate_basic_prd(self) -> str:
        """Generate a basic PRD with minimal information."""
        config = self.config_manager.get_config()
        
        prd_content = f"""# Product Requirements Document

## Project: {config.project_name}

### Overview
{config.description or 'Project description to be added.'}

### Project Information
- **Type**: {config.project_type}
- **Technology Stack**: {', '.join(config.tech_stack) if config.tech_stack else 'To be determined'}
- **Architecture**: {config.architecture}
- **Version**: {config.version}
- **Date**: {datetime.now().strftime('%Y-%m-%d')}

### Features
## Task 1: Project Setup
- Initialize project structure
- Set up development environment
- Configure build tools

## Task 2: Core Implementation
- Implement main functionality
- Add error handling
- Write unit tests

## Task 3: Documentation
- Write user documentation
- Add code comments
- Create API documentation

### Technical Requirements
- Follow {config.coding_standards} coding standards
- Use {config.testing_framework} for testing
- Maintain code coverage above 80%

### Success Criteria
- All features implemented and tested
- Documentation complete
- Code review passed
- Performance requirements met
"""
        
        return prd_content
    
    def generate_prompt_file(self, prd_content: str) -> str:
        """Generate a prompt.txt file based on PRD content."""
        config = self.config_manager.get_config()
        
        prompt_content = f"""# AI Assistant Context for {config.project_name}

## Project Overview
This is a {config.project_type} project using {', '.join(config.tech_stack) if config.tech_stack else 'various technologies'}.

## Current Task Context
Based on the PRD, the main tasks are:
{self._extract_tasks_from_prd(prd_content)}

## Code Guidelines
- Follow {config.coding_standards} coding standards
- Use {config.testing_framework} for testing
- Maintain clean, readable code
- Add comprehensive comments
- Write unit tests for all functions

## Project Structure
- Source code in: {', '.join(config.source_dirs)}
- Tests in: {', '.join(config.test_dirs)}
- Architecture: {config.architecture}

## AI Instructions
When helping with this project:
1. Always consider the project type and architecture
2. Follow the established coding standards
3. Suggest improvements for code quality
4. Provide complete, working code examples
5. Include error handling and edge cases
6. Write appropriate tests
7. Update documentation when needed

## Current Focus
Please help implement the features described in the PRD while maintaining code quality and following best practices.
"""
        
        return prompt_content
    
    def _get_default_questions(self) -> List[Dict[str, Any]]:
        """Get default questions for PRD generation."""
        return [
            {
                'key': 'project_goal',
                'question': 'What is the main goal of this project?',
                'type': 'text',
                'required': True
            },
            {
                'key': 'target_users',
                'question': 'Who are the target users?',
                'type': 'text',
                'required': True
            },
            {
                'key': 'key_features',
                'question': 'What are the key features? (comma-separated)',
                'type': 'list',
                'required': True
            },
            {
                'key': 'success_criteria',
                'question': 'What defines success for this project?',
                'type': 'text',
                'required': True
            },
            {
                'key': 'timeline',
                'question': 'What is the expected timeline?',
                'type': 'text',
                'required': False
            },
            {
                'key': 'constraints',
                'question': 'Are there any constraints or limitations?',
                'type': 'text',
                'required': False
            },
            {
                'key': 'integrations',
                'question': 'What external systems need integration?',
                'type': 'list',
                'required': False
            },
            {
                'key': 'performance_requirements',
                'question': 'Any specific performance requirements?',
                'type': 'text',
                'required': False
            }
        ]
    
    def _load_custom_questions(self, questions_file: str) -> List[Dict[str, Any]]:
        """Load custom questions from a file."""
        questions_path = self.path_manager.resolve_path(questions_file)
        
        try:
            with open(questions_path, 'r', encoding='utf-8') as f:
                questions = json.load(f)
            return questions
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load custom questions: {e}")
            return self._get_default_questions()
    
    def _collect_answers(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Collect answers to questions interactively."""
        answers = {}
        
        for question in questions:
            key = question['key']
            prompt = question['question']
            q_type = question.get('type', 'text')
            required = question.get('required', False)
            
            while True:
                if required:
                    answer = input(f"{prompt} (required): ").strip()
                else:
                    answer = input(f"{prompt} (optional): ").strip()
                
                if not answer and required:
                    print("This field is required. Please provide an answer.")
                    continue
                
                if q_type == 'list' and answer:
                    answer = [item.strip() for item in answer.split(',')]
                
                answers[key] = answer
                break
        
        return answers
    
    def _generate_prd_content(self, base_content: str, answers: Dict[str, Any]) -> str:
        """Generate final PRD content from template and answers."""
        config = self.config_manager.get_config()
        
        # Standard replacements
        replacements = {
            '{{PROJECT_NAME}}': config.project_name,
            '{{PROJECT_TYPE}}': config.project_type,
            '{{DESCRIPTION}}': config.description,
            '{{TECH_STACK}}': ', '.join(config.tech_stack),
            '{{DATE}}': datetime.now().strftime('%Y-%m-%d'),
            '{{VERSION}}': config.version,
            '{{ARCHITECTURE}}': config.architecture
        }
        
        # Add answers as replacements
        for key, value in answers.items():
            placeholder = f'{{{{{key.upper()}}}}}'
            if isinstance(value, list):
                replacements[placeholder] = ', '.join(value)
            else:
                replacements[placeholder] = str(value)
        
        # Generate features section from key features
        if 'key_features' in answers and answers['key_features']:
            features_section = self._generate_features_section(answers['key_features'])
            replacements['{{FEATURES_SECTION}}'] = features_section
        
        # Apply replacements
        prd_content = base_content
        for placeholder, value in replacements.items():
            prd_content = prd_content.replace(placeholder, value)
        
        return prd_content
    
    def _generate_features_section(self, features: List[str]) -> str:
        """Generate features section from feature list."""
        features_section = "### Features\n\n"
        
        for i, feature in enumerate(features, 1):
            feature_name = feature.strip()
            task_id = f"Task {i}"
            
            features_section += f"## {task_id}: {feature_name}\n"
            
            # Generate sub-tasks based on feature name
            subtasks = self._generate_subtasks_for_feature(feature_name)
            for subtask in subtasks:
                features_section += f"- {subtask}\n"
            
            features_section += "\n"
        
        return features_section
    
    def _generate_subtasks_for_feature(self, feature_name: str) -> List[str]:
        """Generate subtasks for a feature based on common patterns."""
        feature_lower = feature_name.lower()
        
        # Common subtask patterns
        if 'auth' in feature_lower or 'login' in feature_lower:
            return [
                "Design authentication flow",
                "Implement login functionality",
                "Add password reset feature",
                "Create user registration",
                "Add session management"
            ]
        elif 'api' in feature_lower:
            return [
                "Design API endpoints",
                "Implement request/response handling",
                "Add input validation",
                "Write API documentation",
                "Add error handling"
            ]
        elif 'database' in feature_lower or 'data' in feature_lower:
            return [
                "Design database schema",
                "Set up database connection",
                "Implement data models",
                "Add data validation",
                "Create migration scripts"
            ]
        elif 'ui' in feature_lower or 'interface' in feature_lower:
            return [
                "Create wireframes",
                "Design user interface",
                "Implement responsive layout",
                "Add user interactions",
                "Test usability"
            ]
        else:
            # Generic subtasks
            return [
                f"Design {feature_name} architecture",
                f"Implement core {feature_name} functionality",
                f"Add {feature_name} validation",
                f"Write {feature_name} tests",
                f"Document {feature_name} usage"
            ]
    
    def _extract_tasks_from_prd(self, prd_content: str) -> str:
        """Extract tasks from PRD content for prompt file."""
        lines = prd_content.split('\n')
        tasks = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('## Task') or line.startswith('# Task'):
                tasks.append(line.replace('#', '').strip())
        
        if tasks:
            return '\n'.join(f"- {task}" for task in tasks)
        else:
            return "- Tasks will be extracted from the PRD"


class TemplateManager:
    """Manages PRD and prompt templates."""
    
    def __init__(self, path_manager: PathManager):
        """Initialize template manager."""
        self.path_manager = path_manager
        self.templates_dir = path_manager.get_templates_dir()
    
    def load_prd_template(self, template_name: str) -> str:
        """Load a PRD template by name."""
        template_path = self.templates_dir / "prd_templates" / f"{template_name}.md"
        
        if template_path.exists():
            return template_path.read_text(encoding='utf-8')
        else:
            print(f"Warning: Template '{template_name}' not found. Using default.")
            return self.get_default_prd_template()
    
    def get_default_prd_template(self) -> str:
        """Get the default PRD template."""
        return """# Product Requirements Document

## Project: {{PROJECT_NAME}}

### Overview
{{DESCRIPTION}}

### Project Information
- **Type**: {{PROJECT_TYPE}}
- **Technology Stack**: {{TECH_STACK}}
- **Architecture**: {{ARCHITECTURE}}
- **Version**: {{VERSION}}
- **Date**: {{DATE}}

### Project Goals
{{PROJECT_GOAL}}

### Target Users
{{TARGET_USERS}}

{{FEATURES_SECTION}}

### Success Criteria
{{SUCCESS_CRITERIA}}

### Timeline
{{TIMELINE}}

### Constraints
{{CONSTRAINTS}}

### Integrations
{{INTEGRATIONS}}

### Performance Requirements
{{PERFORMANCE_REQUIREMENTS}}

### Technical Requirements
- Follow established coding standards
- Implement comprehensive testing
- Maintain documentation
- Ensure security best practices

---
*Generated by AI-Enhanced Task Management System*
"""
    
    def setup_project_templates(self, project_type: str) -> None:
        """Set up project-specific templates."""
        # Create template directories
        prd_templates_dir = self.templates_dir / "prd_templates"
        prompt_templates_dir = self.templates_dir / "prompt_templates"
        
        prd_templates_dir.mkdir(parents=True, exist_ok=True)
        prompt_templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Create project-type specific templates
        self._create_project_type_templates(project_type, prd_templates_dir, prompt_templates_dir)
    
    def _create_project_type_templates(self, project_type: str, prd_dir: Path, prompt_dir: Path) -> None:
        """Create templates specific to project type."""
        templates = {
            'web-app': {
                'prd': self._get_web_app_prd_template(),
                'prompt': self._get_web_app_prompt_template()
            },
            'mobile-app': {
                'prd': self._get_mobile_app_prd_template(),
                'prompt': self._get_mobile_app_prompt_template()
            },
            'api': {
                'prd': self._get_api_prd_template(),
                'prompt': self._get_api_prompt_template()
            },
            'library': {
                'prd': self._get_library_prd_template(),
                'prompt': self._get_library_prompt_template()
            }
        }
        
        if project_type in templates:
            template_data = templates[project_type]
            
            # Save PRD template
            prd_file = prd_dir / f"{project_type}.md"
            prd_file.write_text(template_data['prd'], encoding='utf-8')
            
            # Save prompt template
            prompt_file = prompt_dir / f"{project_type}.txt"
            prompt_file.write_text(template_data['prompt'], encoding='utf-8')
    
    def _get_web_app_prd_template(self) -> str:
        """Get web application PRD template."""
        return """# Web Application PRD

## Project: {{PROJECT_NAME}}

### Overview
{{DESCRIPTION}}

### Features
## Task 1: Frontend Development
- Set up React/Vue/Angular framework
- Create responsive UI components
- Implement routing
- Add state management

## Task 2: Backend Development
- Set up server framework
- Create API endpoints
- Implement authentication
- Add database integration

## Task 3: Integration & Testing
- Connect frontend to backend
- Write unit and integration tests
- Add error handling
- Optimize performance

### Technical Stack
- Frontend: {{TECH_STACK}}
- Backend: Node.js/Python/Java
- Database: PostgreSQL/MongoDB
- Deployment: Docker/Cloud

### Success Criteria
- Responsive design across devices
- Fast loading times (<3 seconds)
- Secure authentication
- 99% uptime
"""
    
    def _get_web_app_prompt_template(self) -> str:
        """Get web application prompt template."""
        return """You are helping with a web application project. Focus on:
- Modern web development practices
- Responsive design
- Performance optimization
- Security best practices
- Clean, maintainable code
- Cross-browser compatibility
"""
    
    def _get_mobile_app_prd_template(self) -> str:
        """Get mobile application PRD template."""
        return """# Mobile Application PRD

## Project: {{PROJECT_NAME}}

### Features
## Task 1: App Structure
- Set up React Native/Flutter project
- Create navigation structure
- Design app architecture
- Set up state management

## Task 2: Core Features
- Implement main functionality
- Add user authentication
- Create data persistence
- Add offline capabilities

## Task 3: Platform Integration
- Add platform-specific features
- Implement push notifications
- Add app store optimization
- Test on multiple devices

### Platform Requirements
- iOS 12+ and Android 8+
- Responsive design
- Offline functionality
- Push notifications
"""
    
    def _get_mobile_app_prompt_template(self) -> str:
        """Get mobile application prompt template."""
        return """You are helping with a mobile application project. Focus on:
- Cross-platform compatibility
- Mobile UI/UX best practices
- Performance optimization for mobile
- Platform-specific guidelines
- Offline functionality
- Battery efficiency
"""
    
    def _get_api_prd_template(self) -> str:
        """Get API PRD template."""
        return """# API Development PRD

## Project: {{PROJECT_NAME}}

### Features
## Task 1: API Design
- Design RESTful endpoints
- Create API documentation
- Define data models
- Set up authentication

## Task 2: Implementation
- Implement CRUD operations
- Add input validation
- Implement error handling
- Add rate limiting

## Task 3: Testing & Documentation
- Write comprehensive tests
- Create API documentation
- Add monitoring
- Optimize performance

### Technical Requirements
- RESTful design principles
- OpenAPI/Swagger documentation
- Authentication & authorization
- Rate limiting & caching
"""
    
    def _get_api_prompt_template(self) -> str:
        """Get API prompt template."""
        return """You are helping with an API development project. Focus on:
- RESTful design principles
- Proper HTTP status codes
- Input validation and sanitization
- Error handling and logging
- API documentation
- Security best practices
- Performance optimization
"""
    
    def _get_library_prd_template(self) -> str:
        """Get library PRD template."""
        return """# Library Development PRD

## Project: {{PROJECT_NAME}}

### Features
## Task 1: Core Library
- Design public API
- Implement core functionality
- Add error handling
- Create documentation

## Task 2: Testing & Quality
- Write comprehensive tests
- Add code coverage
- Set up CI/CD
- Add linting and formatting

## Task 3: Distribution
- Package for distribution
- Create usage examples
- Write installation guide
- Publish to package registry

### Quality Standards
- 100% test coverage
- Comprehensive documentation
- Semantic versioning
- Backward compatibility
"""
    
    def _get_library_prompt_template(self) -> str:
        """Get library prompt template."""
        return """You are helping with a library development project. Focus on:
- Clean, well-documented public API
- Comprehensive testing
- Backward compatibility
- Clear documentation with examples
- Following language conventions
- Minimal dependencies
- Performance optimization
"""