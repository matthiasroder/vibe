#!/usr/bin/env python3
"""
Vibe Template Workflow - Markdown Generator

This script generates the markdown files for the vibe coding workflow:
1. Takes product description and tools list as input
2. Generates architecture.md using an LLM
3. Creates tasks.md based on the architecture
4. Updates agents.md with project-specific information
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional

# You'll need to install: pip install openai anthropic
# Uncomment and configure based on your LLM choice
# import openai
# from anthropic import Anthropic

class VibeWorkflow:
    def __init__(self, product_file: str, tools_file: str, output_dir: str = "."):
        self.product_file = Path(product_file)
        self.tools_file = Path(tools_file)
        self.output_dir = Path(output_dir)
        
        # Read input files
        self.product_description = self._read_file(self.product_file)
        self.tools_list = self._read_file(self.tools_file)
        
        # Ensure output directory exists
        if self.output_dir != Path("."):
            self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _read_file(self, filepath: Path) -> str:
        """Read content from a file."""
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        return filepath.read_text().strip()
    
    def _save_file(self, filename: str, content: str) -> None:
        """Save content to a file in the output directory."""
        filepath = self.output_dir / filename
        filepath.write_text(content)
        print(f"Created: {filepath}")
    
    def generate_architecture_prompt(self) -> str:
        """Generate the prompt for creating architecture.md."""
        return f"""I'm building a {self.product_description}. Use {self.tools_list}. Give me the full architecture:
   - File + folder structure
   - What each part does
   - Where state lives, how services connect.
Format this entire document in markdown.
Do not use icons or emoticons."""
    
    def generate_tasks_prompt(self, architecture: str) -> str:
        """Generate the prompt for creating tasks.md."""
        return f"""Using this architecture:

{architecture}

Write a granular step-by-step plan to build the MVP. Each task should:
   - Be incredibly small + testable
   - Have a clear start + end
   - Focus on one concern
I'll be passing this off to an engineering LLM that will be told to complete one task at a time, allowing me to test in between. Do not use icons or emoticons."""
    
    def call_llm(self, prompt: str, model: str = "gpt-4") -> str:
        """
        Call the LLM API with the given prompt.
        
        This is a placeholder - implement based on your LLM choice.
        Options:
        1. OpenAI API (GPT-4, GPT-3.5)
        2. Anthropic API (Claude)
        3. Local LLM via Ollama
        4. Other LLM providers
        """
        # Example implementation for OpenAI:
        # openai.api_key = os.getenv("OPENAI_API_KEY")
        # response = openai.ChatCompletion.create(
        #     model=model,
        #     messages=[{"role": "user", "content": prompt}],
        #     temperature=0.7
        # )
        # return response.choices[0].message.content
        
        # For now, return a placeholder
        print(f"\n{'='*60}")
        print("LLM PROMPT:")
        print(f"{'='*60}")
        print(prompt)
        print(f"{'='*60}\n")
        
        return f"[LLM Response would go here for: {model}]"
    
    def get_existing_agents_md(self) -> str:
        """Get the existing agents.md content from the template."""
        agents_path = Path(__file__).parent / "agents.md"
        if agents_path.exists():
            return agents_path.read_text()
        else:
            # Fallback content if agents.md doesn't exist
            return """# AGENTS.md - Coding Agent Guidelines

## Build/Test Commands
- No package.json found - this is a template/documentation repository
- No specific build or test commands available
- Check for project-specific build files when implementing actual projects

## Engineering Principles
- Write the absolute minimum code required
- No sweeping changes
- No unrelated edits
- Focus on just the task you're on
- Make code precise, modular, testable
- Don't break existing functionality
- If I need to do anything (e.g. bash/python etc.), tell me clearly

## Code Style Guidelines
- Follow existing patterns in the codebase
- Use clear, descriptive naming conventions
- Keep functions small and focused on single concerns
- Prefer explicit over implicit code
- No comments unless absolutely necessary for complex logic
- Test each small change before moving to the next task

## Workflow
- Read architecture.md and tasks.md before starting
- Complete one task at a time from tasks.md
- Stop after each task for testing/validation
- Commit only when explicitly requested"""
    
    def run(self, use_llm: bool = False) -> None:
        """Execute the vibe workflow to generate markdown files."""
        print(f"Vibe Workflow - Generating Markdown Files")
        print(f"Product: {self.product_description[:50]}...")
        print(f"Tools: {self.tools_list[:50]}...")
        print(f"Output directory: {self.output_dir}\n")
        
        # Step 1: Generate architecture.md
        print("Step 1: Generating architecture.md...")
        arch_prompt = self.generate_architecture_prompt()
        if use_llm:
            architecture = self.call_llm(arch_prompt)
        else:
            architecture = f"# Architecture\n\n## Product Description\n{self.product_description}\n\n## Tools\n{self.tools_list}\n\n[LLM will generate architecture here based on the prompt below]\n\n---\n**Prompt for LLM:**\n```\n{arch_prompt}\n```"
        self._save_file("architecture.md", architecture)
        
        # Step 2: Generate tasks.md
        print("Step 2: Generating tasks.md...")
        tasks_prompt = self.generate_tasks_prompt(architecture)
        if use_llm:
            tasks = self.call_llm(tasks_prompt)
        else:
            tasks = f"# Tasks\n\n[LLM will generate tasks based on architecture.md]\n\n---\n**Prompt for LLM:**\n```\n{tasks_prompt}\n```"
        self._save_file("tasks.md", tasks)
        
        # Step 3: Copy/create agents.md
        print("Step 3: Creating agents.md...")
        agents = self.get_existing_agents_md()
        self._save_file("agents.md", agents)
        
        print(f"\n✅ Markdown files generated successfully!")
        print(f"\nFiles created in {self.output_dir}:")
        print("  - architecture.md")
        print("  - tasks.md") 
        print("  - agents.md")
        print("\nNext steps:")
        print("1. If not using --use-llm, manually run the prompts through your LLM")
        print("2. Review and refine the generated content")
        print("3. Use these files with your AI coding assistant")


def main():
    parser = argparse.ArgumentParser(
        description="Generate markdown files for the vibe coding workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python vibe_workflow.py product.txt tools.txt
  python vibe_workflow.py product.txt tools.txt --output ./docs
  python vibe_workflow.py product.txt tools.txt --use-llm
        """
    )
    
    parser.add_argument("product_file", help="File containing product description")
    parser.add_argument("tools_file", help="File containing list of tools")
    parser.add_argument("--output", "-o", default=".", help="Output directory (default: current directory)")
    parser.add_argument("--use-llm", action="store_true", help="Use LLM API to generate content (requires API setup)")
    
    args = parser.parse_args()
    
    try:
        workflow = VibeWorkflow(args.product_file, args.tools_file, args.output)
        workflow.run(use_llm=args.use_llm)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()