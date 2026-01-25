# Prime Project Context

Load project context and prepare for a new task.

## Important

When running shell commands (like `git status`), run them **without** the `-C` flag. Claude Code already runs from the project's working directory, so `-C` is unnecessary.

## Process

1. **Read core documentation**
   - Read `CLAUDE.md` for global rules and architecture
   - Read project config file (pyproject.toml, package.json, etc.)

2. **Understand project structure**
   - List main source directory to understand current features
   - List core/shared directory to understand infrastructure
   - List docs directory to know available reference docs

3. **Check project state**
   - Run `git status` to see uncommitted changes (no `-C` flag needed)
   - Run validation command if configured

4. **Load session state**
   - Read `TODO.md` for current/next tasks and recent log
   - Read `features/BACKLOG.md` for feature status overview
   - Read `features/progress.txt` for iteration history (if in-progress feature)

5. **Summarize readiness**
   Provide a brief summary:
   - Current TODO items (from TODO.md)
   - Feature backlog status (X draft, Y ready, Z in-progress, W complete)
   - Any outstanding issues (uncommitted changes, lint errors)
   - Ready to receive task

## Output

A concise summary of the project state, ready for the next task.
