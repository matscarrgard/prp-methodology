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

---

## Workflow

### New Project
```
/prd [inputs/]    → Create PRD from notes/requirements
/scaffold         → Create project structure
/plan-feature     → Plan first feature from PRD
/execute          → Implement
/validate         → Test
/commit           → Ship
```

### Adding Features
```
/prime            → Load context (checks PRD, progress.txt)
/plan-feature     → Plan feature (references PRD for context)
/execute          → Implement
/validate         → Test
/commit           → Ship
```

### Key Files
- PRD: `docs/agents/prd.md` - Project scope and features
- Progress: `features/progress.txt` - Iteration memory
- Plans: `docs/agents/plans/` - Implementation plans

## Commands Reference

| Command | Purpose |
|---------|---------|
| `/prd` | Create/update PRD from inputs or conversation |
| `/scaffold` | Create project structure (language-specific) |
| `/prime` | Load project context |
| `/plan-feature` | Plan a feature (from PRD or description) |
| `/execute` | Execute implementation plan |
| `/validate` | Run tests and lint |
| `/commit` | Create git commit |

## Methodology

Using PRP methodology from `.prp/`:
- Workflow: `.prp/instructions/WORKFLOW.md`
- Story sizing: `.prp/instructions/STORY_SIZING.md`
