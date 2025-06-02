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
            You are an expert Product Manager who creates comprehensive Product Requirements Documents (PRDs).
            
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
            
            Format with clear headings, bullet points, and actionable details.
            Include realistic timelines, specific metrics, and technical considerations.
            """
        )

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
        """Interactive command-line mode for PRD generation"""
        print("=== PRD Generator ===")
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
        
        # Ask if user wants to save
        save_choice = input("\nSave PRD to file? (y/n): ").strip().lower()
        if save_choice == 'y':
            filename = input("Enter filename (or press Enter for auto-generated): ").strip()
            result = self.save_prd(prd, filename if filename else None)
            print(result)

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
    """Simple demo of PRD generation"""
    generator = PRDGenerator()
    
    # Quick example - you can modify this or use interactive_mode()
    product_idea = "AI-powered code review tool that integrates with GitHub"
    
    print("Generating PRD for:", product_idea)
    prd = generator.generate_prd(
        product_idea,
        target_audience="Software developers and engineering teams",
        business_goals="Improve code quality and reduce review time by 50%"
    )
    
    print("\n" + "="*60)
    print(prd)
    print("="*60)
    
    # Uncomment for interactive mode:
    # generator.interactive_mode()

if __name__ == "__main__":
    main()