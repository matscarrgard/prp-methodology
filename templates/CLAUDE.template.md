# Project: [NAME]

## Overview
[What this project does - 2-3 sentences]

## Tech Stack
<!-- List your tech stack -->
- Language: [e.g., Python 3.13]
- Framework: [e.g., FastAPI]
- Database: [e.g., PostgreSQL]
- Other: [e.g., Redis, Docker]

## Project Commands

| Action | Command |
|--------|---------|
| Install | `[install command]` |
| Test | `[test command]` |
| Lint | `[lint command]` |
| Run | `[run command]` |

## Methodology

Using PRP methodology from `.prp/`:
- Workflow: `.prp/instructions/WORKFLOW.md`
- Story sizing: `.prp/instructions/STORY_SIZING.md`
- Ralph loops: `.prp/instructions/RALPH.md`

## Pattern Guides
<!-- List your pattern documentation -->
- [Pattern area]: `docs/guides/[guide].md`

## Architecture

```
src/
├── [main package]/
│   ├── core/           # Shared infrastructure
│   ├── [layer]/        # [Description]
│   └── [layer]/        # [Description]
└── tests/
```

## Code Style

<!-- Add your conventions -->
- [Convention 1]
- [Convention 2]

## Codebase Patterns
<!--
Patterns discovered during development.
Update this when you learn something reusable across ALL future work.
-->

## Current State

- Feature: `features/current.json`
- Progress: `features/progress.txt`

---

## Commands Reference

- `/prime` - Load project context
- `/plan-feature <desc>` - Plan new feature
- `/execute [plan]` - Execute implementation plan
- `/validate` - Run tests and lint
- `/commit` - Create git commit
