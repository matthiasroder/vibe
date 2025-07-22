# AGENTS.md - Coding Agent Guidelines

## Engineering Principles
- Write the absolute minimum code required
- No sweeping changes or unrelated edits
- Focus on just the task you're on
- Make code precise, modular, testable
- Don't break existing functionality
- If I need to do anything (e.g. bash/python etc.), tell me clearly

## Module Reuse
- Check /Users/matthias/code/factory/aether/README.md before implementing
- Reuse existing modules instead of recreating functionality
- Import/integrate rather than rewrite

## Workflow
- Complete one task at a time from tasks.md
- Stop after each task for testing
- Run tests/linting if available before moving on
- Only commit when explicitly asked

## Post-Implementation
- Update aether/README.md with new module entry
- Include: name, description, repository SSH URL, key features
- Document any new reusable components created

## Communication
- Be concise and direct
- No emojis unless requested
- Explain commands before running them
