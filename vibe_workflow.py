#!/usr/bin/env python3
"""
Vibe Template Workflow - Markdown Generator

This script generates the markdown files for the vibe coding workflow:
1. Takes product description and tools list as input (from .md files)
2. Generates architecture.md using OpenAI
3. Creates tasks.md based on the architecture
4. Copies agents.md with project-specific information
5. Creates initial_prompt.md for the AI coding assistant

Usage: python vibe_workflow.py <output_dir> <PRODUCT.md> <tools.md>"""

import os
import sys
from pathlib import Path
from typing import Optional
import openai

class VibeWorkflow:
    def __init__(self, output_dir: str, product_file: str, tools_file: str):
        self.output_dir = Path(output_dir)
        self.product_file = Path(product_file)
        self.tools_file = Path(tools_file)

        # Set up OpenAI
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable not set")

        # Read input files
        self.product_description = self._read_file(self.product_file)
        self.tools_list = self._read_file(self.tools_file)

        # Ensure output directory exists
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

    def call_llm(self, prompt: str) -> str:
        """Call OpenAI API with the given prompt using gpt-4o-mini."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            sys.exit(1)

    def get_existing_agents_md(self) -> str:
        """Get the existing agents.md content from the template."""
        agents_path = Path(__file__).parent / "agents.md"
        return agents_path.read_text()

    def create_initial_prompt(self) -> str:
        """Create the initial prompt for the AI coding assistant."""
        return """You're an engineer building this codebase. You've been given architecture.md, tasks.md and agents.md. Read all three of them carefully. There should be no ambiguity about what we're building. Follow tasks.md and complete one task at a time. After each task, stop. I'll test it. If it works, commit to GitHub and move to the next task."""

    def run(self) -> None:
        """Execute the vibe workflow to generate markdown files."""
        print(f"Vibe Workflow - Generating Markdown Files")
        print(f"Product: {self.product_description[:50]}...")
        print(f"Tools: {self.tools_list[:50]}...")
        print(f"Output directory: {self.output_dir}\n")

        # Step 1: Generate architecture.md
        print("Step 1: Generating architecture.md...")
        arch_prompt = self.generate_architecture_prompt()
        architecture = self.call_llm(arch_prompt)
        self._save_file("architecture.md", architecture)

        # Step 2: Generate tasks.md
        print("Step 2: Generating tasks.md...")
        tasks_prompt = self.generate_tasks_prompt(architecture)
        tasks = self.call_llm(tasks_prompt)
        self._save_file("tasks.md", tasks)

        # Step 3: Copy/create agents.md
        print("Step 3: Creating agents.md...")
        agents = self.get_existing_agents_md()
        self._save_file("agents.md", agents)

        # Step 4: Create initial_prompt.md
        print("Step 4: Creating initial_prompt.md...")
        initial_prompt = self.create_initial_prompt()
        self._save_file("initial_prompt.md", initial_prompt)

        print(f"\n✅ Markdown files generated successfully!")
        print(f"\nFiles created in {self.output_dir}:")
        print("  - architecture.md")
        print("  - tasks.md")
        print("  - agents.md")
        print("  - initial_prompt.md")


def main():
    if len(sys.argv) != 4:
        print("Usage: python vibe_workflow.py <output_dir> <PRODUCT.md> <tools.md>")
        print("\nExample:")
        print("  python vibe_workflow.py ./my-project PRODUCT.md tools.md")
        sys.exit(1)

    output_dir = sys.argv[1]
    product_file = sys.argv[2]
    tools_file = sys.argv[3]

    try:
        workflow = VibeWorkflow(output_dir, product_file, tools_file)
        workflow.run()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
