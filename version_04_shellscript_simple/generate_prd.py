#!/usr/bin/env python3
"""
PRD Generator using Agno Agent Framework and Gemini API
Inspired by the blog post generator demo with multi-agent workflow
"""

import json
import os
from textwrap import dedent
from typing import Dict, Iterator, Optional
from pathlib import Path

from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from agno.utils.log import logger
from agno.utils.pprint import pprint_run_response
from agno.workflow import RunEvent, RunResponse, Workflow
from pydantic import BaseModel, Field

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv is optional, continue without it
    pass


class ProjectAnalysis(BaseModel):
    """Structured analysis of project information"""
    project_name: str = Field(..., description="Inferred project name")
    project_type: str = Field(..., description="Type of project (web app, CLI tool, library, etc.)")
    core_functionality: list[str] = Field(..., description="List of core functionalities")
    technical_stack: list[str] = Field(..., description="Technologies and languages used")
    file_structure_summary: str = Field(..., description="Summary of project structure")
    complexity_assessment: str = Field(..., description="Assessment of project complexity")
    user_personas: list[str] = Field(..., description="Identified user types")
    key_features: list[str] = Field(..., description="Main features extracted from code")


class PRDRequirements(BaseModel):
    """Structured PRD requirements"""
    functional_requirements: list[str] = Field(..., description="Functional requirements")
    non_functional_requirements: list[str] = Field(..., description="Non-functional requirements")
    user_stories: list[str] = Field(..., description="User stories in standard format")
    acceptance_criteria: list[str] = Field(..., description="Acceptance criteria")
    technical_constraints: list[str] = Field(..., description="Technical constraints")
    success_metrics: list[str] = Field(..., description="Success metrics and KPIs")


class PRDGenerator(Workflow):
    """Advanced workflow for generating Product Requirements Documents using Agno agent methodology."""

    description: str = dedent("""\
    An intelligent PRD generator that creates comprehensive Product Requirements Documents
    by analyzing project codebases and structure. This workflow orchestrates multiple AI agents
    to analyze, extract requirements, and craft professional PRDs that bridge technical
    implementation with business objectives.
    """)

    # Get model configuration from environment
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

    # Project Analyzer Agent: Analyzes codebase and extracts insights
    project_analyzer: Agent = Agent(
        model=Gemini(id=model_name),
        description=dedent("""\
        You are ProjectAnalyst-X, an elite code analysis specialist with expertise in:
        
        - Analyzing codebases to extract product insights
        - Identifying core functionality from technical implementation
        - Understanding user workflows from code structure
        - Assessing technical complexity and architecture
        - Inferring business logic from code patterns
        """),
        instructions=dedent("""\
        1. Code Analysis 🔍
           - Analyze the project structure and file organization
           - Identify main entry points and core modules
           - Extract functionality from code patterns
           - Assess technical complexity and dependencies
        
        2. Product Insights 💡
           - Infer the project's purpose and target users
           - Identify key features from implementation
           - Understand data flows and user interactions
           - Extract business logic and rules
        
        3. Technical Assessment 🔧
           - Evaluate the technology stack and architecture
           - Identify integration points and dependencies
           - Assess scalability and performance considerations
           - Note security and compliance aspects
        """),
        response_model=ProjectAnalysis,
    )

    # Requirements Engineer Agent: Extracts and structures requirements
    requirements_engineer: Agent = Agent(
        model=Gemini(id=model_name),
        description=dedent("""\
        You are RequirementsEngineer-X, a specialist in translating technical implementations
        into structured business requirements. Your expertise includes:
        
        - Converting code functionality into user requirements
        - Creating comprehensive user stories and acceptance criteria
        - Identifying functional and non-functional requirements
        - Defining success metrics and KPIs
        - Structuring requirements for development teams
        """),
        instructions=dedent("""\
        1. Requirements Extraction 📋
           - Convert technical features into business requirements
           - Create detailed user stories with clear value propositions
           - Define acceptance criteria for each feature
           - Identify edge cases and error scenarios
        
        2. Requirement Categorization 📊
           - Separate functional from non-functional requirements
           - Prioritize requirements by business value
           - Identify dependencies between requirements
           - Note technical constraints and limitations
        
        3. Success Definition 🎯
           - Define measurable success criteria
           - Create KPIs for feature adoption and usage
           - Establish performance benchmarks
           - Set quality and reliability standards
        """),
        response_model=PRDRequirements,
    )

    # PRD Writer Agent: Crafts comprehensive PRD documents
    prd_writer: Agent = Agent(
        model=Gemini(id=model_name),
        description=dedent("""\
        You are PRDMaster-X, an elite Product Requirements Document specialist combining
        technical expertise with strategic product vision. Your strengths include:
        
        - Crafting comprehensive, actionable PRDs
        - Balancing technical detail with business clarity
        - Creating documents that serve both technical and business stakeholders
        - Structuring information for maximum usability
        - Incorporating industry best practices and standards
        """),
        instructions=dedent("""\
        1. Document Structure 📝
           - Create a professional, comprehensive PRD
           - Use clear headings and logical organization
           - Balance technical detail with business context
           - Include executive summary for stakeholders
        
        2. Content Excellence ✍️
           - Write clear, actionable requirements
           - Use consistent terminology throughout
           - Include relevant examples and use cases
           - Provide sufficient detail for implementation
        
        3. Stakeholder Focus 👥
           - Address needs of both technical and business teams
           - Include implementation guidance for developers
           - Provide business context for product managers
           - Create actionable next steps
        
        4. Professional Standards 🏆
           - Follow industry PRD best practices
           - Include all essential PRD sections
           - Use professional formatting and language
           - Ensure document completeness and accuracy
        """),
        expected_output=dedent("""\
        # Product Requirements Document: {Product Name}

        ## Executive Summary
        {Brief overview and value proposition}

        ## Product Overview
        ### Vision & Mission
        {Product vision and mission}
        
        ### Target Users
        {User personas and target audience}
        
        ### Key Value Propositions
        {Main benefits and competitive advantages}

        ## Functional Requirements
        ### Core Features
        {Detailed feature specifications}
        
        ### User Stories
        {User stories in standard format}
        
        ### Acceptance Criteria
        {Specific acceptance criteria}

        ## Technical Requirements
        ### Architecture Overview
        {Technical architecture summary}
        
        ### Performance Requirements
        {Performance, scalability, reliability}
        
        ### Security Requirements
        {Security and compliance needs}

        ## Implementation Plan
        ### Development Phases
        {Phased development approach}
        
        ### Timeline & Milestones
        {Key dates and deliverables}

        ## Success Metrics
        ### Key Performance Indicators
        {Measurable success criteria}
        
        ### User Acceptance Criteria
        {User-focused success measures}

        ## Risk Assessment
        ### Technical Risks
        {Technical challenges and mitigation}
        
        ### Business Risks
        {Business risks and contingencies}

        ## Appendices
        ### Technical Specifications
        {Detailed technical documentation}
        """),
        markdown=True,
    )

    def run(
        self,
        project_info_file: str = "project_info.txt",
        use_cache: bool = True,
    ) -> Iterator[RunResponse]:
        """Generate PRD from project information file"""
        
        logger.info(f"Generating PRD from: {project_info_file}")

        # Check if cached PRD exists
        if use_cache:
            cached_prd = self.get_cached_prd(project_info_file)
            if cached_prd:
                yield RunResponse(
                    content=cached_prd, 
                    event=RunEvent.workflow_completed
                )
                return

        # Read project information
        project_info = self.read_project_info(project_info_file)
        if not project_info:
            yield RunResponse(
                event=RunEvent.workflow_completed,
                content=f"Error: Could not read project information from {project_info_file}",
            )
            return

        # Step 1: Analyze project
        logger.info("🔍 Analyzing project structure and code...")
        project_analysis = self.analyze_project(project_info, use_cache)
        if not project_analysis:
            yield RunResponse(
                event=RunEvent.workflow_completed,
                content="Error: Failed to analyze project",
            )
            return

        # Step 2: Extract requirements
        logger.info("📋 Extracting and structuring requirements...")
        requirements = self.extract_requirements(project_analysis, use_cache)
        if not requirements:
            yield RunResponse(
                event=RunEvent.workflow_completed,
                content="Error: Failed to extract requirements",
            )
            return

        # Step 3: Generate PRD
        logger.info("📝 Generating comprehensive PRD...")
        prd_input = {
            "project_analysis": project_analysis.model_dump(),
            "requirements": requirements.model_dump(),
            "original_project_info": project_info[:2000] + "..." if len(project_info) > 2000 else project_info
        }

        # Run the PRD writer and yield the response
        yield from self.prd_writer.run(
            json.dumps(prd_input, indent=2), 
            stream=True
        )

        # Cache the generated PRD
        if self.prd_writer.run_response and self.prd_writer.run_response.content:
            self.cache_prd(project_info_file, self.prd_writer.run_response.content)

    def read_project_info(self, file_path: str) -> Optional[str]:
        """Read project information from file"""
        try:
            if not os.path.exists(file_path):
                logger.error(f"Project info file not found: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            if not content:
                logger.error(f"Project info file is empty: {file_path}")
                return None
                
            logger.info(f"Successfully read {len(content)} characters from {file_path}")
            return content
            
        except Exception as e:
            logger.error(f"Error reading project info file: {e}")
            return None

    def analyze_project(self, project_info: str, use_cache: bool) -> Optional[ProjectAnalysis]:
        """Analyze project using the project analyzer agent"""
        cache_key = f"analysis_{hash(project_info)}"
        
        if use_cache:
            cached_analysis = self.session_state.get("project_analyses", {}).get(cache_key)
            if cached_analysis:
                logger.info("Using cached project analysis")
                return ProjectAnalysis.model_validate(cached_analysis)

        try:
            response: RunResponse = self.project_analyzer.run(project_info)
            if response and response.content and isinstance(response.content, ProjectAnalysis):
                # Cache the analysis
                self.session_state.setdefault("project_analyses", {})
                self.session_state["project_analyses"][cache_key] = response.content.model_dump()
                return response.content
            else:
                logger.error("Invalid response from project analyzer")
                return None
        except Exception as e:
            logger.error(f"Error in project analysis: {e}")
            return None

    def extract_requirements(self, project_analysis: ProjectAnalysis, use_cache: bool) -> Optional[PRDRequirements]:
        """Extract requirements using the requirements engineer agent"""
        analysis_str = json.dumps(project_analysis.model_dump(), indent=2)
        cache_key = f"requirements_{hash(analysis_str)}"
        
        if use_cache:
            cached_requirements = self.session_state.get("requirements", {}).get(cache_key)
            if cached_requirements:
                logger.info("Using cached requirements")
                return PRDRequirements.model_validate(cached_requirements)

        try:
            response: RunResponse = self.requirements_engineer.run(analysis_str)
            if response and response.content and isinstance(response.content, PRDRequirements):
                # Cache the requirements
                self.session_state.setdefault("requirements", {})
                self.session_state["requirements"][cache_key] = response.content.model_dump()
                return response.content
            else:
                logger.error("Invalid response from requirements engineer")
                return None
        except Exception as e:
            logger.error(f"Error in requirements extraction: {e}")
            return None

    def get_cached_prd(self, project_info_file: str) -> Optional[str]:
        """Get cached PRD if available"""
        return self.session_state.get("generated_prds", {}).get(project_info_file)

    def cache_prd(self, project_info_file: str, prd_content: str):
        """Cache the generated PRD"""
        self.session_state.setdefault("generated_prds", {})
        self.session_state["generated_prds"][project_info_file] = prd_content


def main():
    """Main function to run the PRD generator"""
    import argparse
    from rich.console import Console
    from rich.prompt import Prompt
    
    console = Console()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate PRD using Agno Agent Framework")
    parser.add_argument(
        "-i", "--input", 
        default="project_info.txt",
        help="Input project information file (default: project_info.txt)"
    )
    parser.add_argument(
        "-o", "--output",
        default="prd_output.md",
        help="Output PRD file (default: prd_output.md)"
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input):
        console.print(f"❌ Error: Input file '{args.input}' not found", style="red")
        console.print("💡 Tip: Run the project_info.sh script first to generate project information")
        return 1
    
    # Check for API key
    if not os.getenv("GOOGLE_API_KEY") and not os.getenv("GEMINI_API_KEY"):
        console.print("❌ Error: Google API key not found", style="red")
        console.print("Please set your API key:")
        console.print("  export GOOGLE_API_KEY='your_api_key_here'")
        console.print("  or")
        console.print("  export GEMINI_API_KEY='your_api_key_here'")
        return 1
    
    console.print("🚀 PRD Generator - Powered by Agno Agent Framework", style="bold blue")
    console.print("=" * 60)
    
    # Create URL-safe session ID
    input_name = Path(args.input).stem
    session_id = f"prd-generator-{input_name}"
    
    # Initialize the PRD generator workflow
    prd_generator = PRDGenerator(
        session_id=session_id,
        storage=SqliteStorage(
            table_name="prd_generator_workflows",
            db_file="tmp/agno_workflows.db",
        ),
        debug_mode=args.debug,
    )
    
    try:
        # Generate PRD
        console.print(f"📁 Reading project information from: {args.input}")
        
        prd_responses: Iterator[RunResponse] = prd_generator.run(
            project_info_file=args.input,
            use_cache=not args.no_cache,
        )
        
        # Collect the generated content
        generated_content = ""
        for response in prd_responses:
            if response.content:
                generated_content += str(response.content)
        
        if generated_content:
            # Save to output file
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(f"# Product Requirements Document\n")
                f.write(f"Generated on: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Source: {args.input}\n\n")
                f.write(generated_content)
            
            console.print(f"✅ PRD generated successfully!", style="green")
            console.print(f"📄 Output saved to: {args.output}")
            
            # Display statistics
            word_count = len(generated_content.split())
            char_count = len(generated_content)
            console.print(f"📊 Word count: {word_count:,} words")
            console.print(f"📏 Character count: {char_count:,} characters")
            
            console.print("\n🎉 PRD generation completed successfully!", style="bold green")
            console.print("💡 Next steps:")
            console.print(f"   - Review the generated PRD in {args.output}")
            console.print("   - Customize sections as needed for your specific requirements")
            console.print("   - Share with stakeholders for feedback and approval")
            
        else:
            console.print("❌ No content was generated", style="red")
            return 1
            
    except Exception as e:
        console.print(f"❌ Error generating PRD: {e}", style="red")
        if args.debug:
            import traceback
            console.print(traceback.format_exc())
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())