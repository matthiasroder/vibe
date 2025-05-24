# vibe-template
My approach to vibe coding

## Basic sequence
Use a non-reasoning ChatGPT or Claude model

1. architecture.md
   
   ```
   I’m building a [detailed description of your product]. Use [list of tools]. Give me the full architecture:
      - File + folder structure
      - What each part does
      - Where state lives, how services connect Format this entire document in markdown.
   ```

3. tasks.md

   ```
   Using that architecture, write a granular step-by-step plan to build the MVP. Each task should:
      - Be incredibly small + testable
      - Have a clear start + end
      - Focus on one concern
   I’ll be passing this off to an engineering LLM that will be told to complete one task at a time, allowing me to test in between.
   ```

4. claude.md

   ```
   # Engineering Principles
   - Write the absolute minimum code required
   - No sweeping changes
   - No unrelated edits
   - focus on just the task you're on
   - Make code precise, modular, testable
   - Don’t break existing functionality
   - If I need to do anything (e.g. bash/python etc.), tell me clearly
   ```
   
5. In claude:

   ```
   You’re an engineer building this codebase. You've been given architecture.md, tasks.md and claude.md
      - Read both carefully. There should be no ambiguity about what we’re building.
      - Follow http://tasks.md and complete one task at a time.
      - After each task, stop. I’ll test it. If it works, commit to GitHub and move to the next task.
   ```
