"""
Main application entry point for the AI-Enhanced Task Management System.
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import argparse
import sys

from core.task_manager import TaskManager
from core.prd_generator import PRDGenerator
from agents.analyzer_agent import AnalyzerAgent
from agents.planner_agent import PlannerAgent
from agents.modifier_agent import ModifierAgent
from agents.validator_agent import ValidatorAgent
from utils.file_utils import FileUtils
from utils.ai_utils import AIUtils


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class AITaskManagementApp:
    """Main application class for the AI-Enhanced Task Management System."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the application."""
        self.config_path = config_path or Path("config.json")
        self.config = self._load_config()
        
        # Initialize components
        self.task_manager = TaskManager(self.config.get('task_manager', {}))
        self.prd_generator = PRDGenerator(self.config.get('prd_generator', {}))
        
        # Initialize agents
        self.analyzer_agent = AnalyzerAgent(self.config.get('analyzer_agent', {}))
        self.planner_agent = PlannerAgent(self.config.get('planner_agent', {}))
        self.modifier_agent = ModifierAgent(self.config.get('modifier_agent', {}))
        self.validator_agent = ValidatorAgent(self.config.get('validator_agent', {}))
        
        logger.info("AI Task Management System initialized successfully")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load application configuration."""
        if FileUtils.file_exists(self.config_path):
            try:
                config = FileUtils.read_json(self.config_path)
                logger.info(f"Configuration loaded from {self.config_path}")
                return config
            except Exception as e:
                logger.warning(f"Failed to load config from {self.config_path}: {e}")
        
        # Return default configuration
        default_config = {
            "task_manager": {
                "max_concurrent_tasks": 5,
                "task_timeout": 300,
                "auto_save": True
            },
            "prd_generator": {
                "template_dir": "templates",
                "output_dir": "output",
                "default_format": "markdown"
            },
            "analyzer_agent": {
                "analysis_depth": "deep",
                "include_metrics": True
            },
            "planner_agent": {
                "planning_strategy": "adaptive",
                "max_iterations": 10
            },
            "modifier_agent": {
                "backup_enabled": True,
                "validation_enabled": True
            },
            "validator_agent": {
                "strict_mode": False,
                "auto_fix": True
            },
            "ai_utils": {
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 2000
            }
        }
        
        # Save default config
        try:
            FileUtils.write_json(self.config_path, default_config)
            logger.info(f"Default configuration saved to {self.config_path}")
        except Exception as e:
            logger.warning(f"Failed to save default config: {e}")
        
        return default_config
    
    async def run_interactive_mode(self):
        """Run the application in interactive mode."""
        print("🚀 AI-Enhanced Task Management System")
        print("=====================================")
        print()
        
        while True:
            try:
                print("\nAvailable commands:")
                print("1. Generate PRD")
                print("2. Analyze code")
                print("3. Plan implementation")
                print("4. Modify code")
                print("5. Validate changes")
                print("6. Run full workflow")
                print("7. Show status")
                print("8. Exit")
                print()
                
                choice = input("Enter your choice (1-8): ").strip()
                
                if choice == "1":
                    await self._handle_generate_prd()
                elif choice == "2":
                    await self._handle_analyze_code()
                elif choice == "3":
                    await self._handle_plan_implementation()
                elif choice == "4":
                    await self._handle_modify_code()
                elif choice == "5":
                    await self._handle_validate_changes()
                elif choice == "6":
                    await self._handle_full_workflow()
                elif choice == "7":
                    await self._handle_show_status()
                elif choice == "8":
                    print("Goodbye! 👋")
                    break
                else:
                    print("Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\nExiting... 👋")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {e}")
                print(f"An error occurred: {e}")
    
    async def _handle_generate_prd(self):
        """Handle PRD generation."""
        print("\n📋 Generate Product Requirements Document")
        print("-" * 40)
        
        project_name = input("Project name: ").strip()
        if not project_name:
            print("Project name is required.")
            return
        
        description = input("Project description: ").strip()
        
        project_info = {
            "title": project_name,
            "description": description,
            "author": "AI Assistant",
            "version": "1.0"
        }
        
        try:
            print("Generating PRD...")
            prd_content = await self.prd_generator.generate_prd(project_info)
            
            output_file = Path(f"output/{project_name.lower().replace(' ', '_')}_prd.md")
            output_file.parent.mkdir(exist_ok=True)
            
            FileUtils.write_file(output_file, prd_content)
            print(f"✅ PRD generated successfully: {output_file}")
            
        except Exception as e:
            logger.error(f"Failed to generate PRD: {e}")
            print(f"❌ Failed to generate PRD: {e}")
    
    async def _handle_analyze_code(self):
        """Handle code analysis."""
        print("\n🔍 Analyze Code")
        print("-" * 20)
        
        file_path = input("Enter file path to analyze: ").strip()
        if not file_path:
            print("File path is required.")
            return
        
        path = Path(file_path)
        if not path.exists():
            print(f"File not found: {path}")
            return
        
        try:
            print("Analyzing code...")
            analysis_result = await self.analyzer_agent.analyze_file(path)
            
            print("✅ Analysis completed!")
            print(f"Functions found: {len(analysis_result.get('functions', []))}")
            print(f"Classes found: {len(analysis_result.get('classes', []))}")
            print(f"Complexity score: {analysis_result.get('complexity', 'N/A')}")
            
            # Save analysis result
            output_file = Path(f"output/{path.stem}_analysis.json")
            output_file.parent.mkdir(exist_ok=True)
            FileUtils.write_json(output_file, analysis_result)
            print(f"Analysis saved to: {output_file}")
            
        except Exception as e:
            logger.error(f"Failed to analyze code: {e}")
            print(f"❌ Failed to analyze code: {e}")
    
    async def _handle_plan_implementation(self):
        """Handle implementation planning."""
        print("\n📋 Plan Implementation")
        print("-" * 25)
        
        requirements = input("Enter requirements (comma-separated): ").strip()
        if not requirements:
            print("Requirements are required.")
            return
        
        req_list = [req.strip() for req in requirements.split(",")]
        
        try:
            print("Creating implementation plan...")
            plan = await self.planner_agent.create_implementation_plan(req_list)
            
            print("✅ Implementation plan created!")
            print(f"Total tasks: {len(plan.get('tasks', []))}")
            print(f"Estimated duration: {plan.get('estimated_duration', 'N/A')}")
            
            # Save plan
            output_file = Path("output/implementation_plan.json")
            output_file.parent.mkdir(exist_ok=True)
            FileUtils.write_json(output_file, plan)
            print(f"Plan saved to: {output_file}")
            
        except Exception as e:
            logger.error(f"Failed to create plan: {e}")
            print(f"❌ Failed to create plan: {e}")
    
    async def _handle_modify_code(self):
        """Handle code modification."""
        print("\n✏️  Modify Code")
        print("-" * 15)
        
        file_path = input("Enter file path to modify: ").strip()
        if not file_path:
            print("File path is required.")
            return
        
        path = Path(file_path)
        if not path.exists():
            print(f"File not found: {path}")
            return
        
        modification_type = input("Modification type (create/update/delete): ").strip().lower()
        if modification_type not in ["create", "update", "delete"]:
            print("Invalid modification type.")
            return
        
        try:
            print("Applying modifications...")
            
            if modification_type == "update":
                modifications = [
                    {
                        "type": "replace",
                        "target": "# TODO: Implement this",
                        "replacement": "# Implementation completed",
                        "line_number": None
                    }
                ]
                result = await self.modifier_agent.update_file(path, modifications)
            else:
                print(f"Modification type '{modification_type}' not implemented in demo.")
                return
            
            if result.get("success"):
                print("✅ Code modified successfully!")
            else:
                print(f"❌ Modification failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"Failed to modify code: {e}")
            print(f"❌ Failed to modify code: {e}")
    
    async def _handle_validate_changes(self):
        """Handle change validation."""
        print("\n✅ Validate Changes")
        print("-" * 20)
        
        file_path = input("Enter file path to validate: ").strip()
        if not file_path:
            print("File path is required.")
            return
        
        path = Path(file_path)
        if not path.exists():
            print(f"File not found: {path}")
            return
        
        try:
            print("Validating changes...")
            validation_result = await self.validator_agent.validate_file(path)
            
            if validation_result.get("is_valid"):
                print("✅ Validation passed!")
            else:
                print("❌ Validation failed!")
                issues = validation_result.get("issues", [])
                for issue in issues:
                    print(f"  - {issue.get('message', 'Unknown issue')}")
            
        except Exception as e:
            logger.error(f"Failed to validate changes: {e}")
            print(f"❌ Failed to validate changes: {e}")
    
    async def _handle_full_workflow(self):
        """Handle full workflow execution."""
        print("\n🔄 Run Full Workflow")
        print("-" * 25)
        
        print("This will run the complete AI-enhanced development workflow:")
        print("1. Analyze existing code")
        print("2. Generate implementation plan")
        print("3. Apply modifications")
        print("4. Validate changes")
        print()
        
        confirm = input("Continue? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Workflow cancelled.")
            return
        
        try:
            # Create a sample task
            task_data = {
                "title": "Sample Development Task",
                "description": "Demonstrate the full AI workflow",
                "requirements": ["Analyze code", "Plan implementation", "Apply changes", "Validate results"],
                "priority": "medium"
            }
            
            print("Creating task...")
            task = await self.task_manager.create_task(task_data)
            
            print(f"✅ Task created: {task.get('id')}")
            print("Full workflow demonstration completed!")
            
        except Exception as e:
            logger.error(f"Failed to run full workflow: {e}")
            print(f"❌ Failed to run full workflow: {e}")
    
    async def _handle_show_status(self):
        """Handle status display."""
        print("\n📊 System Status")
        print("-" * 20)
        
        try:
            # Get task manager status
            tasks = await self.task_manager.get_all_tasks()
            
            print(f"Total tasks: {len(tasks)}")
            
            # Count tasks by status
            status_counts = {}
            for task in tasks:
                status = task.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            for status, count in status_counts.items():
                print(f"  {status}: {count}")
            
            print(f"\nConfiguration file: {self.config_path}")
            print(f"Logging level: {logging.getLogger().level}")
            
        except Exception as e:
            logger.error(f"Failed to get status: {e}")
            print(f"❌ Failed to get status: {e}")
    
    async def run_cli_mode(self, args):
        """Run the application in CLI mode."""
        if args.command == "generate-prd":
            await self._cli_generate_prd(args)
        elif args.command == "analyze":
            await self._cli_analyze_code(args)
        elif args.command == "plan":
            await self._cli_plan_implementation(args)
        elif args.command == "modify":
            await self._cli_modify_code(args)
        elif args.command == "validate":
            await self._cli_validate_changes(args)
        else:
            print(f"Unknown command: {args.command}")
    
    async def _cli_generate_prd(self, args):
        """CLI PRD generation."""
        project_info = {
            "title": args.project_name,
            "description": args.description or "",
            "author": "AI Assistant",
            "version": "1.0"
        }
        
        prd_content = await self.prd_generator.generate_prd(project_info)
        
        output_file = Path(args.output) if args.output else Path(f"{args.project_name.lower().replace(' ', '_')}_prd.md")
        FileUtils.write_file(output_file, prd_content)
        
        print(f"PRD generated: {output_file}")
    
    async def _cli_analyze_code(self, args):
        """CLI code analysis."""
        path = Path(args.file)
        analysis_result = await self.analyzer_agent.analyze_file(path)
        
        if args.output:
            FileUtils.write_json(Path(args.output), analysis_result)
            print(f"Analysis saved to: {args.output}")
        else:
            print("Analysis completed:")
            print(f"Functions: {len(analysis_result.get('functions', []))}")
            print(f"Classes: {len(analysis_result.get('classes', []))}")
    
    async def _cli_plan_implementation(self, args):
        """CLI implementation planning."""
        requirements = args.requirements.split(",")
        plan = await self.planner_agent.create_implementation_plan(requirements)
        
        if args.output:
            FileUtils.write_json(Path(args.output), plan)
            print(f"Plan saved to: {args.output}")
        else:
            print(f"Plan created with {len(plan.get('tasks', []))} tasks")
    
    async def _cli_modify_code(self, args):
        """CLI code modification."""
        path = Path(args.file)
        # Simplified modification for CLI
        modifications = [{"type": "update", "description": args.description}]
        result = await self.modifier_agent.update_file(path, modifications)
        
        if result.get("success"):
            print("Code modified successfully")
        else:
            print(f"Modification failed: {result.get('error')}")
    
    async def _cli_validate_changes(self, args):
        """CLI change validation."""
        path = Path(args.file)
        validation_result = await self.validator_agent.validate_file(path)
        
        if validation_result.get("is_valid"):
            print("Validation passed")
        else:
            print("Validation failed")
            for issue in validation_result.get("issues", []):
                print(f"  - {issue.get('message')}")


def create_argument_parser():
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(description="AI-Enhanced Task Management System")
    parser.add_argument("--config", type=str, help="Configuration file path")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # PRD generation command
    prd_parser = subparsers.add_parser("generate-prd", help="Generate Product Requirements Document")
    prd_parser.add_argument("project_name", help="Project name")
    prd_parser.add_argument("--description", help="Project description")
    prd_parser.add_argument("--output", help="Output file path")
    
    # Code analysis command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze code")
    analyze_parser.add_argument("file", help="File to analyze")
    analyze_parser.add_argument("--output", help="Output file for analysis results")
    
    # Implementation planning command
    plan_parser = subparsers.add_parser("plan", help="Create implementation plan")
    plan_parser.add_argument("requirements", help="Comma-separated requirements")
    plan_parser.add_argument("--output", help="Output file for plan")
    
    # Code modification command
    modify_parser = subparsers.add_parser("modify", help="Modify code")
    modify_parser.add_argument("file", help="File to modify")
    modify_parser.add_argument("description", help="Modification description")
    
    # Validation command
    validate_parser = subparsers.add_parser("validate", help="Validate changes")
    validate_parser.add_argument("file", help="File to validate")
    
    return parser


async def main():
    """Main application entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Initialize application
    config_path = Path(args.config) if args.config else None
    app = AITaskManagementApp(config_path)
    
    try:
        if args.interactive or not args.command:
            # Run in interactive mode
            await app.run_interactive_mode()
        else:
            # Run in CLI mode
            await app.run_cli_mode(args)
            
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Run the application
    asyncio.run(main())