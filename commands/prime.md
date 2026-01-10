# Prime Project Context

Load project context and prepare for a new task.

## Process

1. **Read core documentation**
   - Read `CLAUDE.md` for global rules and architecture
   - Read project config file (pyproject.toml, package.json, etc.)

2. **Understand project structure**
   - List main source directory to understand current features
   - List core/shared directory to understand infrastructure
   - List docs directory to know available reference docs

3. **Check project state**
   - Run `git status` to see uncommitted changes
   - Run validation command if configured

4. **Load feature state** (if exists)
   - Read `features/progress.txt` for iteration history
   - Read `features/current.json` for active feature status

5. **Summarize readiness**
   Provide a brief summary:
   - Current features implemented
   - Available reference documentation
   - Any outstanding issues (uncommitted changes, lint errors)
   - Active feature status (if any)
   - Ready to receive task

## Output

A concise summary of the project state, ready for the next task.
