"""
Product Requirements Document (PRD) template generator.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from ..utils.file_utils import FileUtils


class PRDSection(Enum):
    """PRD document sections."""
    OVERVIEW = "overview"
    OBJECTIVES = "objectives"
    REQUIREMENTS = "requirements"
    USER_STORIES = "user_stories"
    ACCEPTANCE_CRITERIA = "acceptance_criteria"
    TECHNICAL_SPECS = "technical_specs"
    TIMELINE = "timeline"
    RISKS = "risks"
    SUCCESS_METRICS = "success_metrics"


@dataclass
class Requirement:
    """Individual requirement specification."""
    id: str
    title: str
    description: str
    priority: str  # High, Medium, Low
    category: str  # Functional, Non-functional, Technical
    acceptance_criteria: List[str]
    dependencies: List[str]
    effort_estimate: Optional[str] = None


@dataclass
class UserStory:
    """User story specification."""
    id: str
    title: str
    description: str
    persona: str
    acceptance_criteria: List[str]
    priority: str
    story_points: Optional[int] = None


@dataclass
class TechnicalSpec:
    """Technical specification."""
    component: str
    description: str
    technologies: List[str]
    interfaces: List[str]
    dependencies: List[str]
    performance_requirements: Optional[str] = None


class PRDTemplate:
    """Generate comprehensive Product Requirements Documents."""
    
    def __init__(self):
        """Initialize the PRD template generator."""
        self.template_version = "1.0"
        self.default_sections = [
            PRDSection.OVERVIEW,
            PRDSection.OBJECTIVES,
            PRDSection.REQUIREMENTS,
            PRDSection.USER_STORIES,
            PRDSection.ACCEPTANCE_CRITERIA,
            PRDSection.TECHNICAL_SPECS,
            PRDSection.TIMELINE,
            PRDSection.RISKS,
            PRDSection.SUCCESS_METRICS
        ]
    
    def generate_prd(self, project_info: Dict[str, Any], 
                    sections: Optional[List[PRDSection]] = None) -> str:
        """Generate a complete PRD document."""
        if sections is None:
            sections = self.default_sections
        
        prd_content = []
        
        # Document header
        prd_content.append(self._generate_header(project_info))
        prd_content.append("")
        
        # Table of contents
        prd_content.append(self._generate_toc(sections))
        prd_content.append("")
        
        # Generate each section
        for section in sections:
            section_content = self._generate_section(section, project_info)
            if section_content:
                prd_content.append(section_content)
                prd_content.append("")
        
        # Document footer
        prd_content.append(self._generate_footer())
        
        return '\n'.join(prd_content)
    
    def _generate_header(self, project_info: Dict[str, Any]) -> str:
        """Generate document header."""
        title = project_info.get('title', 'Project Requirements Document')
        version = project_info.get('version', '1.0')
        author = project_info.get('author', 'AI Assistant')
        date = datetime.now().strftime('%Y-%m-%d')
        
        header = f"""# {title}

**Version:** {version}  
**Author:** {author}  
**Date:** {date}  
**Status:** Draft

---"""
        
        return header
    
    def _generate_toc(self, sections: List[PRDSection]) -> str:
        """Generate table of contents."""
        toc_lines = ["## Table of Contents", ""]
        
        section_titles = {
            PRDSection.OVERVIEW: "1. Project Overview",
            PRDSection.OBJECTIVES: "2. Objectives and Goals",
            PRDSection.REQUIREMENTS: "3. Requirements",
            PRDSection.USER_STORIES: "4. User Stories",
            PRDSection.ACCEPTANCE_CRITERIA: "5. Acceptance Criteria",
            PRDSection.TECHNICAL_SPECS: "6. Technical Specifications",
            PRDSection.TIMELINE: "7. Timeline and Milestones",
            PRDSection.RISKS: "8. Risks and Mitigation",
            PRDSection.SUCCESS_METRICS: "9. Success Metrics"
        }
        
        for section in sections:
            if section in section_titles:
                toc_lines.append(f"- {section_titles[section]}")
        
        return '\n'.join(toc_lines)
    
    def _generate_section(self, section: PRDSection, project_info: Dict[str, Any]) -> str:
        """Generate a specific section of the PRD."""
        if section == PRDSection.OVERVIEW:
            return self._generate_overview(project_info)
        elif section == PRDSection.OBJECTIVES:
            return self._generate_objectives(project_info)
        elif section == PRDSection.REQUIREMENTS:
            return self._generate_requirements(project_info)
        elif section == PRDSection.USER_STORIES:
            return self._generate_user_stories(project_info)
        elif section == PRDSection.ACCEPTANCE_CRITERIA:
            return self._generate_acceptance_criteria(project_info)
        elif section == PRDSection.TECHNICAL_SPECS:
            return self._generate_technical_specs(project_info)
        elif section == PRDSection.TIMELINE:
            return self._generate_timeline(project_info)
        elif section == PRDSection.RISKS:
            return self._generate_risks(project_info)
        elif section == PRDSection.SUCCESS_METRICS:
            return self._generate_success_metrics(project_info)
        
        return ""
    
    def _generate_overview(self, project_info: Dict[str, Any]) -> str:
        """Generate project overview section."""
        overview = project_info.get('overview', '')
        problem_statement = project_info.get('problem_statement', '')
        solution_summary = project_info.get('solution_summary', '')
        target_audience = project_info.get('target_audience', '')
        
        content = [
            "## 1. Project Overview",
            "",
            "### 1.1 Problem Statement",
            problem_statement or "Define the problem this project aims to solve.",
            "",
            "### 1.2 Solution Summary",
            solution_summary or "Provide a high-level description of the proposed solution.",
            "",
            "### 1.3 Target Audience",
            target_audience or "Identify the primary users and stakeholders.",
            "",
            "### 1.4 Project Scope",
            overview or "Define what is included and excluded from this project scope."
        ]
        
        return '\n'.join(content)
    
    def _generate_objectives(self, project_info: Dict[str, Any]) -> str:
        """Generate objectives and goals section."""
        objectives = project_info.get('objectives', [])
        business_goals = project_info.get('business_goals', [])
        success_criteria = project_info.get('success_criteria', [])
        
        content = [
            "## 2. Objectives and Goals",
            "",
            "### 2.1 Primary Objectives"
        ]
        
        if objectives:
            for i, objective in enumerate(objectives, 1):
                content.append(f"{i}. {objective}")
        else:
            content.extend([
                "1. Define primary objective 1",
                "2. Define primary objective 2",
                "3. Define primary objective 3"
            ])
        
        content.extend([
            "",
            "### 2.2 Business Goals"
        ])
        
        if business_goals:
            for goal in business_goals:
                content.append(f"- {goal}")
        else:
            content.extend([
                "- Improve user experience",
                "- Increase operational efficiency",
                "- Reduce development time"
            ])
        
        content.extend([
            "",
            "### 2.3 Success Criteria"
        ])
        
        if success_criteria:
            for criteria in success_criteria:
                content.append(f"- {criteria}")
        else:
            content.extend([
                "- Define measurable success criteria",
                "- Set performance benchmarks",
                "- Establish quality metrics"
            ])
        
        return '\n'.join(content)
    
    def _generate_requirements(self, project_info: Dict[str, Any]) -> str:
        """Generate requirements section."""
        requirements = project_info.get('requirements', [])
        
        content = [
            "## 3. Requirements",
            "",
            "### 3.1 Functional Requirements"
        ]
        
        functional_reqs = [req for req in requirements if isinstance(req, dict) and req.get('category') == 'Functional']
        
        if functional_reqs:
            for req in functional_reqs:
                content.extend([
                    f"**{req.get('id', 'REQ-F-001')}**: {req.get('title', 'Requirement Title')}",
                    f"- **Description**: {req.get('description', 'Requirement description')}",
                    f"- **Priority**: {req.get('priority', 'Medium')}",
                    ""
                ])
        else:
            content.extend([
                "**REQ-F-001**: Core Functionality",
                "- **Description**: Define core functional requirements",
                "- **Priority**: High",
                "",
                "**REQ-F-002**: User Interface",
                "- **Description**: Define user interface requirements",
                "- **Priority**: High",
                ""
            ])
        
        content.extend([
            "### 3.2 Non-Functional Requirements"
        ])
        
        non_functional_reqs = [req for req in requirements if isinstance(req, dict) and req.get('category') == 'Non-functional']
        
        if non_functional_reqs:
            for req in non_functional_reqs:
                content.extend([
                    f"**{req.get('id', 'REQ-NF-001')}**: {req.get('title', 'Requirement Title')}",
                    f"- **Description**: {req.get('description', 'Requirement description')}",
                    f"- **Priority**: {req.get('priority', 'Medium')}",
                    ""
                ])
        else:
            content.extend([
                "**REQ-NF-001**: Performance",
                "- **Description**: System should respond within 2 seconds",
                "- **Priority**: High",
                "",
                "**REQ-NF-002**: Scalability",
                "- **Description**: System should handle 1000 concurrent users",
                "- **Priority**: Medium",
                ""
            ])
        
        return '\n'.join(content)
    
    def _generate_user_stories(self, project_info: Dict[str, Any]) -> str:
        """Generate user stories section."""
        user_stories = project_info.get('user_stories', [])
        
        content = [
            "## 4. User Stories",
            "",
            "### 4.1 Primary User Stories"
        ]
        
        if user_stories:
            for story in user_stories:
                if isinstance(story, dict):
                    content.extend([
                        f"**{story.get('id', 'US-001')}**: {story.get('title', 'User Story Title')}",
                        f"As a {story.get('persona', 'user')}, I want {story.get('description', 'to perform an action')} so that I can achieve a goal.",
                        "",
                        "**Acceptance Criteria:**"
                    ])
                    
                    criteria = story.get('acceptance_criteria', [])
                    if criteria:
                        for criterion in criteria:
                            content.append(f"- {criterion}")
                    else:
                        content.append("- Define acceptance criteria")
                    
                    content.extend([
                        f"**Priority**: {story.get('priority', 'Medium')}",
                        f"**Story Points**: {story.get('story_points', 'TBD')}",
                        ""
                    ])
        else:
            content.extend([
                "**US-001**: Basic User Interaction",
                "As a user, I want to interact with the system so that I can accomplish my tasks efficiently.",
                "",
                "**Acceptance Criteria:**",
                "- User can access the main interface",
                "- User can perform basic operations",
                "- System provides appropriate feedback",
                "",
                "**Priority**: High",
                "**Story Points**: 5",
                ""
            ])
        
        return '\n'.join(content)
    
    def _generate_acceptance_criteria(self, project_info: Dict[str, Any]) -> str:
        """Generate acceptance criteria section."""
        content = [
            "## 5. Acceptance Criteria",
            "",
            "### 5.1 Definition of Done",
            "- All functional requirements are implemented",
            "- All tests pass (unit, integration, acceptance)",
            "- Code review is completed",
            "- Documentation is updated",
            "- Performance requirements are met",
            "",
            "### 5.2 Quality Gates",
            "- Code coverage >= 80%",
            "- No critical security vulnerabilities",
            "- Performance benchmarks met",
            "- User acceptance testing passed",
            ""
        ]
        
        return '\n'.join(content)
    
    def _generate_technical_specs(self, project_info: Dict[str, Any]) -> str:
        """Generate technical specifications section."""
        tech_specs = project_info.get('technical_specs', [])
        architecture = project_info.get('architecture', '')
        technologies = project_info.get('technologies', [])
        
        content = [
            "## 6. Technical Specifications",
            "",
            "### 6.1 Architecture Overview",
            architecture or "Define the high-level system architecture.",
            "",
            "### 6.2 Technology Stack"
        ]
        
        if technologies:
            for tech in technologies:
                content.append(f"- {tech}")
        else:
            content.extend([
                "- Programming Language: Python 3.9+",
                "- Framework: FastAPI/Flask",
                "- Database: PostgreSQL",
                "- Frontend: React/Vue.js",
                "- Deployment: Docker/Kubernetes"
            ])
        
        content.extend([
            "",
            "### 6.3 Component Specifications"
        ])
        
        if tech_specs:
            for spec in tech_specs:
                if isinstance(spec, dict):
                    content.extend([
                        f"**{spec.get('component', 'Component Name')}**",
                        f"- **Description**: {spec.get('description', 'Component description')}",
                        f"- **Technologies**: {', '.join(spec.get('technologies', []))}",
                        f"- **Interfaces**: {', '.join(spec.get('interfaces', []))}",
                        ""
                    ])
        else:
            content.extend([
                "**API Layer**",
                "- **Description**: RESTful API for client communication",
                "- **Technologies**: FastAPI, Pydantic",
                "- **Interfaces**: HTTP/HTTPS, JSON",
                "",
                "**Business Logic Layer**",
                "- **Description**: Core application logic and processing",
                "- **Technologies**: Python, SQLAlchemy",
                "- **Interfaces**: Internal function calls",
                ""
            ])
        
        return '\n'.join(content)
    
    def _generate_timeline(self, project_info: Dict[str, Any]) -> str:
        """Generate timeline and milestones section."""
        milestones = project_info.get('milestones', [])
        
        content = [
            "## 7. Timeline and Milestones",
            "",
            "### 7.1 Project Phases"
        ]
        
        if milestones:
            for milestone in milestones:
                if isinstance(milestone, dict):
                    content.extend([
                        f"**{milestone.get('name', 'Milestone')}** - {milestone.get('date', 'TBD')}",
                        f"- {milestone.get('description', 'Milestone description')}",
                        ""
                    ])
        else:
            content.extend([
                "**Phase 1: Planning and Design** - Week 1-2",
                "- Requirements gathering",
                "- System design",
                "- Technical architecture",
                "",
                "**Phase 2: Development** - Week 3-8",
                "- Core functionality implementation",
                "- API development",
                "- Frontend development",
                "",
                "**Phase 3: Testing and Deployment** - Week 9-10",
                "- Testing and quality assurance",
                "- Performance optimization",
                "- Production deployment",
                ""
            ])
        
        return '\n'.join(content)
    
    def _generate_risks(self, project_info: Dict[str, Any]) -> str:
        """Generate risks and mitigation section."""
        risks = project_info.get('risks', [])
        
        content = [
            "## 8. Risks and Mitigation",
            "",
            "### 8.1 Identified Risks"
        ]
        
        if risks:
            for risk in risks:
                if isinstance(risk, dict):
                    content.extend([
                        f"**{risk.get('title', 'Risk Title')}**",
                        f"- **Probability**: {risk.get('probability', 'Medium')}",
                        f"- **Impact**: {risk.get('impact', 'Medium')}",
                        f"- **Mitigation**: {risk.get('mitigation', 'Define mitigation strategy')}",
                        ""
                    ])
        else:
            content.extend([
                "**Technical Complexity**",
                "- **Probability**: Medium",
                "- **Impact**: High",
                "- **Mitigation**: Conduct proof of concept, allocate extra time for complex features",
                "",
                "**Resource Availability**",
                "- **Probability**: Low",
                "- **Impact**: High",
                "- **Mitigation**: Cross-train team members, maintain resource buffer",
                "",
                "**Scope Creep**",
                "- **Probability**: Medium",
                "- **Impact**: Medium",
                "- **Mitigation**: Clear requirements documentation, change control process",
                ""
            ])
        
        return '\n'.join(content)
    
    def _generate_success_metrics(self, project_info: Dict[str, Any]) -> str:
        """Generate success metrics section."""
        metrics = project_info.get('success_metrics', [])
        
        content = [
            "## 9. Success Metrics",
            "",
            "### 9.1 Key Performance Indicators (KPIs)"
        ]
        
        if metrics:
            for metric in metrics:
                if isinstance(metric, dict):
                    content.extend([
                        f"**{metric.get('name', 'Metric Name')}**",
                        f"- **Description**: {metric.get('description', 'Metric description')}",
                        f"- **Target**: {metric.get('target', 'Define target value')}",
                        f"- **Measurement**: {metric.get('measurement', 'How to measure')}",
                        ""
                    ])
        else:
            content.extend([
                "**User Adoption Rate**",
                "- **Description**: Percentage of target users actively using the system",
                "- **Target**: 80% adoption within 3 months",
                "- **Measurement**: Monthly active users / Total target users",
                "",
                "**System Performance**",
                "- **Description**: Average response time for user requests",
                "- **Target**: < 2 seconds for 95% of requests",
                "- **Measurement**: Application performance monitoring",
                "",
                "**User Satisfaction**",
                "- **Description**: User satisfaction score from surveys",
                "- **Target**: Average score >= 4.0/5.0",
                "- **Measurement**: Quarterly user satisfaction surveys",
                ""
            ])
        
        return '\n'.join(content)
    
    def _generate_footer(self) -> str:
        """Generate document footer."""
        footer = f"""---

**Document Information:**
- Template Version: {self.template_version}
- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Generator: AI-Enhanced Task Management System

**Revision History:**
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | {datetime.now().strftime('%Y-%m-%d')} | AI Assistant | Initial version |

---

*This document was generated using the AI-Enhanced Task Management System PRD Template.*"""
        
        return footer
    
    def generate_requirements_matrix(self, requirements: List[Requirement]) -> str:
        """Generate a requirements traceability matrix."""
        if not requirements:
            return ""
        
        content = [
            "## Requirements Traceability Matrix",
            "",
            "| ID | Title | Priority | Category | Dependencies | Status |",
            "|----|----|----------|----------|--------------|--------|"
        ]
        
        for req in requirements:
            deps = ", ".join(req.dependencies) if req.dependencies else "None"
            content.append(f"| {req.id} | {req.title} | {req.priority} | {req.category} | {deps} | Draft |")
        
        return '\n'.join(content)
    
    def generate_user_story_map(self, user_stories: List[UserStory]) -> str:
        """Generate a user story mapping visualization."""
        if not user_stories:
            return ""
        
        # Group stories by persona
        personas = {}
        for story in user_stories:
            if story.persona not in personas:
                personas[story.persona] = []
            personas[story.persona].append(story)
        
        content = [
            "## User Story Map",
            ""
        ]
        
        for persona, stories in personas.items():
            content.extend([
                f"### {persona}",
                ""
            ])
            
            for story in stories:
                content.extend([
                    f"**{story.id}**: {story.title}",
                    f"- Priority: {story.priority}",
                    f"- Story Points: {story.story_points or 'TBD'}",
                    f"- Description: {story.description}",
                    ""
                ])
        
        return '\n'.join(content)